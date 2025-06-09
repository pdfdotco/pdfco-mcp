from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import get_pdf_info
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field


@mcp.tool()
async def pdf_info_reader(
    url: str = Field(
        description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."
    ),
    httpusername: str = Field(
        description="HTTP auth user name if required to access source url. (Optional)",
        default="",
    ),
    httppassword: str = Field(
        description="HTTP auth password if required to access source url. (Optional)",
        default="",
    ),
    password: str = Field(
        description="Password of the PDF file. (Optional)", default=""
    ),
    api_key: str = Field(
        description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)",
        default=None,
    ),
) -> BaseResponse:
    """
    Get detailed information about a PDF document - number of pages, metadata, security, form fields, and more.
    Ref: https://developer.pdf.co/api-reference/pdf-info-reader.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        password=password,
    )

    return await get_pdf_info(params, api_key=api_key)
