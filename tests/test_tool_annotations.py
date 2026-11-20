from fastmcp import Client

from pdfco.mcp import mcp

READ_ONLY_TOOLS = {
    "get_job_check",
    "wait_job_completion",
    "pdf_info_reader",
    "read_pdf_forms_info",
    "find_text",
    "find_table",
}


async def list_tools():
    async with Client(mcp) as client:
        return await client.list_tools()


async def test_every_tool_has_a_title_and_a_read_only_hint():
    tools = await list_tools()
    assert len(tools) == 40
    for tool in tools:
        assert tool.title, tool.name
        assert tool.annotations is not None, tool.name
        assert tool.annotations.read_only_hint is not None, tool.name


async def test_read_only_tools_return_data_without_creating_files():
    tools = await list_tools()
    read_only = {t.name for t in tools if t.annotations.read_only_hint}
    assert read_only == READ_ONLY_TOOLS


async def test_write_tools_are_additive_not_destructive():
    tools = await list_tools()
    for tool in tools:
        if not tool.annotations.read_only_hint:
            assert tool.annotations.destructive_hint is False, tool.name
