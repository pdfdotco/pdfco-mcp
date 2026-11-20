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
    args = sys.argv[1:]
    transport = args[0] if args else "stdio"
    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport in ("sse", "streamable-http"):
        if len(args) < 2:
            raise ValueError(f"{transport} transport requires a port number")
        options = {"host": "0.0.0.0", "port": int(args[1])}
        if len(args) > 2:
            options["path"] = args[2]
        mcp.run(transport=transport, **options)
    else:
        raise ValueError(f"Invalid transport: {transport}")


if __name__ == "__main__":
    main()
