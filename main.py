import mcp_server
from tools import key

mcp = mcp_server.mcp
from tools.apis import conversion, file
from tools import key

if __name__ == "__main__":
    mcp.run(transport="stdio")
