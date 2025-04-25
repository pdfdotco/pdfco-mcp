import mcp_server

mcp = mcp_server.mcp
from tools.apis import conversion, job, file

if __name__ == "__main__":
    mcp.run(transport="stdio")
