from fastmcp import FastMCP

mcp = FastMCP("pdfco")

# Tool annotations (MCP ToolAnnotations). destructiveHint defaults to true in the
# spec, so tools that only add new files to PDF.co temporary storage set it to
# false explicitly. No tool deletes or overwrites user data.
READ_ONLY = {"readOnlyHint": True}
ADDITIVE_WRITE = {"readOnlyHint": False, "destructiveHint": False}
