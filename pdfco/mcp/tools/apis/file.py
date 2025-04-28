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

@mcp.tool()
async def download_file(
    url: str = Field(description="The URL of the file to get, must start with https://pdf-temp-files.s3.amazonaws.com"), 
    path: str = Field(description="The absolute path to save the file to"),
) -> BaseResponse:
    """
    Download a file from the PDF.co API
    """
    try:
        if not url.startswith("https://pdf-temp-files.s3.") and not url.startswith("https://pdf-temp-files-stage.s3."):
            raise ValueError("URL must start with https://pdf-temp-files.s3.us-west-2.amazonaws.com")
        async with PDFCoClient() as client:
            response = await client.get(url)
            if response.headers.get("Content-Type", "").startswith("application/json"):
                json_data = response.json()
                paths = []
                if isinstance(json_data, list) and len(json_data) > 0:
                    target = Path(path)
                    target_dir = target.parent
                    for idx, item in enumerate(json_data):
                        target_path = target_dir / f'{target.stem}_{idx}.{target.suffix}'
                        await download_file(item, target_path)
                        paths.append(str(target_path))
                return BaseResponse(
                    status="success",
                    content={
                        "paths": paths,
                    },
                    tips=f"Result files saved to {paths}",
                )
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

@mcp.tool()
async def read_html(
    file_path: str = Field(description="The absolute path to the HTML file to read"),
    encoding: str = Field(description="The encoding of the HTML file. (Optional)", default="utf-8"),
) -> BaseResponse:
    """
    Read local HTML file before converting to PDF.
    """
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        return BaseResponse(
            status="error",
            content=f"File not found: {path}",
        )
    if path.suffix.lower() != ".html":
        return BaseResponse(
            status="error",
            content=f"File is not an HTML file: {path}",
        )
    return path.read_text(encoding=encoding)