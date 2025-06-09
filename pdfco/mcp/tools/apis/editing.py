from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import pdf_add
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field
from typing import List, Any


@mcp.tool()
async def pdf_add_annotations_images_fields(
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
        description="Password for the PDF file. (Optional)", default=""
    ),
    name: str = Field(
        description="File name for the generated output. (Optional)", default=""
    ),
    annotations: List[Any] = Field(
        description="Array of annotation objects to add text, links, shapes, etc. Each object can have: 'text' (string), 'x' (number), 'y' (number), 'size' (number), 'pages' (string), 'color' (string hex), 'link' (string URL), 'fontName' (string), 'fontItalic' (boolean), 'fontBold' (boolean), 'fontStrikeout' (boolean), 'fontUnderline' (boolean). (Optional)",
        default=[],
    ),
    images: List[Any] = Field(
        description="Array of image objects to add images to PDF. Each object can have: 'url' (string), 'x' (number), 'y' (number), 'width' (number), 'height' (number), 'pages' (string). (Optional)",
        default=[],
    ),
    fields: List[Any] = Field(
        description="Array of form field objects to fill PDF form fields. Each object can have: 'fieldName' (string), 'pages' (string), 'text' (string), 'fontName' (string), 'size' (number), 'fontBold' (boolean), 'fontItalic' (boolean), 'fontStrikeout' (boolean), 'fontUnderline' (boolean). (Optional)",
        default=[],
    ),
    expiration: int = Field(
        description="Set the expiration time for the output link in minutes. After this specified duration, any generated output file(s) will be automatically deleted. (Optional)",
        default=60,
    ),
    encrypt: bool = Field(description="Encrypt output file. (Optional)", default=False),
    flatten: bool = Field(
        description="Flatten filled form fields and annotations into PDF content. Set to true to disable editing of filled form fields in the output PDF. (Optional)",
        default=False,
    ),
    api_key: str = Field(
        description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)",
        default=None,
    ),
) -> BaseResponse:
    """
    Add text, images, forms, other PDFs, fill forms, links to external sites and external PDF files. You can update or modify PDF and scanned PDF files.

    This tool supports three main ways to add content:

    1. **annotations**: Add text, links, shapes, etc.
       Properties: text, x, y, size, pages, color, link, fontName, fontItalic, fontBold, fontStrikeout, fontUnderline

    2. **images**: Add images or other PDF content
       Properties: url, x, y, width, height, pages

    3. **fields**: Fill existing form fields
       Properties: fieldName, pages, text, fontName, size, fontBold, fontItalic, fontStrikeout, fontUnderline

    Example annotations:
    [{"text": "Sample Text - Click here to test link", "x": 250, "y": 240, "size": 24, "pages": "0-", "color": "CCBBAA", "link": "https://pdf.co/", "fontName": "Comic Sans MS", "fontItalic": true, "fontBold": true, "fontStrikeout": false, "fontUnderline": true}]

    Example images:
    [{"url": "https://pdfco-test-files.s3.us-west-2.amazonaws.com/pdf-edit/logo.png", "x": 270, "y": 150, "width": 159, "height": 43, "pages": "0"}]

    Example fields:
    [{"fieldName": "topmostSubform[0].Page1[0].YourSocial_ReadOrderControl[0].f1_05[0]", "pages": "1", "text": "Joan B.", "fontName": "Arial", "size": 6, "fontBold": true, "fontItalic": true, "fontStrikeout": true, "fontUnderline": true}]

    Ref: https://developer.pdf.co/api-reference/pdf-add.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        password=password,
        name=name,
        expiration=expiration,
    )

    # Prepare additional parameters
    add_params = {}

    if annotations:
        add_params["annotations"] = annotations
    if images:
        add_params["images"] = images
    if fields:
        add_params["fields"] = fields
    if encrypt:
        add_params["encrypt"] = encrypt
    if flatten:
        add_params["flatten"] = flatten

    return await pdf_add(params, **add_params, api_key=api_key)
