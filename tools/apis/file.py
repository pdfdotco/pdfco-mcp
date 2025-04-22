from mcp_server import mcp, base_url
from models import BaseResponse
from httpx import AsyncClient
from mcp.server.fastmcp import Context

@mcp.tool()
async def upload_file(file_path: str, x_api_key: str, ctx: Context) -> BaseResponse:
    """
    Upload a file to the PDF.co API
    Args:
        file_path: The path to the file to upload
        x_api_key: The API key to use for the upload 
    Returns:
        The response from the PDF.co API
    """
    if ctx:
        await ctx.info(f"Uploading file: {file_path}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            response = await client.post(
                "/v1/file/upload", 
                files={
                "file": open(file_path, "rb"),
            }, headers={
                "x-api-key": x_api_key,
            })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e

@mcp.tool()
async def download_file(url: str, path: str, ctx: Context) -> str:
    """
    Get a result file from the PDF.co API
    Args:
        url: The URL of the file to get, must start with https://pdf-temp-files-stage.s3.us-west-2.amazonaws.com
        path: The path to save the file to
    Returns:
        The path to the file
    """
    if ctx:
        await ctx.info(f"Downloading file: {url}")
    try:
        if not url.startswith("https://pdf-temp-files-stage.s3.us-west-2.amazonaws.com"):
            raise ValueError("URL must start with https://pdf-temp-files-stage.s3.us-west-2.amazonaws.com")
        async with AsyncClient() as client:
            response = await client.get(url)
            with open(path, "wb") as file:
                file.write(response.content)
            return path
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e
