from contextlib import asynccontextmanager
from httpx import AsyncClient
import os, sys
from typing import AsyncGenerator
import importlib.metadata

__BASE_URL = "https://api.pdf.co"
X_API_KEY = os.getenv("X_API_KEY")  

__version__ = importlib.metadata.version('pdfco-mcp')
print(f"pdfco-mcp version: {__version__}", file=sys.stderr)

@asynccontextmanager
async def PDFCoClient() -> AsyncGenerator[AsyncClient, None]:
    if not X_API_KEY:
        raise ValueError("""X_API_KEY is not set. Please set X_API_KEY in the environment variables in your MCP server. 
        To get the API key please sign up at https://pdf.co and you can get the API key from the dashboard.
        ex) .cursor/mcp.json
        ```json
        {
            "mcpServers": {
                "pdfco": {
                    "command": "uvx",
                    "args": [
                        "pdfco-mcp"
                    ],
                    "env": {
                        "X_API_KEY": "YOUR_API_KEY"
                    }
                }
            }
        }
        ```
        """)
    
    client = AsyncClient(
            base_url=__BASE_URL,
            headers={
                "x-api-key": X_API_KEY,
                "User-Agent": f"pdfco-mcp/{__version__}",
            },
        )
    try:
        yield client
    finally:
        await client.aclose()
