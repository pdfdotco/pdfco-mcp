from mcp_server import mcp, base_url
from models import AsyncRequestResponse
from httpx import AsyncClient

@mcp.tool()
async def url_to_pdf(url: str, x_api_key: str) -> AsyncRequestResponse:
    """
    Convert a URL to a PDF
    Args:
        url: The URL to convert to a PDF
        x_api_key: The API key to use for the conversion
    Returns:
        The response from the PDF.co API
    """
    async with AsyncClient() as client:
        response = await client.post(f"{base_url}/v1/pdf/convert/from/url", json={
            "url": url,
            "async": "true",
        }, headers={
            "x-api-key": x_api_key,
        })
    return response.json()

@mcp.tool()
async def pdf_to_text(url: str, x_api_key: str) -> AsyncRequestResponse:
    """
    Convert a PDF to text
    Args:
        url: The URL to convert to text
        x_api_key: The API key to use for the conversion
    """
    async with AsyncClient() as client:
        response = await client.post(f"{base_url}/v1/pdf/convert/to/text", json={
            "url": url,
            "async": "true",
        }, headers={
            "x-api-key": x_api_key,
        })
    return response.json()
