from mcp_server import mcp
from services.client import PDFCoClient
from mcp.server.fastmcp import Context
from models import BaseResponse

@mcp.tool()
async def pdf_to_merge(
    url: str,
    ctx: Context,
    ) -> BaseResponse:
    """
    Merge PDF from two or more PDF, DOC, XLS, images, even ZIP with documents and images into a new PDF.

    Ref: https://developer.pdf.co/api/pdf-merge/index.html#post-tag-pdf-merge2

    Args:
        url: URLs to the source files (comma-separated). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage.
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
        async with PDFCoClient() as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/merge2", 
                json=payload)
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return BaseResponse(
                status="success",
                content=response.json(),
            )
    except Exception as e:
        return BaseResponse(
            status="error",
            content=str(e),
        )
