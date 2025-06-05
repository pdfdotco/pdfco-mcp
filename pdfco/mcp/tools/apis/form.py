from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import get_pdf_form_fields_info, fill_pdf_form_fields
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field


@mcp.tool()
async def read_pdf_forms_info(
    url: str = Field(description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    password: str = Field(description="Password of PDF file. (Optional)", default=""),
    api_key: str = Field(description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)", default=None),
) -> BaseResponse:
    """
    Extracts information about fillable PDF fields from an input PDF file.
    Ref: https://developer.pdf.co/api-reference/forms/info-reader.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        password=password,
    )
    
    return await get_pdf_form_fields_info(params, api_key=api_key)

@mcp.tool(name="fill_forms")
async def fill_pdf_forms(
    url: str = Field(description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    fields: list = Field(description="List of fields to fill. Each field is a dict with 'fieldName', 'pages', and 'text' properties."),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    api_key: str = Field(description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)", default=None),
) -> BaseResponse:
    """
    Fill existing form fields in a PDF document.

    Example fields format:
    [
        {
            "fieldName": "field_name_from_form_info",
            "pages": "1",
            "text": "Value to fill"
        }
    ]

    Use 'read_pdf_forms_info' first to get the fieldName values of the form.
    
    Ref: https://developer.pdf.co/api-reference/pdf-add#create-fillable-pdf-forms.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        name=name,
    )
    
    return await fill_pdf_form_fields(params, fields=fields, api_key=api_key)

@mcp.tool(name="create_fillable_forms")
async def create_fillable_forms(
    url: str = Field(description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    annotations: list = Field(description="List of form annotations to create. Each annotation can be a textfield or checkbox with properties like 'x', 'y', 'size', 'pages', 'type', and 'id'."),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    api_key: str = Field(description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)", default=None),
) -> BaseResponse:
    """
    Create new fillable form elements in a PDF document.

    Example annotations format:
    [
        {
            "text": "prefilled text",
            "x": 10,
            "y": 30,
            "size": 12,
            "pages": "0-",
            "type": "TextField",
            "id": "textfield1"
        },
        {
            "x": 100,
            "y": 150,
            "size": 12,
            "pages": "0-",
            "type": "Checkbox",
            "id": "checkbox1"
        }
    ]

    Ref: https://developer.pdf.co/api-reference/pdf-add#create-fillable-pdf-forms.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        name=name,
    )
    
    return await fill_pdf_form_fields(params, annotations=annotations, api_key=api_key) 
