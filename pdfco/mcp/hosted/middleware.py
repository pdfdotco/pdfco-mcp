"""Answers 503 or 429 instead of 401 when the refusal is not about the token.

The account service could not answer (503), or the session is over its
request limit (429).

A 401 tells a client its token is no good, so it refreshes or asks the user to
sign in again. That is right when the account service rejected the token, and
wrong when the service was down: the client would discard a refresh token that
still works. The verifier marks the request when it got no verdict, and this
middleware turns the 401 that follows into a 503. Upstream errors raised while
the proxy talks to the token endpoint become a 503 as well, except an OAuth
error: that is the service judging our own client configuration or request,
which a retry cannot fix, so it becomes a 500.

A session over its request limit is refused the same way: the proxy marks the
request (or raises `RateLimited` on /token) and this middleware answers 429.
"""

import json
import logging

import httpx2

# fastmcp re-exports authlib's class up to 4.2.5 and defines its own from 4.2.6;
# importing it from fastmcp catches whichever the proxy raises.
from fastmcp.server.auth.oauth_proxy.upstream import OAuthError
from fastmcp.server.dependencies import get_http_request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from pdfco.mcp.hosted.limits import RateLimited

logger = logging.getLogger(__name__)

RETRY_AFTER_SECONDS = 30
_MARK = "pdfco_backend_unavailable"
_RATE_MARK = "pdfco_rate_limited"

# What the proxy raises when the upstream token endpoint gives no usable answer.
# A non-JSON body comes only with a status below 500 (a WAF page, say); the
# client hook in app.py logs that status.
UPSTREAM_ERRORS = (httpx2.HTTPError, json.JSONDecodeError)

_BODY = json.dumps(
    {
        "error": "temporarily_unavailable",
        "error_description": "The PDF.co account service is unavailable. Retry later.",
    }
).encode()
_MISCONFIGURED_BODY = json.dumps(
    {
        "error": "server_error",
        "error_description": "The PDF.co MCP server is misconfigured.",
    }
).encode()
_RATE_BODY = json.dumps(
    {
        "error": "rate_limited",
        "error_description": "Too many requests for this session. Retry later.",
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


async def log_token_error_response(response: httpx2.Response) -> None:
    """Upstream client hook: name the status of a failed token response.

    The errors the proxy raises do not all carry it; a non-JSON body (a WAF
    page, say) surfaces only as a JSONDecodeError. The service itself answers
    every 4xx in JSON, so a non-JSON 4xx did not come from it: a WAF or proxy
    in front of it, or a wrong upstream URL. That is logged at error level.
    """
    status = response.status_code
    content_type = response.headers.get("content-type", "")
    shown = content_type or "without a content type"
    if 400 <= status < 500 and "json" not in content_type.lower():
        logger.error("PDF.co token endpoint answered %s %s, not JSON", status, shown)
    elif status >= 400:
        logger.warning("PDF.co token endpoint answered %s %s", status, shown)


def mark_rate_limited(retry_after: int) -> None:
    """Record on the current request that its session is over the limit."""
    try:
        request = get_http_request()
    except RuntimeError:
        return
    setattr(request.state, _RATE_MARK, retry_after)


def is_rate_limited(state) -> bool:
    """Whether `mark_rate_limited` was called on the request with this state."""
    return bool(getattr(state, _RATE_MARK, None))


async def _send_json(
    send: Send, status: int, body: bytes, retry_after: int | None
) -> None:
    headers = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(body)).encode()),
        (b"cache-control", b"no-store"),
    ]
    if retry_after is not None:
        headers.append((b"retry-after", str(retry_after).encode()))
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body})


async def _send_unavailable(send: Send) -> None:
    await _send_json(send, 503, _BODY, RETRY_AFTER_SECONDS)


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
                state = scope.get("state", {})
                if message["status"] == 401 and state.get(_RATE_MARK):
                    replaced = True
                    await _send_json(send, 429, _RATE_BODY, state[_RATE_MARK])
                    return
                if message["status"] == 401 and state.get(_MARK):
                    replaced = True
                    await _send_unavailable(send)
                    return
            elif replaced:
                return
            await send(message)

        try:
            await self.app(scope, receive, guarded_send)
        except RateLimited as error:
            if started:
                raise
            await _send_json(send, 429, _RATE_BODY, error.retry_after)
        except OAuthError as error:
            # invalid_grant never gets here: the library answers it itself.
            if started:
                raise
            logger.error(
                "PDF.co token endpoint rejected this server's request on %s: %s",
                scope.get("path"),
                error.error,
            )
            await _send_json(send, 500, _MISCONFIGURED_BODY, None)
        except UPSTREAM_ERRORS as error:
            if started:
                raise
            logger.warning(
                "PDF.co token endpoint unavailable on %s: %s",
                scope.get("path"),
                type(error).__name__,
            )
            await _send_unavailable(send)
