from mcp_server import mcp
from services.client import PDFCoClient
from models import BaseResponse, ConversionParams, ImageConversionParams
from pydantic import Field
async def _convert_pdf(endpoint: str, params: ConversionParams) -> BaseResponse:
    """Helper function to handle PDF conversion with common logic"""
    payload = params.parse_payload(async_mode=True)
    try:
        async with PDFCoClient() as client:
            url = f"/v1/pdf/convert/to/{endpoint}"
            response = await client.post(url, json=payload)
            json_data = response.json()
            return BaseResponse(
                status="working",
                content=json_data,
                tips=f"You **should** use the 'job_check' tool to check the status of the job [{json_data['jobId']}] is completed(status: success)",
            )
    except Exception as e:
        return BaseResponse(
            status="error",
            content=str(e),
        )

@mcp.tool()
async def pdf_to_json(
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False),
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default=""),
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng"),
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0"),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert PDF and scanned images into JSON representation with text, fonts, images, vectors, and formatting preserved using the /pdf/convert/to/json2 endpoint.
    Ref: https://developer.pdf.co/api/pdf-to-json/index.html#post-tag-pdf-to-json2
    """
    return await _convert_pdf("json2", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

@mcp.tool()
async def pdf_to_csv(
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False),
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default=""),
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng"),
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0"),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert PDF and scanned images into CSV representation with layout, columns, rows, and tables.
    Ref: https://developer.pdf.co/api/pdf-to-csv/index.html
    """
    return await _convert_pdf("csv", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

@mcp.tool()
async def pdf_to_text(
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False),
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default=""),
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng"),
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0"),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert PDF and scanned images to text with layout preserved.
    Ref: https://developer.pdf.co/api/pdf-to-text/index.html
    """
    return await _convert_pdf("text", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

@mcp.tool()
async def pdf_to_xls(
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False),
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default=""),
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng"),
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0"),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert PDF and scanned images to XLS (Excel 97-2003) format.
    Ref: https://developer.pdf.co/api/pdf-to-excel/index.html
    """
    return await _convert_pdf("xls", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

@mcp.tool()
async def pdf_to_xlsx(
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False),
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default=""),
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng"),
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0"),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert PDF and scanned images to XLSX (Excel 2007+) format.        
    Ref: https://developer.pdf.co/api/pdf-to-excel/index.html
    """
    return await _convert_pdf("xlsx", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

@mcp.tool()
async def pdf_to_xml(
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False),
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default=""),
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng"),
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0"),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert PDF and scanned images to XML format.
    Ref: https://developer.pdf.co/api/pdf-to-xml/index.html
    """
    return await _convert_pdf("xml", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

@mcp.tool()
async def pdf_to_html(
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False),
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default=""),
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng"),
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0"),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert PDF and scanned images to HTML format.
    Ref: https://developer.pdf.co/api/pdf-to-html/index.html
    """
    return await _convert_pdf("html", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

@mcp.tool()
async def pdf_to_image(
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False),
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default=""),
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng"),
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0"),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    type: str = Field(description="Type of image to convert to. (jpg, png, webp, tiff) (Optional)", default="jpg", choices=["jpg", "png", "webp", "tiff"]),
) -> BaseResponse:
    """
    Convert PDF and scanned images to various image formats (JPG, PNG, WebP, TIFF).
    Ref: https://developer.pdf.co/api/pdf-to-image/index.html
    """
    return await _convert_pdf(type, ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))
