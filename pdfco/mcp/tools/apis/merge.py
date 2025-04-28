from pdfco.mcp.server import mcp
from pdfco.mcp.services.client import PDFCoClient
from pdfco.mcp.models import BaseResponse

from pydantic import Field

@mcp.tool()
async def pdf_to_merge(
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    ) -> BaseResponse:
    """
    Merge PDF from two or more PDF, DOC, XLS, images, even ZIP with documents and images into a new PDF.
    Ref: https://developer.pdf.co/api/pdf-merge/index.html#post-tag-pdf-merge2
    """
    payload = {
        "url": url,
        "async": True,
    }
    
    try:
        async with PDFCoClient() as client:
            response = await client.post(
                "/v1/pdf/merge2", 
                json=payload)
            return BaseResponse(
                status="success",
                content=response.json(),
            )
    except Exception as e:
        return BaseResponse(
            status="error",
            content=str(e),
        )
