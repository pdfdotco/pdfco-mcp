"""Hosted mode: who may call, and with whose key."""

import asyncio
import logging
import secrets
from urllib.parse import parse_qs

import pytest
from fastmcp import Client

from pdfco.mcp import mcp as local_mcp
from .flow import (
    RESOURCE,
    jwt_claims,
    mcp_client,
    parse,
    register_client,
    sign_in,
    stored_text,
)

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


async def test_request_without_token_is_refused_with_a_metadata_pointer(serve, oauth):
    async with serve() as http:
        response = await http.post("/mcp", json=INITIALIZE, headers=MCP_HEADERS)
    assert response.status_code == 401
    assert "resource_metadata=" in response.headers["www-authenticate"]
    assert oauth.userinfo_calls == []


async def test_random_and_forged_tokens_never_reach_the_backend(serve, oauth, api):
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        header, payload, _ = jwt.split(".")
        forged = f"{header}.{payload}.{secrets.token_urlsafe(32)}"
        oauth.userinfo_calls.clear()
        tokens = [secrets.token_urlsafe(32) for _ in range(1000)] + [forged]
        for token in tokens:
            response = await http.post(
                "/mcp",
                json=INITIALIZE,
                headers={**MCP_HEADERS, "Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 401
    assert oauth.userinfo_calls == []
    assert api.requests == []


async def test_each_user_calls_the_api_with_their_own_key(serve, oauth, api):
    async with serve() as http:
        alice = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        bob = await sign_in(http, oauth.add_user("bob", "202", "key-bob"))

        async def info(jwt: str, n: int):
            async with mcp_client(http, jwt) as client:
                for i in range(n):
                    await client.call_tool(
                        "pdf_info_reader", {"url": f"https://f/{i}.pdf"}
                    )

        await asyncio.gather(info(alice, 5), info(bob, 5))

    keys = sorted(r.headers["x-api-key"] for r in api.requests)
    assert keys == ["key-alice"] * 5 + ["key-bob"] * 5
    for request in api.requests:
        assert request.headers["user-agent"].endswith(" (hosted)")


async def test_an_api_key_argument_is_rejected_and_never_sent(serve, oauth, api):
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        async with mcp_client(http, jwt) as client:
            result = await client.call_tool(
                "pdf_info_reader",
                {"url": "https://f/a.pdf", "api_key": "key-of-someone-else"},
                raise_on_error=False,
            )
    assert result.is_error
    assert "api_key" in result.content[0].text
    assert api.requests == []


async def test_server_wide_key_is_never_used_for_a_hosted_user(
    serve, oauth, api, monkeypatch
):
    import pdfco.mcp.services.client as client_module

    monkeypatch.setattr(client_module, "X_API_KEY", "server-wide-key")
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        async with mcp_client(http, jwt) as client:
            await client.call_tool("pdf_info_reader", {"url": "https://f/a.pdf"})
    assert api.last.headers["x-api-key"] == "key-alice"


async def test_userinfo_without_api_key_is_a_tool_error(serve, oauth, api):
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("carol", "303", api_key=None))
        async with mcp_client(http, jwt) as client:
            response = parse(
                await client.call_tool("pdf_info_reader", {"url": "https://f/a.pdf"})
            )
    assert response.status == "error"
    assert "did not return an API key" in str(response.content)
    assert api.requests == []


async def test_userinfo_failure_refuses_the_request(serve, oauth, api):
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        oauth.userinfo_status = 500
        response = await http.post(
            "/mcp",
            json=INITIALIZE,
            headers={**MCP_HEADERS, "Authorization": f"Bearer {jwt}"},
        )
    # Every userinfo failure is a 401 for now; outages are to answer 503.
    assert response.status_code == 401
    assert api.requests == []


async def test_no_key_is_stored_or_logged(serve, oauth, api, store, caplog):
    caplog.set_level(logging.DEBUG)
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        async with mcp_client(http, jwt) as client:
            await client.call_tool("pdf_info_reader", {"url": "https://f/a.pdf"})
    assert api.last.headers["x-api-key"] == "key-alice"
    assert "key-alice" not in await stored_text(store)
    assert "key-alice" not in caplog.text


async def test_issued_token_is_bound_to_the_mcp_endpoint_for_one_hour(serve, oauth):
    flow = {}
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
    claims = jwt_claims(jwt)
    assert claims["aud"] == RESOURCE
    assert claims["exp"] - claims["iat"] == 3600
    assert flow["token"]["expires_in"] == 3600


async def test_upstream_sign_in_asks_for_openid_and_api(serve, oauth):
    flow = {}
    async with serve() as http:
        await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
    upstream = flow["upstream_authorize"]
    query = {k: v[0] for k, v in parse_qs(upstream.query).items()}
    assert f"{upstream.scheme}://{upstream.netloc}{upstream.path}" == (
        "https://oauth.test/oauth/authorize"
    )
    assert query["scope"].split() == ["openid", "api"]
    assert query["redirect_uri"] == "https://mcp.test/auth/callback"


async def test_protected_resource_metadata_names_the_mcp_endpoint(serve):
    async with serve() as http:
        response = await http.get("/.well-known/oauth-protected-resource/mcp")
    assert response.status_code == 200
    body = response.json()
    assert body["resource"] == RESOURCE
    assert body["authorization_servers"] == ["https://mcp.test/"]


async def test_foreign_resource_is_refused(serve, oauth):
    async with serve() as http:
        registered = await register_client(http, "http://localhost:5555/callback")
        response = await http.get(
            "/authorize",
            params={
                "response_type": "code",
                "client_id": registered.json()["client_id"],
                "redirect_uri": "http://localhost:5555/callback",
                "state": "s",
                "code_challenge": "x" * 43,
                "code_challenge_method": "S256",
                "resource": "https://other.example/mcp",
            },
        )
    assert "invalid_target" in (response.headers.get("location", "") + response.text)


@pytest.mark.parametrize(
    "redirect_uri",
    [
        "http://localhost/callback",
        "http://127.0.0.1/callback",
        "http://localhost:33418/callback",
        "https://claude.ai/api/mcp/auth_callback",
        "https://chatgpt.com/connector/oauth/abc123",
    ],
)
async def test_allowed_redirect_uris_are_accepted(serve, redirect_uri):
    async with serve() as http:
        response = await register_client(http, redirect_uri)
    assert response.status_code == 201, response.text


@pytest.mark.parametrize(
    "redirect_uri",
    [
        "https://evil.example/callback",
        "https://claude.ai.evil.example/api/mcp/auth_callback",
        "cursor://anysphere.cursor-mcp/oauth/callback",
    ],
)
async def test_other_redirect_uris_are_refused(serve, redirect_uri):
    async with serve() as http:
        response = await register_client(http, redirect_uri)
    assert response.status_code == 400
    assert response.json()["error"] == "invalid_redirect_uri"


async def test_health_check_needs_no_token(serve):
    async with serve() as http:
        response = await http.get("/healthz")
    assert response.status_code == 200


async def test_tool_list_is_local_minus_upload_file_without_api_key(serve, oauth):
    async with Client(local_mcp) as client:
        local = {t.name: t for t in await client.list_tools()}
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        async with mcp_client(http, jwt) as client:
            hosted = {t.name: t for t in await client.list_tools()}
            upload = await client.call_tool(
                "upload_file", {"file_path": "/etc/hostname"}, raise_on_error=False
            )

    assert set(hosted) == set(local) - {"upload_file"}
    for name, tool in hosted.items():
        assert "api_key" not in tool.inputSchema.get("properties", {}), name
        assert tool.title == local[name].title, name
        assert tool.annotations == local[name].annotations, name
    assert upload.is_error
    assert "Unknown tool" in upload.content[0].text
