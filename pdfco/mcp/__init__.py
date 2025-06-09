import sys
from pdfco.mcp.server import mcp
from pdfco.mcp.tools.apis import (
    conversion,
    job,
    file,
    modification,
    form,
    search,
    searchable,
    security,
    document,
    extraction,
    editing,
)


def main():
    if len(sys.argv) > 1:
        transport = sys.argv[1]
        if transport == "stdio":
            mcp.run(transport=transport)
        elif transport == "sse":
            if len(sys.argv) < 2:
                raise ValueError("SSE transport requires a port number")
            port = int(sys.argv[2])
            mcp.run(transport=transport, host="0.0.0.0", port=port)
        elif transport == "streamable-http":
            if len(sys.argv) < 3:
                raise ValueError(
                    "Streamable HTTP transport requires a port number and path"
                )
            port = int(sys.argv[2])
            path = sys.argv[3]
            mcp.run(transport=transport, host="0.0.0.0", port=port, path=path)
        else:
            raise ValueError(f"Invalid transport: {transport}")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
