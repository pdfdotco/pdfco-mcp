from contextlib import asynccontextmanager
from fastmcp.server.dependencies import get_access_token
from httpx import AsyncClient
import os
import sys
from typing import AsyncGenerator
import importlib.metadata

__BASE_URL = "https://api.pdf.co"
X_API_KEY = os.getenv("X_API_KEY")

__version__ = importlib.metadata.version("pdfco-mcp")
print(f"pdfco-mcp version: {__version__}", file=sys.stderr)


def _hosted_api_key() -> str | None:
    """The API key of the authenticated hosted user, or None outside hosted mode.

    In hosted mode the key is only ever the one userinfo returned for this
    request's token. A tool argument or X_API_KEY must never stand in for it,
    because either would let one user act with another user's key.
    """
    access_token = get_access_token()
    if access_token is None:
        return None
    key = access_token.claims.get("api_key")
    if not key:
        raise ValueError(
            "The PDF.co account did not return an API key for this session. "
            "Disconnect and reconnect the PDF.co connector."
        )
    return key


@asynccontextmanager
async def PDFCoClient(api_key: str | None = None) -> AsyncGenerator[AsyncClient, None]:
    user_agent = f"pdfco-mcp/{__version__}"
    hosted_key = _hosted_api_key()
    if hosted_key is not None:
        x_api_key = hosted_key
        user_agent += " (hosted)"
    else:
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
            "User-Agent": user_agent,
        },
    )
    try:
        yield client
    finally:
        await client.aclose()
