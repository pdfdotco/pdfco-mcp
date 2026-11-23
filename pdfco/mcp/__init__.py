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


def run_hosted(port: int):
    # Imported here so local stdio use never loads the hosted modules.
    import uvicorn

    from pdfco.mcp.hosted.app import build_hosted_app
    from pdfco.mcp.hosted.settings import HostedSettings

    app = build_hosted_app(HostedSettings.from_env())
    uvicorn.run(app, host="0.0.0.0", port=port)


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
    elif transport == "hosted":
        run_hosted(int(args[1]) if len(args) > 1 else 8000)
    else:
        raise ValueError(f"Invalid transport: {transport}")


if __name__ == "__main__":
    main()
