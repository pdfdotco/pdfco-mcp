"""Hosted mode: per-session limits, counted before any account-service call."""

import asyncio
import time

import httpx
import pytest

import pdfco.mcp.hosted.verifier as verifier_module
from pdfco.mcp.hosted.limits import (
    MCP_REQUESTS_PER_MINUTE,
    TOKEN_REFRESHES_PER_MINUTE,
    FixedWindowCounter,
)
from pdfco.mcp.hosted.verifier import USERINFO_CONCURRENCY, UserinfoVerifier

from .flow import UPSTREAM_URL, jwt_claims, sign_in
from .test_hosted_outage import initialize, refresh

# 15 s into a minute window, so an over-limit answer says 45 s are left.
NOW = 1_000 * 60 + 15.0


def fixed_clock():
    return NOW


def assert_rate_limited(response: httpx.Response):
    assert response.status_code == 429, response.text
    assert response.headers["retry-after"] == "45"
    assert "www-authenticate" not in response.headers
    assert response.json()["error"] == "rate_limited"


async def refreshed(http, flow: dict) -> str:
    """Refresh through /token, keep the rotated tokens in `flow`, return the JWT."""
    response = await refresh(http, flow)
    assert response.status_code == 200, response.text
    flow["token"] = response.json()
    return flow["token"]["access_token"]


async def expire_upstream_token(proxy, jwt: str):
    mapping = await proxy._jti_mapping_store.get(key=jwt_claims(jwt)["jti"])
    tokens = await proxy._upstream_token_store.get(key=mapping.upstream_token_id)
    tokens.expires_at = time.time() - 1
    await proxy._upstream_token_store.put(
        key=mapping.upstream_token_id, value=tokens, ttl=3600
    )


def test_default_limits(proxy):
    assert MCP_REQUESTS_PER_MINUTE == 300
    assert TOKEN_REFRESHES_PER_MINUTE == 10
    assert USERINFO_CONCURRENCY == 10
    assert proxy.mcp_limit.limit == MCP_REQUESTS_PER_MINUTE
    assert proxy.refresh_limit.limit == TOKEN_REFRESHES_PER_MINUTE


def test_counter_drops_every_count_when_the_window_ends():
    now = [NOW]
    counter = FixedWindowCounter(1, clock=lambda: now[0])
    assert counter.hit("a") is None
    assert counter.hit("b") is None
    assert counter.hit("a") == 45
    now[0] += 45
    assert counter.hit("a") is None
    assert counter._counts == {"a": 1}


async def test_session_over_the_limit_answers_429_without_userinfo(serve, oauth, proxy):
    proxy.mcp_limit = FixedWindowCounter(2, clock=fixed_clock)
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        assert (await initialize(http, jwt)).status_code == 200
        assert (await initialize(http, jwt)).status_code == 200
        calls = len(oauth.userinfo_calls)
        response = await initialize(http, jwt)
    assert_rate_limited(response)
    assert len(oauth.userinfo_calls) == calls


async def test_forged_tokens_never_reach_the_counter(serve, oauth, proxy):
    proxy.mcp_limit = FixedWindowCounter(1, clock=fixed_clock)
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        header, payload, signature = jwt.split(".")
        forged = f"{header}.{payload}.{signature[::-1]}"
        for _ in range(3):
            assert (await initialize(http, forged)).status_code == 401
        assert (await initialize(http, jwt)).status_code == 200


async def test_count_survives_a_refresh_and_spares_other_sessions(serve, oauth, proxy):
    proxy.mcp_limit = FixedWindowCounter(2, clock=fixed_clock)
    flow = {}
    async with serve() as http:
        alice = await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
        bob = await sign_in(http, oauth.add_user("bob", "202", "key-bob"))
        assert (await initialize(http, alice)).status_code == 200

        # A real refresh changes the upstream access token as well.
        oauth.users["up-access-alice-2"] = oauth.users["up-access-alice"]
        oauth.next_access["alice"] = "up-access-alice-2"
        alice = await refreshed(http, flow)
        assert (await initialize(http, alice)).status_code == 200
        assert_rate_limited(await initialize(http, alice))
        assert (await initialize(http, bob)).status_code == 200


async def test_internal_refresh_verifies_the_new_token_and_counts_once(
    serve, oauth, proxy
):
    # One request runs the counting hook several times when the upstream token
    # has expired; with a limit of one, a second count would refuse it.
    proxy.mcp_limit = FixedWindowCounter(1, clock=fixed_clock)
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        await expire_upstream_token(proxy, jwt)
        body = oauth.users.pop("up-access-alice")
        oauth.users["up-access-alice-2"] = body
        oauth.next_access["alice"] = "up-access-alice-2"

        response = await initialize(http, jwt)
        assert response.status_code == 200, response.text
        assert oauth.userinfo_calls[-2:] == ["up-access-alice", "up-access-alice-2"]
        assert_rate_limited(await initialize(http, jwt))


async def test_refresh_over_the_limit_answers_429_without_upstream_call(
    serve, oauth, proxy
):
    proxy.refresh_limit = FixedWindowCounter(2, clock=fixed_clock)
    flow = {}
    async with serve() as http:
        await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
        await refreshed(http, flow)
        await refreshed(http, flow)
        requests = len(oauth.token_requests)
        response = await refresh(http, flow)
    assert_rate_limited(response)
    assert len(oauth.token_requests) == requests


async def test_refresh_rotates_the_refresh_token(serve, oauth):
    flow = {}
    async with serve() as http:
        await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
        old = dict(flow)
        await refreshed(http, flow)
        assert flow["token"]["refresh_token"] != old["token"]["refresh_token"]
        response = await refresh(http, old)
    assert response.status_code == 401
    assert response.json()["error"] == "invalid_grant"


@pytest.fixture
def held_userinfo(monkeypatch):
    """Userinfo that answers only once `release` is set; `active` counts calls in flight."""
    state = {"active": 0, "peak": 0, "release": asyncio.Event()}

    async def handler(request):
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        await state["release"].wait()
        state["active"] -= 1
        return httpx.Response(200, json={"sub": "101", "api_key": "key-alice"})

    transport = httpx.MockTransport(handler)
    monkeypatch.setattr(
        verifier_module,
        "AsyncClient",
        lambda **kwargs: httpx.AsyncClient(transport=transport, **kwargs),
    )
    return state


async def test_userinfo_calls_wait_beyond_the_concurrency_cap(held_userinfo):
    verifier = UserinfoVerifier(UPSTREAM_URL)
    calls = [
        asyncio.create_task(verifier.verify_token("up-access-alice"))
        for _ in range(USERINFO_CONCURRENCY + 1)
    ]
    await asyncio.sleep(0.05)
    assert held_userinfo["active"] == USERINFO_CONCURRENCY

    held_userinfo["release"].set()
    results = await asyncio.gather(*calls)
    assert all(result is not None for result in results)
    assert held_userinfo["peak"] == USERINFO_CONCURRENCY


async def test_userinfo_call_that_cannot_start_in_time_gives_up(
    held_userinfo, monkeypatch
):
    monkeypatch.setattr(verifier_module, "USERINFO_QUEUE_SECONDS", 0.05)
    verifier = UserinfoVerifier(UPSTREAM_URL)
    held = [
        asyncio.create_task(verifier.verify_token("up-access-alice"))
        for _ in range(USERINFO_CONCURRENCY)
    ]
    await asyncio.sleep(0.01)
    assert await verifier.verify_token("up-access-alice") is None

    held_userinfo["release"].set()
    assert all(result is not None for result in await asyncio.gather(*held))
