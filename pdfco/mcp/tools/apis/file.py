from pdfco.mcp.server import mcp
from pdfco.mcp.services.client import PDFCoClient
from pdfco.mcp.models import BaseResponse

from pydantic import Field

@mcp.tool()
async def upload_file(
    file_path: str = Field(description="The path to the file to upload"), 
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

@mcp.tool()
async def download_file(
    url: str = Field(description="The URL of the file to get, must start with https://pdf-temp-files-stage.s3.us-west-2.amazonaws.com"), 
    path: str = Field(description="The path to save the file to"),
) -> BaseResponse:
    """
    Download a file from the PDF.co API
    """
    try:
        if not url.startswith("https://pdf-temp-files-stage.s3.us-west-2.amazonaws.com"):
            raise ValueError("URL must start with https://pdf-temp-files-stage.s3.us-west-2.amazonaws.com")
        async with PDFCoClient() as client:
            response = await client.get(url)
            with open(path, "wb") as file:
                file.write(response.content)
            return BaseResponse(
                status="success",
                content={
                    "path": path,
                },
                tips=f"Result file saved to {path}",
            )
    except Exception as e:
        return BaseResponse(
            status="error",
            content=str(e),
        )
