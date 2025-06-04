from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import convert_to, convert_from
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field
    

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
    return await convert_to("pdf", "json2", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

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
    return await convert_to("pdf", "csv", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

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
    return await convert_to("pdf", "text", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

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
    return await convert_to("pdf", "xls", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

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
    return await convert_to("pdf", "xlsx", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

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
    return await convert_to("pdf", "xml", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

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
    return await convert_to("pdf", "html", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

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
    return await convert_to("pdf", type, ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, unwrap=unwrap, rect=rect, lang=lang, line_grouping=line_grouping, password=password, name=name))

@mcp.tool()
async def document_to_pdf(
    url: str = Field(description="URL to the source file (DOC, DOCX, RTF, TXT, XPS). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    autosize: bool = Field(description="Controls automatic page sizing. If true, page dimensions adjust to content. If false, uses worksheet’s page setup. (Optional)", default=False),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert various document types (DOC, DOCX, RTF, TXT, XLS, XLSX, CSV, HTML, JPG, PNG, TIFF, WEBP) into PDF.
    Ref: https://developer.pdf.co/api/pdf-from-document/index.html#post-pdf-convert-from-doc
    """
    return await convert_from("pdf", "doc", ConversionParams(url=url, autosize=autosize, httpusername=httpusername, httppassword=httppassword, pages=pages, name=name))

@mcp.tool()
async def csv_to_pdf(
    url: str = Field(description="URL to the source file (CSV, XLS, XLSX). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    autosize: bool = Field(description="Controls automatic page sizing. If true, page dimensions adjust to content. If false, uses worksheet’s page setup. (Optional)", default=False),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert CSV or spreadsheet files (XLS, XLSX) to PDF.
    Ref: https://developer.pdf.co/api/pdf-from-document/index.html#post-tag-pdf-convert-from-csv
    """
    return await convert_from("pdf", "csv", ConversionParams(url=url, autosize=autosize, httpusername=httpusername, httppassword=httppassword, pages=pages, name=name))

@mcp.tool()
async def image_to_pdf(
    url: str = Field(description="URL to the source file (JPG, PNG, TIFF). Multiple files are supported (by providing a comma-separated list of URLs). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert various image formats (JPG, PNG, TIFF) to PDF.
    Ref: https://developer.pdf.co/api/pdf-from-image/index.html
    ```
    """
    return await convert_from("pdf", "image", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, pages=pages, name=name))

@mcp.tool()
async def webpage_to_pdf(
    url: str = Field(description="URL to the source file (external webpage URL)."),
    margins: str = Field(description="Set to CSS style margins like 10px, 5mm, 5in for all sides or 5px 5px 5px 5px (the order of margins is top, right, bottom, left). (Optional)", default=""),
    paperSize: str = Field(description="A4 is set by default. Can be Letter, Legal, Tabloid, Ledger, A0, A1, A2, A3, A4, A5, A6 or a custom size. Custom size can be set in px (pixels), mm or in (inches) with width and height separated by space like this: 200 300, 200px 300px, 200mm 300mm, 20cm 30cm or 6in 8in. (Optional)", default=""),
    orientation: str = Field(description="Set to Portrait or Landscape. Portrait is set by default. (Optional)", default=""),
    printBackground: bool = Field(description="true by default. Set to false to disable printing of background. (Optional)", default=True),
    mediaType: str = Field(description="Uses print by default. Set to screen to convert HTML as it appears in a browser or print to convert as it appears for printing or none to set none as mediaType for CSS styles. (Optional)", default=""),
    DoNotWaitFullLoad: bool = Field(description="false by default. Set to true to skip waiting for full load (like full video load etc. that may affect the total conversion time). (Optional)", default=False),
    header: str = Field(description="User definable HTML for the header to be applied on every page header. (Optional)", default=""),
    footer: str = Field(description="User definable HTML for the footer to be applied on every page footer. (Optional)", default=""),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert external webpage URL to PDF.
    Ref: https://developer.pdf.co/api/pdf-from-url/index.html
    
    The header and footer parameters can contain valid HTML markup with the following classes used to inject printing values into them:
    - date: formatted print date
    - title: document title
    - url: document location
    - pageNumber: current page number
    - totalPages: total pages in the document
    - img: tag is supported in both the header and footer parameter, provided that the src attribute is specified as a base64-encoded string.
    For example, the following markup will generate Page N of NN page numbering:
    ```html
    <span style='font-size:10px'>Page <span class='pageNumber'></span> of <span class='totalPages'></span>.</span>
    """
    return await convert_from("pdf", "url", ConversionParams(url=url, margins=margins, paperSize=paperSize, orientation=orientation, printBackground=printBackground, mediaType=mediaType, DoNotWaitFullLoad=DoNotWaitFullLoad, header=header, footer=footer, httpusername=httpusername, httppassword=httppassword, name=name))

@mcp.tool()
async def html_to_pdf(
    html: str = Field(description="Input HTML code to be converted. To convert the link to a PDF use the /pdf/convert/from/url endpoint instead. If it is a local file, just pass the file content as a string."),
    margins: str = Field(description="Set to CSS style margins like 10px, 5mm, 5in for all sides or 5px 5px 5px 5px (the order of margins is top, right, bottom, left). (Optional)", default=""),
    paperSize: str = Field(description="A4 is set by default. Can be Letter, Legal, Tabloid, Ledger, A0, A1, A2, A3, A4, A5, A6 or a custom size. Custom size can be set in px (pixels), mm or in (inches) with width and height separated by space like this: 200 300, 200px 300px, 200mm 300mm, 20cm 30cm or 6in 8in. (Optional)", default=""),
    orientation: str = Field(description="Set to Portrait or Landscape. Portrait is set by default. (Optional)", default=""),
    printBackground: bool = Field(description="true by default. Set to false to disable printing of background. (Optional)", default=True),
    mediaType: str = Field(description="Uses print by default. Set to screen to convert HTML as it appears in a browser or print to convert as it appears for printing or none to set none as mediaType for CSS styles. (Optional)", default=""),
    DoNotWaitFullLoad: bool = Field(description="false by default. Set to true to skip waiting for full load (like full video load etc. that may affect the total conversion time). (Optional)", default=False),
    header: str = Field(description="User definable HTML for the header to be applied on every page header. (Optional)", default=""),
    footer: str = Field(description="User definable HTML for the footer to be applied on every page footer. (Optional)", default=""),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert HTML to PDF.
    Ref: https://developer.pdf.co/api/pdf-from-html/index.html
    
    The header and footer parameters can contain valid HTML markup with the following classes used to inject printing values into them:
    - date: formatted print date
    - title: document title
    - url: document location
    - pageNumber: current page number
    - totalPages: total pages in the document
    - img: tag is supported in both the header and footer parameter, provided that the src attribute is specified as a base64-encoded string.
    For example, the following markup will generate Page N of NN page numbering:
    ```html
    <span style='font-size:10px'>Page <span class='pageNumber'></span> of <span class='totalPages'></span>.</span>
    """
    return await convert_from("pdf", "html", ConversionParams(html=html, margins=margins, paperSize=paperSize, orientation=orientation, printBackground=printBackground, mediaType=mediaType, DoNotWaitFullLoad=DoNotWaitFullLoad, header=header, footer=footer, httpusername=httpusername, httppassword=httppassword, name=name))

@mcp.tool()
async def email_to_pdf(
    url: str = Field(description="URL to the source file (MSG, EML). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    embedAttachments: bool = Field(description="Set to true to automatically embeds all attachments from original input email MSG or EML files into the final output PDF. Set it to false if you don’t want to embed attachments so it will convert only the body of the input email. True by default.", default=True),
    convertAttachments: bool = Field(description="Set to false if you don’t want to convert attachments from the original email and want to embed them as original files (as embedded PDF attachments). Converts attachments that are supported by the PDF.co API (DOC, DOCx, HTML, PNG, JPG etc.) into PDF format and then merges into output final PDF. Non-supported file types are added as PDF attachments (Adobe Reader or another viewer may be required to view PDF attachments).", default=True),
    margins: str = Field(description="Set to CSS style margins like 10px, 5mm, 5in for all sides or 5px 5px 5px 5px (the order of margins is top, right, bottom, left). (Optional)", default=""),
    paperSize: str = Field(description="A4 is set by default. Can be Letter, Legal, Tabloid, Ledger, A0, A1, A2, A3, A4, A5, A6 or a custom size. Custom size can be set in px (pixels), mm or in (inches) with width and height separated by space like this: 200 300, 200px 300px, 200mm 300mm, 20cm 30cm or 6in 8in. (Optional)", default=""),
    orientation: str = Field(description="Set to Portrait or Landscape. Portrait is set by default. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert email to PDF.
    Ref: https://developer.pdf.co/api/pdf-from-email/index.html
    """
    return await convert_from("pdf", "email", ConversionParams(url=url, embedAttachments=embedAttachments, convertAttachments=convertAttachments, margins=margins, paperSize=paperSize, orientation=orientation))
    
@mcp.tool()
async def excel_to_csv(
    url: str = Field(description="URL to the source file (XLS, XLSX). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    worksheetIndex: str = Field(description="Index of the worksheet to convert. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert Excel(XLS, XLSX) to CSV.
    Ref: https://developer.pdf.co/api/convert-excel/index.html
    """
    return await convert_to("xls", "csv", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, name=name, worksheetIndex=worksheetIndex))

@mcp.tool()
async def excel_to_json(
    url: str = Field(description="URL to the source file (XLS, XLSX). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    worksheetIndex: str = Field(description="Index of the worksheet to convert. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert Excel(XLS, XLSX) to JSON.
    Ref: https://developer.pdf.co/api/convert-excel/index.html
    """
    return await convert_to("xls", "json", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, name=name, worksheetIndex=worksheetIndex))

@mcp.tool()
async def excel_to_html(
    url: str = Field(description="URL to the source file (XLS, XLSX). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    worksheetIndex: str = Field(description="Index of the worksheet to convert. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert Excel(XLS, XLSX) to HTML.
    Ref: https://developer.pdf.co/api/convert-excel/index.html
    """
    return await convert_to("xls", "html", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, name=name, worksheetIndex=worksheetIndex))

@mcp.tool()
async def excel_to_txt(
    url: str = Field(description="URL to the source file (XLS, XLSX). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    worksheetIndex: str = Field(description="Index of the worksheet to convert. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert Excel(XLS, XLSX) to TXT.
    Ref: https://developer.pdf.co/api/convert-excel/index.html
    """
    return await convert_to("xls", "txt", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, name=name, worksheetIndex=worksheetIndex))

@mcp.tool()
async def excel_to_xml(
    url: str = Field(description="URL to the source file (XLS, XLSX). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    worksheetIndex: str = Field(description="Index of the worksheet to convert. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert Excel(XLS, XLSX) to XML.
    Ref: https://developer.pdf.co/api/convert-excel/index.html
    """
    return await convert_to("xls", "xml", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, name=name, worksheetIndex=worksheetIndex))

@mcp.tool()
async def excel_to_pdf(
    url: str = Field(description="URL to the source file (XLS, XLSX). Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    worksheetIndex: str = Field(description="Index of the worksheet to convert. (Optional)", default=""),
) -> BaseResponse:
    """
    Convert Excel(XLS, XLSX) to PDF.
    Ref: https://developer.pdf.co/api/convert-excel/index.html
    """
    return await convert_to("xls", "pdf", ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, name=name, worksheetIndex=worksheetIndex))
