"""Answers 503 instead of 401 when the PDF.co account service could not answer.

A 401 tells a client its token is no good, so it refreshes or asks the user to
sign in again. That is right when the account service rejected the token, and
wrong when the service was down: the client would discard a refresh token that
still works. The verifier marks the request when it got no verdict, and this
middleware turns the 401 that follows into a 503. Upstream errors raised while
the proxy talks to the token endpoint become a 503 as well.
"""

import json
import logging

import httpx2
from authlib.integrations.base_client import OAuthError
from fastmcp.server.dependencies import get_http_request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger(__name__)

RETRY_AFTER_SECONDS = 30
_MARK = "pdfco_backend_unavailable"

# What the proxy raises when the upstream token endpoint gives no usable answer.
# invalid_grant never gets here: the library turns it into a 400 itself.
UPSTREAM_ERRORS = (httpx2.HTTPError, OAuthError, json.JSONDecodeError)

_BODY = json.dumps(
    {
        "error": "temporarily_unavailable",
        "error_description": "The PDF.co account service is unavailable. Retry later.",
    }
).encode()


def mark_backend_unavailable(reason: str) -> None:
    """Record on the current request that the account service gave no verdict."""
    logger.warning("PDF.co account service unavailable: %s", reason)
    try:
        request = get_http_request()
    except RuntimeError:
        return
    setattr(request.state, _MARK, True)


async def _send_unavailable(send: Send) -> None:
    await send(
        {
            "type": "http.response.start",
            "status": 503,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(_BODY)).encode()),
                (b"retry-after", str(RETRY_AFTER_SECONDS).encode()),
                (b"cache-control", b"no-store"),
            ],
        }
    )
    await send({"type": "http.response.body", "body": _BODY})


class BackendUnavailableMiddleware:
    """Pure ASGI, so streamed MCP responses pass through untouched."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        started = False
        replaced = False

        async def guarded_send(message: Message) -> None:
            nonlocal started, replaced
            if message["type"] == "http.response.start":
                started = True
                if message["status"] == 401 and scope.get("state", {}).get(_MARK):
                    replaced = True
                    await _send_unavailable(send)
                    return
            elif replaced:
                return
            await send(message)

        try:
            await self.app(scope, receive, guarded_send)
        except UPSTREAM_ERRORS as error:
            if started:
                raise
            logger.warning(
                "PDF.co token endpoint unavailable on %s: %s",
                scope.get("path"),
                type(error).__name__,
            )
            await _send_unavailable(send)
