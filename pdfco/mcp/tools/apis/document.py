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
    profiles: str = Field(
        description="JSON string with extra engine options for this endpoint, e.g. '{\"CheckPermissions\": false}'. See https://developer.pdf.co/api/profiles for the options each endpoint supports. (Optional)",
        default="",
    ),
    expiration: int | None = Field(
        description="Lifetime of the output link in minutes; the output file is deleted afterwards. API default is 60; the maximum depends on the plan. (Optional)",
        default=None,
    ),
    api_key: str = Field(
        description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)",
        default="",
    ),
) -> BaseResponse:
    """
    Get detailed information about a PDF document - number of pages, metadata, security, form fields, and more.
    Ref: https://developer.pdf.co/api/pdf-info-reader.md
    """
    params = ConversionParams(
        profiles=profiles,
        expiration=expiration,
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        password=password,
    )

    return await get_pdf_info(params, api_key=api_key)
