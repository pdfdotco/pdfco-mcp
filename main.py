import mcp_server

mcp = mcp_server.mcp
from tools import openapi # file, pdf, job, 

if __name__ == "__main__":
    mcp.run(transport="stdio")
