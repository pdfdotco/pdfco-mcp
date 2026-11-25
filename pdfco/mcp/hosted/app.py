from collections.abc import Sequence

from fastmcp import FastMCP
from fastmcp.server.auth import OAuthProxy
from fastmcp.server.auth.oauth_proxy.models import UpstreamTokenSet
from fastmcp.server.auth.oauth_proxy.upstream import AsyncOAuth2Client
from fastmcp.server.dependencies import get_http_request
from fastmcp.server.transforms import GetToolNext, Transform, Visibility
from fastmcp.tools import Tool
from fastmcp.tools.tool_transform import ArgTransformConfig, ToolTransformConfig
from fastmcp.utilities.versions import VersionSpec
from key_value.aio.protocols import AsyncKeyValue
from key_value.aio.stores.memory import MemoryStore
from mcp.server.auth.provider import RefreshToken
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from pdfco.mcp.hosted.limits import (
    MCP_REQUESTS_PER_MINUTE,
    TOKEN_REFRESHES_PER_MINUTE,
    FixedWindowCounter,
    RateLimited,
)
from pdfco.mcp.hosted.middleware import (
    BackendUnavailableMiddleware,
    is_rate_limited,
    log_token_error_response,
    mark_rate_limited,
)
from pdfco.mcp.hosted.settings import HostedSettings
from pdfco.mcp.hosted.verifier import UserinfoVerifier
from pdfco.mcp.server import mcp as local_mcp

MCP_PATH = "/mcp"

# Where an authorization code may be delivered. Claude's hosted
# apps, ChatGPT's two callback forms, and loopback for desktop clients.
ALLOWED_CLIENT_REDIRECT_URIS = [
    "https://claude.ai/api/mcp/auth_callback",
    "https://chatgpt.com/connector_platform_oauth_redirect",
    "https://chatgpt.com/connector/oauth/*",
    "http://localhost:*/*",
    "http://127.0.0.1:*/*",
]

ACCESS_TOKEN_SECONDS = 3600
# Claude waits 10 s for a token response; the library's own default is 30 s.
UPSTREAM_TIMEOUT_SECONDS = 5.0
REFRESH_TOKEN_SECONDS = 90 * 24 * 3600

# Local-only tools. upload_file opens a path on the machine the server runs on,
# which in hosted mode is the container.
HOSTED_EXCLUDED_TOOLS = {"upload_file"}


class HideApiKey(Transform):
    """Removes the `api_key` argument from every tool that has one.

    In hosted mode the key comes from the caller's OAuth session, so the
    argument must not be offered; the key resolver ignores it as well.
    """

    _config = ToolTransformConfig(arguments={"api_key": ArgTransformConfig(hide=True)})

    def _apply(self, tool: Tool) -> Tool:
        if "api_key" in tool.parameters.get("properties", {}):
            return self._config.apply(tool)
        return tool

    async def list_tools(self, tools: Sequence[Tool]) -> Sequence[Tool]:
        return [self._apply(tool) for tool in tools]

    async def get_tool(
        self, name: str, call_next: GetToolNext, *, version: VersionSpec | None = None
    ) -> Tool | None:
        tool = await call_next(name, version=version)
        return None if tool is None else self._apply(tool)


# Set on a request once its session has been counted, so the hook below,
# which the library may call several times in one request, counts it once.
_COUNTED = "pdfco_session_counted"


class PdfcoOAuthProxy(OAuthProxy):
    """OAuthProxy with per-session limits and a short upstream timeout.

    A slow upstream answers 503 before the client stops waiting. A session over
    its limit is refused before any call to the account service. Failed token
    responses are logged with their status.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mcp_limit = FixedWindowCounter(MCP_REQUESTS_PER_MINUTE)
        self.refresh_limit = FixedWindowCounter(TOKEN_REFRESHES_PER_MINUTE)

    def _get_verification_token(
        self, upstream_token_set: UpstreamTokenSet
    ) -> str | None:
        # Called after the JWT signature check and before userinfo, so forged
        # tokens never reach the counter and an over-limit request never
        # reaches userinfo. Returning None makes the library answer 401, which
        # the middleware turns into 429.
        try:
            state = get_http_request().state
        except RuntimeError:
            return super()._get_verification_token(upstream_token_set)
        if not getattr(state, _COUNTED, False):
            setattr(state, _COUNTED, True)
            retry_after = self.mcp_limit.hit(upstream_token_set.upstream_token_id)
            if retry_after is not None:
                mark_rate_limited(retry_after)
        if is_rate_limited(state):
            return None
        return super()._get_verification_token(upstream_token_set)

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: RefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        session = await self._session_of(refresh_token.token)
        if session is not None:
            retry_after = self.refresh_limit.hit(session)
            if retry_after is not None:
                raise RateLimited(retry_after)
        return await super().exchange_refresh_token(client, refresh_token, scopes)

    async def _session_of(self, refresh_token: str) -> str | None:
        """The upstream_token_id behind a refresh token, as the library finds it."""
        try:
            payload = self.jwt_issuer.verify_token(
                refresh_token, expected_token_use="refresh"
            )
        except Exception:
            # The library rejects it with invalid_grant right after.
            return None
        mapping = await self._jti_mapping_store.get(key=payload["jti"])
        return mapping.upstream_token_id if mapping else None

    def _create_upstream_oauth_client(self) -> AsyncOAuth2Client:
        default = super()._create_upstream_oauth_client()
        client = AsyncOAuth2Client(
            client_id=default.client_id,
            client_secret=default.client_secret,
            token_endpoint_auth_method=default.token_endpoint_auth_method,
            timeout=UPSTREAM_TIMEOUT_SECONDS,
        )
        # The client takes no hook option; _client is its httpx2 client.
        client._client.event_hooks = {"response": [log_token_error_response]}
        return client


def build_auth(
    settings: HostedSettings, client_storage: AsyncKeyValue | None = None
) -> OAuthProxy:
    upstream = settings.upstream_url
    return PdfcoOAuthProxy(
        upstream_authorization_endpoint=f"{upstream}/oauth/authorize",
        upstream_token_endpoint=f"{upstream}/oauth/token",
        upstream_client_id=settings.upstream_client_id,
        upstream_client_secret=settings.upstream_client_secret,
        token_verifier=UserinfoVerifier(upstream),
        base_url=settings.base_url,
        allowed_client_redirect_uris=ALLOWED_CLIENT_REDIRECT_URIS,
        # In-memory until a persistent, encrypted store is wired in.
        client_storage=client_storage or MemoryStore(),
        jwt_signing_key=settings.jwt_signing_key,
        fastmcp_access_token_expiry_seconds=ACCESS_TOKEN_SECONDS,
        fallback_refresh_token_expiry_seconds=REFRESH_TOKEN_SECONDS,
        # Refresh upstream only after expiry; Claude refreshes ahead of expiry
        # itself and a second refresher would race it for the rotating token.
        token_expiry_threshold_seconds=0,
    )


def build_hosted_server(auth: OAuthProxy) -> FastMCP:
    hosted = FastMCP("pdfco", auth=auth)
    hosted.mount(local_mcp)
    hosted.add_transform(HideApiKey())
    hosted.add_transform(Visibility(False, names=HOSTED_EXCLUDED_TOOLS))

    @hosted.custom_route("/healthz", methods=["GET"], include_in_schema=False)
    async def healthz(_: Request) -> JSONResponse:
        return JSONResponse({"status": "ok"})

    return hosted


def build_http_app(hosted: FastMCP):
    # Passed to http_app, the middleware sits inside the authentication
    # middleware, so it sees the 401 the /mcp route produces and the errors
    # the OAuth routes raise.
    return hosted.http_app(
        path=MCP_PATH,
        stateless_http=True,
        middleware=[Middleware(BackendUnavailableMiddleware)],
    )


def build_hosted_app(
    settings: HostedSettings, client_storage: AsyncKeyValue | None = None
):
    return build_http_app(build_hosted_server(build_auth(settings, client_storage)))
