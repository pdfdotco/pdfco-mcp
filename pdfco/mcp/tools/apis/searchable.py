from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import make_pdf_searchable, make_pdf_unsearchable
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field


@mcp.tool()
async def pdf_make_searchable(
    url: str = Field(
        description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."
    ),
    httpusername: str = Field(
        description="HTTP auth user name if required to access source url. (Optional)",
        default="",
    ),
    httppassword: str = Field(
        description="HTTP auth password if required to access source url. (Optional)",
        default="",
    ),
    lang: str = Field(
        description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')",
        default="eng",
    ),
    pages: str = Field(
        description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)",
        default="",
    ),
    password: str = Field(
        description="Password of the PDF file. (Optional)", default=""
    ),
    name: str = Field(
        description="File name for the generated output. (Optional)", default=""
    ),
    api_key: str = Field(
        description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)",
        default="",
    ),
) -> BaseResponse:
    """
    Convert scanned PDF documents or image files into a text-searchable PDF.
    Runs OCR and adds an invisible text layer that can be used for text search.
    Ref: https://developer.pdf.co/api-reference/pdf-change-text-searchable/searchable.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        lang=lang,
        pages=pages,
        password=password,
        name=name,
    )

    return await make_pdf_searchable(params, api_key=api_key)


@mcp.tool()
async def pdf_make_unsearchable(
    url: str = Field(
        description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."
    ),
    httpusername: str = Field(
        description="HTTP auth user name if required to access source url. (Optional)",
        default="",
    ),
    httppassword: str = Field(
        description="HTTP auth password if required to access source url. (Optional)",
        default="",
    ),
    pages: str = Field(
        description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)",
        default="",
    ),
    password: str = Field(
        description="Password of the PDF file. (Optional)", default=""
    ),
    name: str = Field(
        description="File name for the generated output. (Optional)", default=""
    ),
    api_key: str = Field(
        description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)",
        default="",
    ),
) -> BaseResponse:
    """
    Make existing PDF document non-searchable by removing the text layer from it.
    Ref: https://developer.pdf.co/api-reference/pdf-change-text-searchable/unsearchable.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        pages=pages,
        password=password,
        name=name,
    )

    return await make_pdf_unsearchable(params, api_key=api_key)
