from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import parse_invoice, extract_pdf_attachments
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field


@mcp.tool()
async def ai_invoice_parser(
    url: str = Field(
        description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."
    ),
    api_key: str = Field(
        description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)",
        default="",
    ),
) -> BaseResponse:
    """
    AI Invoice Parser: Extracts data from invoices using AI.
    Ref: https://developer.pdf.co/api/ai-invoice-parser.md
    """

    params = ConversionParams(
        url=url,
    )

    return await parse_invoice(params, api_key=api_key)


@mcp.tool()
async def extract_attachments(
    url: str = Field(description="URL to the source PDF file."),
    httpusername: str = Field(
        description="HTTP auth user name if required to access source url. (Optional)",
        default="",
    ),
    httppassword: str = Field(
        description="HTTP auth password if required to access source url. (Optional)",
        default="",
    ),
    password: str = Field(description="Password of PDF file. (Optional)", default=""),
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
    Extracts attachments from a source PDF file.
    Ref: https://developer.pdf.co/api/pdf-extract-attachments.md
    """
    params = ConversionParams(
        profiles=profiles,
        expiration=expiration,
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        password=password,
    )
    return await extract_pdf_attachments(params, api_key=api_key)
