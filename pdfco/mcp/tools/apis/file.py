from pathlib import Path
from pdfco.mcp.server import mcp
from pdfco.mcp.services.client import PDFCoClient
from pdfco.mcp.models import BaseResponse

from pydantic import Field

@mcp.tool()
async def upload_file(
    file_path: str = Field(description="The absolute path to the file to upload"), 
) -> BaseResponse:
    """
    Upload a file to the PDF.co API
    """
    try:
        async with PDFCoClient() as client:
            response = await client.post(
                "/v1/file/upload", 
                files={
                "file": open(file_path, "rb"),
            })
            res = response.json()
            return BaseResponse(
                status='success' if res["status"] == 200 else 'error',
                content=res,
                tips=f"You can use the url {res['url']} to access the file",
            )
    except Exception as e:
        return BaseResponse(
            status="error",
            content=str(e),
        )
