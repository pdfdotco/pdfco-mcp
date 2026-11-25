"""Per-session request limits, counted before any call to the account service.

A session is the proxy's `upstream_token_id`: created when the user signs in and
kept across refreshes, while the access JWT and refresh token change every hour.
Counting by it means a refresh does not reset the count.
"""

import math
import time
from collections.abc import Callable

# One tool call is several /mcp requests (initialize, list, call, ...), each
# with one userinfo call. 300 a minute stops a runaway session, not a busy one.
MCP_REQUESTS_PER_MINUTE = 300
TOKEN_REFRESHES_PER_MINUTE = 10
WINDOW_SECONDS = 60


class FixedWindowCounter:
    """Counts hits per key in fixed windows shared by all keys.

    All keys share the same window boundaries, so when a window ends every
    count is dropped at once and memory never holds more than one window.
    Counts are per process: with two tasks a session can reach twice the limit.
    """

    def __init__(
        self,
        limit: int,
        window_seconds: int = WINDOW_SECONDS,
        clock: Callable[[], float] = time.time,
    ):
        self.limit = limit
        self._window_seconds = window_seconds
        self._clock = clock
        self._window: int | None = None
        self._counts: dict[str, int] = {}

    def hit(self, key: str) -> int | None:
        """Count one hit; None if allowed, else seconds until the window ends."""
        now = self._clock()
        window = int(now // self._window_seconds)
        if window != self._window:
            self._window = window
            self._counts = {}
        count = self._counts.get(key, 0) + 1
        self._counts[key] = count
        if count <= self.limit:
            return None
        remaining = (window + 1) * self._window_seconds - now
        return max(1, math.ceil(remaining))


class RateLimited(Exception):
    """Raised on a route when a session is over its limit."""

    def __init__(self, retry_after: int):
        super().__init__(f"rate limited, retry after {retry_after} s")
        self.retry_after = retry_after
