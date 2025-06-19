from pdfco.mcp.server import mcp
from pdfco.mcp.services.pdf import add_pdf_password, remove_pdf_password
from pdfco.mcp.models import BaseResponse, ConversionParams

from pydantic import Field


@mcp.tool()
async def pdf_add_password(
    url: str = Field(
        description="URL to the source PDF file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files."
    ),
    owner_password: str = Field(
        description="The main owner password that is used for document encryption and for setting/removing restrictions."
    ),
    user_password: str = Field(
        description="The optional user password will be asked for viewing and printing document.",
        default="",
    ),
    encryption_algorithm: str = Field(
        description="Encryption algorithm. Valid values: RC4_40bit, RC4_128bit, AES_128bit, AES_256bit. AES_128bit or higher is recommended.",
        default="AES_256bit",
    ),
    allow_accessibility_support: bool = Field(
        description="Allow or prohibit content extraction for accessibility needs.",
        default=False,
    ),
    allow_assembly_document: bool = Field(
        description="Allow or prohibit assembling the document.", default=False
    ),
    allow_print_document: bool = Field(
        description="Allow or prohibit printing PDF document.", default=False
    ),
    allow_fill_forms: bool = Field(
        description="Allow or prohibit the filling of interactive form fields (including signature fields) in the PDF documents.",
        default=False,
    ),
    allow_modify_document: bool = Field(
        description="Allow or prohibit modification of PDF document.", default=False
    ),
    allow_content_extraction: bool = Field(
        description="Allow or prohibit copying content from PDF document.",
        default=False,
    ),
    allow_modify_annotations: bool = Field(
        description="Allow or prohibit interacting with text annotations and forms in PDF document.",
        default=False,
    ),
    print_quality: str = Field(
        description="Allowed printing quality. Valid values: HighResolution, LowResolution.",
        default="",
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
        description="Password of the PDF file if it's already password-protected. (Optional)",
        default="",
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
    Add password protection to a PDF file.
    Ref: https://developer.pdf.co/api-reference/pdf-password/add.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        password=password,
        name=name,
    )

    additional_params = {
        "ownerPassword": owner_password,
    }

    if user_password is not None:
        additional_params["userPassword"] = user_password

    if encryption_algorithm is not None:
        additional_params["EncryptionAlgorithm"] = encryption_algorithm

    if allow_accessibility_support is not None:
        additional_params["AllowAccessibilitySupport"] = allow_accessibility_support

    if allow_assembly_document is not None:
        additional_params["AllowAssemblyDocument"] = allow_assembly_document

    if allow_print_document is not None:
        additional_params["AllowPrintDocument"] = allow_print_document

    if allow_fill_forms is not None:
        additional_params["AllowFillForms"] = allow_fill_forms

    if allow_modify_document is not None:
        additional_params["AllowModifyDocument"] = allow_modify_document

    if allow_content_extraction is not None:
        additional_params["AllowContentExtraction"] = allow_content_extraction

    if allow_modify_annotations is not None:
        additional_params["AllowModifyAnnotations"] = allow_modify_annotations

    if print_quality is not None:
        additional_params["PrintQuality"] = print_quality

    return await add_pdf_password(params, **additional_params, api_key=api_key)


@mcp.tool()
async def pdf_remove_password(
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
        description="Password of the PDF file to be removed. (Optional)", default=""
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
    Remove password protection from a PDF file.
    Ref: https://developer.pdf.co/api-reference/pdf-password/remove.md
    """
    params = ConversionParams(
        url=url,
        httpusername=httpusername,
        httppassword=httppassword,
        password=password,
        name=name,
    )

    return await remove_pdf_password(params, api_key=api_key)
