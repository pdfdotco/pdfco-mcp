from fastmcp.server.auth import AccessToken, TokenVerifier
from httpx import AsyncClient, HTTPError

from pdfco.mcp.hosted.middleware import mark_backend_unavailable

REQUIRED_SCOPES = ["openid", "api"]
USERINFO_TIMEOUT_SECONDS = 5.0

# Answers in which the account service judged the token itself: expired,
# revoked, or its user deleted (404). Anything else is no verdict.
TOKEN_REJECTED = {401, 403, 404}


class UserinfoVerifier(TokenVerifier):
    """Verifies a PDF.co OAuth access token by calling `/oauth/userinfo`.

    The OAuth proxy calls this with the stored upstream token after it has
    checked its own JWT locally. A 200 answer yields the user's id and API key
    as claims; tool code reads them through `get_access_token()`. Nothing is
    cached, so revocation upstream takes effect on the next request.

    Both kinds of failure return None, which the library turns into a 401.
    When the service gave no verdict the request is also marked, and the
    hosted middleware answers 503 instead.
    """

    def __init__(self, upstream_url: str):
        # The scopes are recorded on every returned token and checked by the
        # library on each request. PDF.co's userinfo needs `openid`, and
        # returns api_key only with `api`.
        super().__init__(required_scopes=REQUIRED_SCOPES)
        self._userinfo_url = f"{upstream_url.rstrip('/')}/oauth/userinfo"

    async def verify_token(self, token: str) -> AccessToken | None:
        async with AsyncClient(timeout=USERINFO_TIMEOUT_SECONDS) as client:
            try:
                response = await client.get(
                    self._userinfo_url, headers={"Authorization": f"Bearer {token}"}
                )
            except HTTPError as error:
                mark_backend_unavailable(f"userinfo {type(error).__name__}")
                return None
        if response.status_code in TOKEN_REJECTED:
            return None
        if response.status_code != 200:
            mark_backend_unavailable(f"userinfo HTTP {response.status_code}")
            return None
        try:
            body = response.json()
        except ValueError:
            mark_backend_unavailable("userinfo returned a non-JSON body")
            return None
        sub = body.get("sub") if isinstance(body, dict) else None
        if not sub:
            mark_backend_unavailable("userinfo returned no sub")
            return None
        claims = {"sub": str(sub)}
        if body.get("api_key"):
            claims["api_key"] = body["api_key"]
        return AccessToken(
            token=token,
            client_id="pdfco-mcp",
            scopes=list(REQUIRED_SCOPES),
            subject=str(sub),
            claims=claims,
        )
