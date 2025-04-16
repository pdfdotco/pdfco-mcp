from mcp_server import mcp, base_url
from httpx import AsyncClient
from mcp.server.fastmcp import Context

@mcp.tool()
async def pdf_to_json(
    url: str,
    x_api_key: str,
    httpusername: str | None = None,
    httppassword: str | None = None,
    pages: str | None = None,
    unwrap: bool | None = None,
    rect: str | None = None,
    lang: str | None = None,
    line_grouping: str | None = None,
    password: str | None = None,
    name: str | None = None,
    ctx: Context | None = None,
    ) -> dict:
    """
    Convert PDF and scanned images into JSON representation with text, fonts, images, vectors, and formatting preserved using the /pdf/convert/to/json2 endpoint.

    Ref: https://developer.pdf.co/api/pdf-to-json/index.html#post-tag-pdf-to-json2

    Args:
        url: URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files.
        x_api_key: The API key.
        httpusername: HTTP auth user name if required to access source url. (Optional)
        httppassword: HTTP auth password if required to access source url. (Optional)
        pages: Comma-separated page indices (e.g., "0, 1, 2-" or "1, 3-7"). Use "!" for inverted page numbers (e.g., "!0" for last page). Processes all pages if None. (Optional)
        unwrap: Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)
        rect: Defines coordinates for extraction (e.g., "51.8,114.8,235.5,204.0"). (Optional)
        lang: Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')
        line_grouping: Enables line grouping within table cells when set to "1". (Optional)
        password: Password of the PDF file. (Optional)
        name: File name for the generated output. (Optional)

    Returns:
        The response from the PDF.co API. The response contains a jobId.
    """
    if ctx:
        ctx.info(f"Converting PDF to JSON: {url}")
    payload = {
        "url": url,
    }
    
    if httpusername is not None: payload["httpusername"] = httpusername
    if httppassword is not None: payload["httppassword"] = httppassword
    if pages is not None: payload["pages"] = pages
    if unwrap is not None: payload["unwrap"] = unwrap
    if rect is not None: payload["rect"] = rect
    if lang is not None: payload["lang"] = lang
    if line_grouping is not None: payload["lineGrouping"] = line_grouping
    if password is not None: payload["password"] = password
    if name is not None: payload["name"] = name

    if ctx:
        ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/convert/to/json2", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            ctx.error(f"Error: {e}")
        raise e
