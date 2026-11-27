"""Hosted mode: 401 only for a rejected token, 503 when the account service is down."""

import asyncio

import httpx
import httpx2
import pytest

from pdfco.mcp.hosted.app import UPSTREAM_TIMEOUT_SECONDS, build_auth
from pdfco.mcp.hosted.middleware import log_token_error_response
from pdfco.mcp.hosted.verifier import USERINFO_TIMEOUT_SECONDS

from .flow import INITIALIZE, MCP_HEADERS, SETTINGS, sign_in


async def initialize(http, jwt: str) -> httpx.Response:
    return await http.post(
        "/mcp",
        json=INITIALIZE,
        headers={**MCP_HEADERS, "Authorization": f"Bearer {jwt}"},
    )


def assert_unavailable(response: httpx.Response):
    assert response.status_code == 503, response.text
    assert response.headers["retry-after"] == "30"
    assert "www-authenticate" not in response.headers
    assert response.json()["error"] == "temporarily_unavailable"


@pytest.mark.parametrize(
    "outage",
    [
        {"userinfo_status": 500},
        {"userinfo_status": 502},
        {"userinfo_status": 429},
        {"userinfo_status": 400},
        {"userinfo_error": httpx.ConnectError("refused")},
        {"userinfo_error": httpx.ReadTimeout("slow")},
        {"userinfo_raw": "<html>maintenance</html>"},
        {"userinfo_raw": '{"name": "no sub"}'},
    ],
    ids=["500", "502", "429", "400", "connect", "timeout", "html", "no-sub"],
)
async def test_userinfo_without_a_verdict_answers_503(serve, oauth, api, outage):
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        for name, value in outage.items():
            setattr(oauth, name, value)
        response = await initialize(http, jwt)
    assert_unavailable(response)
    assert api.requests == []


@pytest.mark.parametrize("status", [401, 403, 404])
async def test_userinfo_verdict_on_the_token_stays_401(serve, oauth, status):
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        oauth.userinfo_status = status
        response = await initialize(http, jwt)
    assert response.status_code == 401
    assert "www-authenticate" in response.headers


async def test_first_request_after_recovery_succeeds(serve, oauth):
    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        oauth.userinfo_status = 500
        assert (await initialize(http, jwt)).status_code == 503
        oauth.userinfo_status = 200
        assert (await initialize(http, jwt)).status_code == 200


async def test_mark_never_reaches_another_request(serve, oauth):
    async with serve() as http:
        alice = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        bob = await sign_in(http, oauth.add_user("bob", "202", "key-bob"))
        oauth.broken_users.add("alice")

        sequential = [await initialize(http, jwt) for jwt in [alice, bob] * 30]
        concurrent = await asyncio.gather(
            *(initialize(http, jwt) for jwt in [alice, bob] * 30)
        )

    for responses in (sequential, concurrent):
        assert [r.status_code for r in responses] == [503, 200] * 30


async def refresh(http, flow: dict) -> httpx.Response:
    return await http.post(
        "/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": flow["token"]["refresh_token"],
            "client_id": flow["client_id"],
        },
    )


def raise_(error):
    def failure():
        raise error

    return failure


@pytest.mark.parametrize(
    "failure",
    [
        lambda: httpx2.Response(500, text="boom"),
        lambda: httpx2.Response(503, text="maintenance"),
        raise_(httpx2.ConnectError("refused")),
        raise_(httpx2.ReadTimeout("slow")),
        lambda: httpx2.Response(429, text="<html>slow down</html>"),
        lambda: httpx2.Response(
            403, text="<html>blocked</html>", headers={"content-type": "text/html"}
        ),
    ],
    ids=["500", "503", "connect", "timeout", "html-429", "html-403"],
)
async def test_refresh_without_a_verdict_answers_503(serve, oauth, failure):
    flow = {}
    async with serve() as http:
        await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
        oauth.token_failure = failure
        response = await refresh(http, flow)
    assert_unavailable(response)


def non_json_records(caplog):
    return [r for r in caplog.records if r.message.endswith(", not JSON")]


async def test_refresh_blocked_by_a_waf_logs_non_json_at_error(serve, oauth, caplog):
    flow = {}
    async with serve() as http:
        await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
        oauth.token_failure = lambda: httpx2.Response(
            403, text="<html>blocked</html>", headers={"content-type": "text/html"}
        )
        response = await refresh(http, flow)
    assert_unavailable(response)
    non_json = non_json_records(caplog)
    assert [r.levelname for r in non_json] == ["ERROR"]
    assert (
        non_json[0].message == "PDF.co token endpoint answered 403 text/html, not JSON"
    )


async def test_refresh_upstream_5xx_stays_a_warning(serve, oauth, caplog):
    flow = {}
    async with serve() as http:
        await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
        oauth.token_failure = lambda: httpx2.Response(502, text="<html>bad</html>")
        response = await refresh(http, flow)
    assert_unavailable(response)
    assert non_json_records(caplog) == []
    assert "PDF.co token endpoint answered 502" in caplog.text


@pytest.mark.parametrize(
    ("status", "error"),
    [
        (401, "invalid_client"),
        (400, "unauthorized_client"),
        (400, "invalid_scope"),
        (400, "invalid_request"),
        (400, "temporarily_unavailable"),
    ],
)
async def test_refresh_rejected_for_our_client_answers_500(
    serve, oauth, caplog, status, error
):
    flow = {}
    async with serve() as http:
        await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
        oauth.token_failure = lambda: httpx2.Response(
            status, json={"error": error, "error_description": "secret detail"}
        )
        response = await refresh(http, flow)
    assert response.status_code == 500, response.text
    assert response.json()["error"] == "server_error"
    assert response.headers["cache-control"] == "no-store"
    assert "retry-after" not in response.headers
    assert "www-authenticate" not in response.headers
    rejected = [r for r in caplog.records if "rejected this server" in r.message]
    assert [r.levelname for r in rejected] == ["ERROR"]
    assert error in rejected[0].message
    assert "secret detail" not in caplog.text
    # A JSON answer is the service's own; it is not logged as non-JSON.
    assert non_json_records(caplog) == []


async def test_refresh_rejected_upstream_stays_invalid_grant(serve, oauth):
    flow = {}
    async with serve() as http:
        await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
        oauth.token_failure = lambda: httpx2.Response(
            400, json={"error": "invalid_grant"}
        )
        response = await refresh(http, flow)
    # fastmcp answers invalid_grant with 401, as the MCP spec asks.
    assert response.status_code == 401
    assert response.json()["error"] == "invalid_grant"


async def test_refresh_works_when_upstream_is_up(serve, oauth):
    flow = {}
    async with serve() as http:
        await sign_in(http, oauth.add_user("alice", "101", "key-alice"), flow)
        response = await refresh(http, flow)
        assert response.status_code == 200, response.text
        assert (
            await initialize(http, response.json()["access_token"])
        ).status_code == 200


async def test_upstream_calls_give_up_after_five_seconds(serve, oauth):
    client = build_auth(SETTINGS)._create_upstream_oauth_client()
    assert UPSTREAM_TIMEOUT_SECONDS == 5.0
    assert client._client.timeout == httpx2.Timeout(UPSTREAM_TIMEOUT_SECONDS)
    # Guards the private attribute the hook is attached through.
    assert client._client.event_hooks["response"] == [log_token_error_response]
    await client.aclose()

    async with serve() as http:
        jwt = await sign_in(http, oauth.add_user("alice", "101", "key-alice"))
        await initialize(http, jwt)
    assert USERINFO_TIMEOUT_SECONDS == 5.0
    assert oauth.userinfo_client_kwargs[-1]["timeout"] == USERINFO_TIMEOUT_SECONDS
