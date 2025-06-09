from pathlib import Path
from pdfco.mcp.server import mcp
from pdfco.mcp.services.client import PDFCoClient
from pdfco.mcp.models import BaseResponse

from pydantic import Field

@mcp.tool()
async def upload_file(
    file_path: str = Field(description="The absolute path to the file to upload"),
    api_key: str = Field(description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)", default=None)
) -> BaseResponse:
    """
    Upload a file to the PDF.co API
    """
    try:
        async with PDFCoClient(api_key=api_key) as client:
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
