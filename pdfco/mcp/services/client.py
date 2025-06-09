from contextlib import asynccontextmanager
from httpx import AsyncClient
import os
import sys
from typing import AsyncGenerator
import importlib.metadata

__BASE_URL = "https://api.pdf.co"
X_API_KEY = os.getenv("X_API_KEY")

__version__ = importlib.metadata.version("pdfco-mcp")
print(f"pdfco-mcp version: {__version__}", file=sys.stderr)


@asynccontextmanager
async def PDFCoClient(api_key: str = None) -> AsyncGenerator[AsyncClient, None]:
    # Use provided API key, fall back to environment variable
    x_api_key = api_key or X_API_KEY

    if not x_api_key:
        raise ValueError("""API key is required. Please provide an API key as a parameter or set X_API_KEY in the environment variables.
        
        To get the API key:
        1. Sign up at https://pdf.co
        2. Get the API key from the dashboard
        3. Either set it as an environment variable or provide it as a parameter
        
        Environment variable setup example (.cursor/mcp.json):
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
        
        Or provide the API key as a parameter when calling the tool.
        """)

    client = AsyncClient(
        base_url=__BASE_URL,
        headers={
            "x-api-key": x_api_key,
            "User-Agent": f"pdfco-mcp/{__version__}",
        },
    )
    try:
        yield client
    finally:
        await client.aclose()
