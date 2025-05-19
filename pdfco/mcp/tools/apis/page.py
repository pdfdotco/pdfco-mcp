from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import delete_pdf_pages, rotate_pdf_pages, auto_rotate_pdf_pages
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field


@mcp.tool()
async def pdf_delete_pages(
    url: str = Field(description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    pages: str = Field(description="Comma-separated list of page indices (or ranges) to delete. Example: '0,2-5,7-'. The first-page index is 0. Use '!' for inverted page numbers (e.g., '!0' for the last page)."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Deletes selected pages inside a PDF file.
    Ref: https://developer.pdf.co/api/pdf-delete-pages/index.html
    """
    params = ConversionParams(
        url=url,
        pages=pages,
        httpusername=httpusername,
        httppassword=httppassword,
        name=name,
    )
    
    return await delete_pdf_pages(params)


@mcp.tool()
async def pdf_rotate_pages(
    url: str = Field(description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    angle: str = Field(description="Angle in degrees. Supported values are 90, 180, and 270. If not specified, pages will be automatically rotated based on content orientation.", default=""),
    pages: str = Field(description="Comma-separated list of page indices (or ranges) to rotate. Example: '0,2-5,7-'. The first-page index is 0. Use '!' for inverted page numbers (e.g., '!0' for the last page). (Optional)", default=""),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Rotates pages in a PDF file. 
    - When angle is specified: Rotates by the specified angle (90, 180, or 270 degrees)
    - When angle is omitted: Automatically detects and corrects page orientation
    
    Ref: https://developer.pdf.co/api/pdf-rotate-pages/index.html
    """
    params = ConversionParams(
        url=url,
        pages=pages,
        httpusername=httpusername,
        httppassword=httppassword,
        password=password,
        name=name,
    )
    
    if angle:
        return await rotate_pdf_pages(params, angle)
    else:
        return await auto_rotate_pdf_pages(params) 