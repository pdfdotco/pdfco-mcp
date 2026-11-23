"""Every input a tool advertises must reach the API; none may be dropped."""

import pytest
from pydantic import ValidationError

from pdfco.mcp.models import ConversionParams

# Tools whose endpoints take neither `profiles` nor `expiration`.
NON_API_TOOLS = {
    "ai_invoice_parser",
    "upload_file",
    "get_job_check",
    "wait_job_completion",
}
# Background-only endpoints that take `expiration` but not `profiles`.
NO_PROFILES_TOOLS = {"pdf_to_pdfa", "pdf_to_e_invoice", "markdown_to_pdf"}
# Tools with no required input that still need one source to reach the API.
SOURCE_INPUTS = {"markdown_to_pdf": {"url": "https://example.com/input.md"}}
EXPECTED_TOOL_COUNT = 41


def input_schema(tool) -> dict:
    """MCP SDK v2 renamed `inputSchema` to `input_schema`; accept both."""
    return getattr(tool, "input_schema", None) or tool.inputSchema


def dummy_for(schema: dict):
    """A value of the right JSON type for a required parameter."""
    if "enum" in schema:
        return schema["enum"][0]
    kind = schema.get("type")
    if isinstance(kind, list):
        kind = next(k for k in kind if k != "null")
    if kind == "array":
        return [{"text": "x"}]
    if kind == "integer":
        return 1
    if kind == "number":
        return 1.0
    if kind == "boolean":
        return True
    if kind == "object":
        return {}
    return "https://example.com/input.pdf"


async def api_tools(client):
    tools = await client.list_tools()
    assert len(tools) == EXPECTED_TOOL_COUNT
    return [t for t in tools if t.name not in NON_API_TOOLS]


async def test_api_tool_inventory(call):
    assert len(await api_tools(call.client)) == EXPECTED_TOOL_COUNT - len(NON_API_TOOLS)


async def test_shared_inputs_reach_every_api_tool(api, call):
    for tool in await api_tools(call.client):
        props = input_schema(tool).get("properties", {})
        required = {
            name: dummy_for(props[name])
            for name in input_schema(tool).get("required", [])
        }
        required.update(SOURCE_INPUTS.get(tool.name, {}))

        takes_profiles = tool.name not in NO_PROFILES_TOOLS
        if takes_profiles:
            required["profiles"] = '{"TrimSpaces": true}'
        result = await call(tool.name, **required, api_key="k-test", expiration=5)

        assert result.status == "working", (tool.name, result)
        assert api.last.headers["x-api-key"] == "k-test", tool.name
        payload = api.last_payload
        if takes_profiles:
            assert payload["profiles"] == '{"TrimSpaces": true}', tool.name
        assert payload["expiration"] == 5, tool.name


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


async def test_pdfa_sends_only_its_own_inputs(api, call):
    result = await call(
        "pdf_to_pdfa", url="https://example.com/in.pdf", name="out.pdf", api_key="k"
    )
    # The endpoint takes no `async` flag and none of the shared conversion defaults.
    assert api.last.url.path == "/v1/pdf/convert/to/pdfa"
    assert api.last_payload == {"url": "https://example.com/in.pdf", "name": "out.pdf"}
    assert "wait_job_completion" in result.tips
    assert "isCompliant" in result.tips


async def test_e_invoice_sends_xml_profile_and_source_credentials(api, call):
    result = await call(
        "pdf_to_e_invoice",
        url="https://example.com/in.pdf",
        xml_url="https://example.com/invoice.xml",
        profile="zugferd",
        httpusername="user",
        httppassword="pass",
        api_key="k",
    )
    assert api.last.url.path == "/v1/pdf/convert/to/e-invoice"
    assert api.last_payload == {
        "url": "https://example.com/in.pdf",
        "xml_url": "https://example.com/invoice.xml",
        "profile": "zugferd",
        "httpusername": "user",
        "httppassword": "pass",
    }
    assert "validationReportUrl" in result.tips


async def test_e_invoice_rejects_an_unknown_profile(api, call):
    with pytest.raises(Exception):
        await call(
            "pdf_to_e_invoice",
            url="https://example.com/in.pdf",
            xml_url="https://example.com/invoice.xml",
            profile="xrechnung",
            api_key="k",
        )
    assert api.requests == []


async def test_markdown_sends_inline_text_only(api, call):
    result = await call("markdown_to_pdf", markdown="# Title\n\nBody", api_key="k")
    # Background-only: no `async` flag, and empty optional inputs are left out
    # because the endpoint rejects empty strings.
    assert api.last.url.path == "/v1/pdf/convert/from/md"
    assert api.last_payload == {"markdown": "# Title\n\nBody"}
    assert "wait_job_completion" in result.tips
    assert "warnings" in result.tips


async def test_markdown_sends_url_name_and_integer_expiration(api, call):
    await call(
        "markdown_to_pdf",
        url="https://example.com/doc.md",
        name="doc.pdf",
        expiration=120,
        api_key="k",
    )
    assert api.last_payload == {
        "url": "https://example.com/doc.md",
        "name": "doc.pdf",
        "expiration": 120,
    }


@pytest.mark.parametrize(
    "sources",
    [{}, {"markdown": "# Title", "url": "https://example.com/doc.md"}],
    ids=["neither", "both"],
)
async def test_markdown_needs_exactly_one_source(api, call, sources):
    result = await call("markdown_to_pdf", **sources, api_key="k")
    assert result.status == "error"
    assert "exactly one of markdown or url" in result.content
    assert api.requests == []
