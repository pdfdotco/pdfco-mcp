from mcp_server import mcp
import os

@mcp.tool()
async def get_key_from_env() -> str:
    """
    Try to get the key from the environment variable
    
    Returns:
        The API key (x_api_key)
    """
    return os.getenv("X_API_KEY")
    