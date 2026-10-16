"""Every input a tool advertises must reach the API; none may be dropped."""

import pytest
from pydantic import ValidationError

from pdfco.mcp.models import ConversionParams
from pdfco.mcp.tools.apis import conversion

CONVERSION_TOOL_NAMES = sorted(
    name
    for name, obj in vars(conversion).items()
    if callable(obj) and getattr(obj, "__module__", None) == conversion.__name__
)


def test_conversion_tool_inventory():
    assert len(CONVERSION_TOOL_NAMES) == 20


@pytest.mark.parametrize("tool_name", CONVERSION_TOOL_NAMES)
async def test_call_level_api_key_is_sent(api, call, tool_name):
    tool = next(t for t in await call.client.list_tools() if t.name == tool_name)
    arguments = {
        name: "https://example.com/input.pdf"
        for name in tool.inputSchema.get("required", [])
    }

    result = await call(tool_name, **arguments, api_key="k-test")

    assert result.status == "working", result
    assert api.last.headers["x-api-key"] == "k-test"


async def test_false_booleans_are_sent(api, call):
    await call("html_to_pdf", html="<p>hi</p>", printBackground=False, api_key="k")
    assert api.last_payload["printBackground"] is False

    await call(
        "email_to_pdf",
        url="https://example.com/mail.eml",
        embedAttachments=False,
        convertAttachments=False,
        api_key="k",
    )
    assert api.last_payload["embedAttachments"] is False
    assert api.last_payload["convertAttachments"] is False


async def test_expiration_is_sent(api, call):
    await call(
        "pdf_add_annotations_images_fields",
        url="https://example.com/in.pdf",
        annotations=[{"text": "x", "x": 1, "y": 1}],
        expiration=15,
        api_key="k",
    )
    assert api.last_payload["expiration"] == 15


def test_unknown_field_is_rejected():
    with pytest.raises(ValidationError):
        ConversionParams(url="https://example.com/in.pdf", api_key="k")


def test_payload_omits_unset_and_empty_values():
    payload = ConversionParams(url="https://example.com/in.pdf").parse_payload()
    assert payload == {
        "async": True,
        "url": "https://example.com/in.pdf",
        "lang": "eng",
        "lineGrouping": "0",
    }
