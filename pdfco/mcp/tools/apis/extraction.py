from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import parse_invoice, extract_pdf_attachments
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field


@mcp.tool()
async def ai_invoice_parser(
    url: str = Field(description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
) -> BaseResponse:
    """
    AI Invoice Parser: Extracts data from invoices using AI.
    Ref: https://developer.pdf.co/api/ai-invoice-parser/index.html
    """
    
    # Pass arguments directly; ConversionParams now handles Optional[str] with default=None
    params = ConversionParams(
        url=url,
    )
    
    return await parse_invoice(params)


@mcp.tool()
async def extract_attachments(
    url: str = Field(description="URL to the source PDF file."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    password: str = Field(description="Password of PDF file. (Optional)", default=""),
) -> BaseResponse:
    """
    Extracts attachments from a source PDF file.
    Ref: https://developer.pdf.co/api/extract-attachments/index.html
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername if httpusername else None,
        httppassword=httppassword if httppassword else None,
        password=password if password else None,
    )
    return await extract_pdf_attachments(params)
