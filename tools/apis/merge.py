from mcp_server import mcp, base_url
from httpx import AsyncClient
from mcp.server.fastmcp import Context

@mcp.tool()
async def pdf_to_merge(
    url: str,
    x_api_key: str,
    ctx: Context,
    ) -> dict:
    """
    Merge PDF from two or more PDF, DOC, XLS, images, even ZIP with documents and images into a new PDF.

    Ref: https://developer.pdf.co/api/pdf-merge/index.html#post-tag-pdf-merge2

    Args:
        url: URLs to the source files (comma-separated). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage.
        x_api_key: The API key.

    Returns:
        The response from the PDF.co API.
    """
    if ctx:
        await ctx.info(f"Merging PDFs: {url}")
    
    payload = {
        "url": url,
        "async": True,
    }
    
    if ctx:
        await ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/merge2", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e
