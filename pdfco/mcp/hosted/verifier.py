from fastmcp.server.auth import AccessToken, TokenVerifier
from httpx import AsyncClient, HTTPError

REQUIRED_SCOPES = ["openid", "api"]


class UserinfoVerifier(TokenVerifier):
    """Verifies a PDF.co OAuth access token by calling `/oauth/userinfo`.

    The OAuth proxy calls this with the stored upstream token after it has
    checked its own JWT locally. A 200 answer yields the user's id and API key
    as claims; tool code reads them through `get_access_token()`. Nothing is
    cached, so revocation upstream takes effect on the next request.
    """

    def __init__(self, upstream_url: str):
        # The scopes are recorded on every returned token and checked by the
        # library on each request. PDF.co's userinfo needs `openid`, and
        # returns api_key only with `api`.
        super().__init__(required_scopes=REQUIRED_SCOPES)
        self._userinfo_url = f"{upstream_url.rstrip('/')}/oauth/userinfo"

    async def verify_token(self, token: str) -> AccessToken | None:
        async with AsyncClient() as client:
            try:
                response = await client.get(
                    self._userinfo_url, headers={"Authorization": f"Bearer {token}"}
                )
            except HTTPError:
                # For now an unreachable server counts as a rejected token
                # (401); outages are to answer 503 instead.
                return None
        if response.status_code != 200:
            return None
        body = response.json()
        sub = body.get("sub")
        if not sub:
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
