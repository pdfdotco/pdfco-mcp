"""A hosted server wired to the fakes in flow.py, run in-process."""

from contextlib import asynccontextmanager

import httpx
import httpx2
import pytest
from key_value.aio.stores.memory import MemoryStore

import pdfco.mcp.hosted.verifier as verifier_module
from pdfco.mcp.hosted.app import build_auth, build_hosted_server, build_http_app

from .flow import BASE_URL, SETTINGS, FakeOAuth


@pytest.fixture
def oauth(monkeypatch) -> FakeOAuth:
    fake = FakeOAuth()
    userinfo_transport = httpx.MockTransport(fake.userinfo_handler)
    monkeypatch.setattr(
        verifier_module,
        "AsyncClient",
        lambda **kwargs: (
            fake.userinfo_client_kwargs.append(kwargs)
            or httpx.AsyncClient(transport=userinfo_transport, **kwargs)
        ),
    )
    return fake


@pytest.fixture
def store() -> MemoryStore:
    return MemoryStore()


@pytest.fixture
def proxy(oauth, store):
    auth = build_auth(SETTINGS, client_storage=store)
    token_transport = httpx2.MockTransport(oauth.token_handler)
    original = auth._create_upstream_oauth_client

    def create_client():
        client = original()
        client._client = httpx2.AsyncClient(
            transport=token_transport, event_hooks=client._client.event_hooks
        )
        return client

    auth._create_upstream_oauth_client = create_client
    return auth


@pytest.fixture
def serve(proxy, api):
    """`async with serve() as http:` runs the hosted app in-process.

    The app's lifespan has to start and stop in the same task, which an async
    fixture does not guarantee, so each test enters it itself.
    """

    @asynccontextmanager
    async def _serve():
        app = build_http_app(build_hosted_server(proxy))
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url=BASE_URL
            ) as http:
                http.app = app
                yield http

    return _serve
