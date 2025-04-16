from mcp_server import mcp, base_url
from models import BaseResponse
from httpx import AsyncClient

@mcp.tool()
async def upload_file(file_path: str, x_api_key: str) -> BaseResponse:
    """
    Upload a file to the PDF.co API
    Args:
        file_path: The path to the file to upload
        x_api_key: The API key to use for the upload
    Returns:
        The response from the PDF.co API
    """
    with open(file_path, "rb") as file:
        async with AsyncClient() as client:
            response = await client.post(f"{base_url}/v1/file/upload", files={
                "file": file,
                "async": "true",
            }, headers={
                "x-api-key": x_api_key,
                "Content-Type": "multipart/form-data",
            })
    return response.json()
