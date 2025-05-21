from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import parse_invoice, parse_document, extract_pdf_attachments
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
async def document_parser(
    url: str = Field(description="URL to the source file (PDF, JPG, PNG)."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    template_id: str = Field(description="ID of the document parser template to use. (Optional)", default=""),
    template_code: str = Field(description="Document parser template code (YAML or JSON) to use directly. (Optional)", default=""),
    output_format: str = Field(description="Output format for the parsed data. Can be JSON, CSV, or XML.", default="JSON"),
    password: str = Field(description="Password of the PDF file if it's protected. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Processes all pages if not specified. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Extracts data from documents based on a document parser extraction template.
    Ref: https://developer.pdf.co/api/document-parser/index.html
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername if httpusername else None,
        httppassword=httppassword if httppassword else None,
        password=password if password else None,
        pages=pages if pages else None,
        name=name if name else None,
        templateId=template_id if template_id else None, # templateId goes into ConversionParams
    )

    custom_payload = {
        "outputFormat": output_format,
    }

    if template_code:
        custom_payload["template"] = template_code # template code itself
        
    return await parse_document(params, custom_payload=custom_payload)


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
