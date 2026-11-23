from collections.abc import Sequence

from fastmcp import FastMCP
from fastmcp.server.auth import OAuthProxy
from fastmcp.server.auth.oauth_proxy.upstream import AsyncOAuth2Client
from fastmcp.server.transforms import GetToolNext, Transform, Visibility
from fastmcp.tools import Tool
from fastmcp.tools.tool_transform import ArgTransformConfig, ToolTransformConfig
from fastmcp.utilities.versions import VersionSpec
from key_value.aio.protocols import AsyncKeyValue
from key_value.aio.stores.memory import MemoryStore
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from pdfco.mcp.hosted.middleware import BackendUnavailableMiddleware
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


class PdfcoOAuthProxy(OAuthProxy):
    """OAuthProxy whose calls to the upstream token endpoint give up in time.

    A slow upstream then answers 503 before the client stops waiting.
    """

    def _create_upstream_oauth_client(self) -> AsyncOAuth2Client:
        default = super()._create_upstream_oauth_client()
        return AsyncOAuth2Client(
            client_id=default.client_id,
            client_secret=default.client_secret,
            token_endpoint_auth_method=default.token_endpoint_auth_method,
            timeout=UPSTREAM_TIMEOUT_SECONDS,
        )


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
