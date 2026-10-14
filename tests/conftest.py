import json

import httpx
import pytest
from fastmcp import Client

import pdfco.mcp.services.client as client_module
from pdfco.mcp import mcp  # noqa: F401  (importing registers every tool)
from pdfco.mcp.models import BaseResponse


class FakeAPI:
    """Records every request and answers with a configurable response."""

    def __init__(self):
        self.requests: list[httpx.Request] = []
        self.response = httpx.Response(
            200,
            json={
                "jobId": "JOB123",
                "url": "https://pdf-temp-files.s3.us-west-2.amazonaws.com/out.pdf",
                "status": "working",
                "credits": 2,
                "remainingCredits": 100,
            },
        )

    def respond(
        self, status_code: int, body: dict | None = None, text: str | None = None
    ):
        if text is not None:
            self.response = httpx.Response(status_code, text=text)
        else:
            self.response = httpx.Response(status_code, json=body)

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self.response

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]

    @property
    def last_payload(self) -> dict:
        return json.loads(self.last.content)


@pytest.fixture
def api(monkeypatch) -> FakeAPI:
    fake = FakeAPI()
    transport = httpx.MockTransport(fake.handler)

    def make_client(**kwargs):
        return httpx.AsyncClient(transport=transport, **kwargs)

    monkeypatch.setattr(client_module, "AsyncClient", make_client)
    monkeypatch.setattr(client_module, "X_API_KEY", None)
    return fake


@pytest.fixture
async def call():
    """Invoke a tool the way an MCP client does, and parse the BaseResponse back."""

    async with Client(mcp) as client:

        async def _call(tool_name: str, **arguments) -> BaseResponse:
            result = await client.call_tool(tool_name, arguments)
            # fastmcp < 3 returns a list of content blocks; fastmcp >= 3 wraps it.
            contents = getattr(result, "content", result)
            return BaseResponse.model_validate_json(contents[0].text)

        _call.client = client
        yield _call
