from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import merge_pdf, split_pdf, optimize_pdf
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field


@mcp.tool()
async def pdf_merge(
    url: str = Field(description="URLs to the source files as a comma-separated list. Supports PDF, DOC, DOCX, RTF, TXT, XLS, XLSX, CSV, images, and more. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
) -> BaseResponse:
    """
    Merge PDF from two or more PDF, DOC, XLS, images, even ZIP with documents and images into a new PDF.
    Ref: https://developer.pdf.co/api/pdf-merge/index.html#post-tag-pdf-merge2
    """
    return await merge_pdf(ConversionParams(url=url, httpusername=httpusername, httppassword=httppassword, name=name))

@mcp.tool()
async def pdf_split(
    url: str = Field(description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    pages: str = Field(description="Comma-separated indices of pages (or page ranges) that you want to use. The first-page index is 1. For example: '1,3,5-7' or '1-2,4-'. Use '*' to split every page into separate files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default=""),
    password: str = Field(description="Password of the PDF file. (Optional)", default=""),
    name: str = Field(description="Base file name for the generated output files. (Optional)", default=""),
) -> BaseResponse:
    """
    Split a PDF into multiple PDF files using page indexes or page ranges.
    Ref: https://developer.pdf.co/api/pdf-split/index.html
    """
    params = ConversionParams(
        url=url,
        pages=pages,
        httpusername=httpusername,
        httppassword=httppassword,
        password=password,
        name=name,
    )
    
    return await split_pdf(params)

@mcp.tool()
async def pdf_optimize(
    url: str = Field(description="URL to the source PDF file. Supports publicly accessible links, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."),
    httpusername: str = Field(description="HTTP auth user name if required to access source URL. (Optional)", default=""),
    httppassword: str = Field(description="HTTP auth password if required to access source URL. (Optional)", default=""),
    name: str = Field(description="File name for the generated output. (Optional)", default=""),
    password: str = Field(description="Password of the input PDF file. (Optional)", default=""),
) -> BaseResponse:
    """
    Optimize a PDF document to reduce its size.
    Ref: https://developer.pdf.co/api/pdf-optimize/index.html
    """
    common_params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        name=name,
        password=password
    )
        
    return await optimize_pdf(common_params)
