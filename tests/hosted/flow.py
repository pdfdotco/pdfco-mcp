"""Fakes and OAuth-flow helpers for the hosted tests.

Three fakes stand in for the network: the PDF.co OAuth server's token endpoint (reached
by the proxy through httpx2), its userinfo endpoint (reached by the verifier
through httpx), and `api.pdf.co` (the `api` fixture from tests/conftest.py).
"""

import base64
import hashlib
import json
import re
import secrets
from urllib.parse import parse_qs, urlparse

import httpx
import httpx2
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from key_value.aio.stores.memory import MemoryStore

from pdfco.mcp.hosted.app import MCP_PATH
from pdfco.mcp.hosted.settings import HostedSettings
from pdfco.mcp.models import BaseResponse

BASE_URL = "https://mcp.test"
UPSTREAM_URL = "https://oauth.test"
RESOURCE = f"{BASE_URL}{MCP_PATH}"
INITIALIZE = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "t", "version": "0"},
    },
}
MCP_HEADERS = {"Accept": "application/json, text/event-stream"}
SETTINGS = HostedSettings(
    base_url=BASE_URL,
    upstream_url=UPSTREAM_URL,
    upstream_client_id="upstream-client",
    upstream_client_secret="upstream-secret",
    jwt_signing_key="test-signing-key",
)


class FakeOAuth:
    """The PDF.co OAuth server: one authorization code per user, userinfo per access token."""

    def __init__(self):
        self.users: dict[str, dict] = {}  # upstream access token -> userinfo body
        self.userinfo_calls: list[str] = []
        self.token_requests: list[dict] = []
        self.userinfo_status = 200
        # Outage knobs. userinfo_error is raised instead of answering;
        # userinfo_raw replaces the JSON body; broken_users answer 500.
        self.userinfo_error: Exception | None = None
        self.userinfo_raw: str | None = None
        self.broken_users: set[str] = set()
        self.userinfo_client_kwargs: list[dict] = []
        # None, or a callable returning the token endpoint's answer/raising.
        self.token_failure = None

    def add_user(self, name: str, sub: str, api_key: str | None) -> str:
        body = {"sub": sub}
        if api_key is not None:
            body["api_key"] = api_key
        self.users[f"up-access-{name}"] = body
        return f"code-{name}"

    def token_handler(self, request: httpx2.Request) -> httpx2.Response:
        form = {k: v[0] for k, v in parse_qs(request.content.decode()).items()}
        self.token_requests.append(form)
        if form["grant_type"] == "refresh_token" and self.token_failure:
            return self.token_failure()
        if form["grant_type"] == "refresh_token":
            name = form["refresh_token"].removeprefix("up-refresh-")
        else:
            name = form["code"].removeprefix("code-")
        return httpx2.Response(
            200,
            json={
                "access_token": f"up-access-{name}",
                "refresh_token": f"up-refresh-{name}",
                "token_type": "Bearer",
                # PDF.co gives authorization_code access tokens 10 days
                # (Authlib's default), so the proxy's own 1-hour bound is visible.
                "expires_in": 10 * 24 * 3600,
                "scope": "openid api",
            },
        )

    def userinfo_handler(self, request: httpx.Request) -> httpx.Response:
        token = request.headers["Authorization"].removeprefix("Bearer ")
        self.userinfo_calls.append(token)
        body = self.users.get(token)
        if body is None:
            return httpx.Response(401, json={"error": "invalid_token"})
        if self.userinfo_error is not None:
            raise self.userinfo_error
        if self.userinfo_raw is not None:
            return httpx.Response(200, text=self.userinfo_raw)
        if token.removeprefix("up-access-") in self.broken_users:
            return httpx.Response(500, json=body)
        # A failing status still carries the user's body, so a verifier that
        # ignored the status would be caught.
        return httpx.Response(self.userinfo_status, json=body)


async def stored_text(store: MemoryStore) -> str:
    """Everything the proxy persisted, as one string to search."""
    parts = []
    for collection in await store.collections():
        for key in await store.keys(collection=collection):
            parts.append(
                f"{collection}/{key}={await store.get(key, collection=collection)!r}"
            )
    return "\n".join(parts)


def pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(48)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .rstrip(b"=")
        .decode()
    )
    return verifier, challenge


async def register_client(http: httpx.AsyncClient, redirect_uri: str) -> httpx.Response:
    return await http.post(
        "/register",
        json={
            "redirect_uris": [redirect_uri],
            "client_name": "test client",
            "token_endpoint_auth_method": "none",
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
        },
    )


async def sign_in(
    http: httpx.AsyncClient, upstream_code: str, flow: dict | None = None
) -> str:
    """Run DCR, authorize, consent, upstream callback and token exchange; return the JWT.

    `flow` collects the intermediate responses for tests that inspect them.
    """
    flow = {} if flow is None else flow
    redirect_uri = "http://localhost:5555/callback"
    registered = await register_client(http, redirect_uri)
    assert registered.status_code == 201, registered.text
    client_id = registered.json()["client_id"]
    verifier, challenge = pkce_pair()

    authorize = await http.get(
        "/authorize",
        params={
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "state": "client-state",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "resource": RESOURCE,
        },
    )
    assert authorize.status_code == 302, authorize.text
    consent_page = await http.get(authorize.headers["location"])
    assert consent_page.status_code == 200, consent_page.text
    fields = dict(
        re.findall(r'name="(txn_id|csrf_token)"\s+value="([^"]+)"', consent_page.text)
    )
    approved = await http.post("/consent", data={**fields, "action": "approve"})
    assert approved.status_code in (302, 303), approved.text
    upstream_authorize = urlparse(approved.headers["location"])
    flow["upstream_authorize"] = upstream_authorize
    query = {k: v[0] for k, v in parse_qs(upstream_authorize.query).items()}

    callback = await http.get(
        "/auth/callback", params={"code": upstream_code, "state": query["state"]}
    )
    assert callback.status_code in (302, 303), callback.text
    client_redirect = urlparse(callback.headers["location"])
    code = parse_qs(client_redirect.query)["code"][0]

    token = await http.post(
        "/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "code_verifier": verifier,
            "resource": RESOURCE,
        },
    )
    assert token.status_code == 200, token.text
    flow["token"] = token.json()
    flow["client_id"] = client_id
    return flow["token"]["access_token"]


def mcp_client(http: httpx.AsyncClient, jwt: str | None) -> Client:
    transport = StreamableHttpTransport(
        f"{BASE_URL}{MCP_PATH}",
        auth=jwt,
        httpx_client_factory=lambda **kwargs: httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=http.app), **kwargs
        ),
    )
    return Client(transport)


def parse(result) -> BaseResponse:
    return BaseResponse.model_validate_json(result.content[0].text)


def jwt_claims(jwt: str) -> dict:
    payload = jwt.split(".")[1]
    return json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
