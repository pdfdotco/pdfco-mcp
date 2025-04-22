from mcp_server import mcp, base_url
from httpx import AsyncClient
from mcp.server.fastmcp import Context

@mcp.tool()
async def pdf_to_json(
    url: str,
    x_api_key: str,
    httpusername: str,
    httppassword: str,
    pages: str,
    unwrap: bool,
    rect: str,
    lang: str,
    line_grouping: str,
    password: str,
    name: str,
    ctx: Context,
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
        await ctx.info(f"Converting PDF to JSON: {url}")
    payload = {
        "url": url,
    }
    
    if httpusername: payload["httpusername"] = httpusername
    if httppassword: payload["httppassword"] = httppassword
    if pages: payload["pages"] = pages
    if unwrap: payload["unwrap"] = unwrap
    if rect: payload["rect"] = rect
    if lang: payload["lang"] = lang
    if line_grouping: payload["lineGrouping"] = line_grouping
    if password: payload["password"] = password
    if name: payload["name"] = name

    if ctx:
        await ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/convert/to/json2", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e

@mcp.tool()
async def pdf_to_csv(
    url: str,
    x_api_key: str,
    httpusername: str,
    httppassword: str,
    pages: str,
    unwrap: bool,
    rect: str,
    lang: str,
    line_grouping: str,
    password: str,
    name: str,
    ctx: Context,
    ) -> dict:
    """
    Convert PDF and scanned images into CSV representation with layout, columns, rows, and tables.

    Ref: https://developer.pdf.co/api/pdf-to-csv/index.html

    Args:
        url: URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files.
        x_api_key: The API key.
        httpusername: HTTP auth user name if required to access source url. (Optional)
        httppassword: HTTP auth password if required to access source url. (Optional)
        pages: Comma-separated page indices (e.g., "0, 1, 2-" or "1, 3-7"). Use "!" for inverted page numbers (e.g., "!0" for last page). Processes all pages if None. (Optional)
        unwrap: Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)
        rect: Defines coordinates for extraction (e.g., "51.8,114.8,235.5,204.0"). (Optional)
        lang: Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional)
        line_grouping: Enables line grouping within table cells when set to "1". (Optional)
        password: Password of the PDF file. (Optional)
        name: File name for the generated output. (Optional)

    Returns:
        The response from the PDF.co API.
    """
    if ctx:
        await ctx.info(f"Converting PDF to CSV: {url}")
    
    payload = {
        "url": url,
    }
    
    if httpusername: payload["httpusername"] = httpusername
    if httppassword: payload["httppassword"] = httppassword
    if pages: payload["pages"] = pages
    if unwrap: payload["unwrap"] = unwrap
    if rect: payload["rect"] = rect
    if lang: payload["lang"] = lang
    if line_grouping: payload["lineGrouping"] = line_grouping
    if password: payload["password"] = password
    if name: payload["name"] = name

    if ctx:
        await ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/convert/to/csv", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e

@mcp.tool()
async def pdf_to_text(
    url: str,
    x_api_key: str,
    httpusername: str,
    httppassword: str,
    pages: str,
    unwrap: bool,
    rect: str,
    lang: str,
    line_grouping: str,
    password: str,
    name: str,
    ctx: Context,
    ) -> dict:
    """
    Convert PDF and scanned images to text with layout preserved.

    Ref: https://developer.pdf.co/api/pdf-to-text/index.html

    Args:
        url: URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage.
        x_api_key: The API key.
        httpusername: HTTP auth user name if required to access source url. (Optional)
        httppassword: HTTP auth password if required to access source url. (Optional)
        pages: Comma-separated page indices (e.g., "0, 1, 2-" or "1, 3-7"). Use "!" for inverted page numbers (e.g., "!0" for last page). (Optional)
        unwrap: Unwrap lines into a single line within table cells when lineGrouping is enabled. (Optional)
        rect: Defines coordinates for extraction (e.g., "51.8,114.8,235.5,204.0"). (Optional)
        lang: Language for OCR for scanned documents. Default is 'eng'. (Optional)
        line_grouping: Enables line grouping within table cells when set to "1". (Optional)
        password: Password of the PDF file. (Optional)
        name: File name for the generated output. (Optional)

    Returns:
        The response from the PDF.co API.
    """
    if ctx:
        await ctx.info(f"Converting PDF to Text: {url}")
    
    payload = {
        "url": url,
    }
    
    if httpusername: payload["httpusername"] = httpusername
    if httppassword: payload["httppassword"] = httppassword
    if pages: payload["pages"] = pages
    if unwrap: payload["unwrap"] = unwrap
    if rect: payload["rect"] = rect
    if lang: payload["lang"] = lang
    if line_grouping: payload["lineGrouping"] = line_grouping
    if password: payload["password"] = password
    if name: payload["name"] = name

    if ctx:
        await ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/convert/to/text", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e

@mcp.tool()
async def pdf_to_xls(
    url: str,
    x_api_key: str,
    httpusername: str,
    httppassword: str,
    pages: str,
    unwrap: bool,
    rect: str,
    lang: str,
    line_grouping: str,
    password: str,
    name: str,
    ctx: Context,
    ) -> dict:
    """
    Convert PDF and scanned images to XLS (Excel 97-2003) format.

    Ref: https://developer.pdf.co/api/pdf-to-excel/index.html

    Args:
        url: URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage.
        x_api_key: The API key.
        httpusername: HTTP auth user name if required to access source url. (Optional)
        httppassword: HTTP auth password if required to access source url. (Optional)
        pages: Comma-separated page indices (e.g., "0, 1, 2-" or "1, 3-7"). Use "!" for inverted page numbers (e.g., "!0" for last page). (Optional)
        unwrap: Unwrap lines into a single line within table cells when lineGrouping is enabled. (Optional)
        rect: Defines coordinates for extraction (e.g., "51.8,114.8,235.5,204.0"). (Optional)
        lang: Language for OCR for scanned documents. Default is 'eng'. (Optional)
        line_grouping: Enables line grouping within table cells when set to "1". (Optional)
        password: Password of the PDF file. (Optional)
        name: File name for the generated output. (Optional)

    Returns:
        The response from the PDF.co API.
    """
    if ctx:
        await ctx.info(f"Converting PDF to XLS: {url}")
    
    payload = {
        "url": url,
    }
    
    if httpusername: payload["httpusername"] = httpusername
    if httppassword: payload["httppassword"] = httppassword
    if pages: payload["pages"] = pages
    if unwrap: payload["unwrap"] = unwrap
    if rect: payload["rect"] = rect
    if lang: payload["lang"] = lang
    if line_grouping: payload["lineGrouping"] = line_grouping
    if password: payload["password"] = password
    if name: payload["name"] = name

    if ctx:
        await ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/convert/to/xls", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e

@mcp.tool()
async def pdf_to_xlsx(
    url: str,
    x_api_key: str,
    httpusername: str,
    httppassword: str,
    pages: str,
    unwrap: bool,
    rect: str,
    lang: str,
    line_grouping: str,
    password: str,
    name: str,
    ctx: Context,
    ) -> dict:
    """
    Convert PDF and scanned images to XLSX (Excel 2007+) format.

    Ref: https://developer.pdf.co/api/pdf-to-excel/index.html

    Args:
        url: URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage.
        x_api_key: The API key.
        httpusername: HTTP auth user name if required to access source url. (Optional)
        httppassword: HTTP auth password if required to access source url. (Optional)
        pages: Comma-separated page indices (e.g., "0, 1, 2-" or "1, 3-7"). Use "!" for inverted page numbers (e.g., "!0" for last page). (Optional)
        unwrap: Unwrap lines into a single line within table cells when lineGrouping is enabled. (Optional)
        rect: Defines coordinates for extraction (e.g., "51.8,114.8,235.5,204.0"). (Optional)
        lang: Language for OCR for scanned documents. Default is 'eng'. (Optional)
        line_grouping: Enables line grouping within table cells when set to "1". (Optional)
        password: Password of the PDF file. (Optional)
        name: File name for the generated output. (Optional)

    Returns:
        The response from the PDF.co API.
    """
    if ctx:
        await ctx.info(f"Converting PDF to XLSX: {url}")
    
    payload = {
        "url": url,
    }
    
    if httpusername: payload["httpusername"] = httpusername
    if httppassword: payload["httppassword"] = httppassword
    if pages: payload["pages"] = pages
    if unwrap: payload["unwrap"] = unwrap
    if rect: payload["rect"] = rect
    if lang: payload["lang"] = lang
    if line_grouping: payload["lineGrouping"] = line_grouping
    if password: payload["password"] = password
    if name: payload["name"] = name

    if ctx:
        await ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/convert/to/xlsx", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e

@mcp.tool()
async def pdf_to_xml(
    url: str,
    x_api_key: str,
    httpusername: str,
    httppassword: str,
    pages: str,
    unwrap: bool,
    rect: str,
    lang: str,
    line_grouping: str,
    password: str,
    name: str,
    ctx: Context,
    ) -> dict:
    """
    Convert PDF and scanned images to XML format.

    Ref: https://developer.pdf.co/api/pdf-to-xml/index.html

    Args:
        url: URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage.
        x_api_key: The API key.
        httpusername: HTTP auth user name if required to access source url. (Optional)
        httppassword: HTTP auth password if required to access source url. (Optional)
        pages: Comma-separated page indices (e.g., "0, 1, 2-" or "1, 3-7"). Use "!" for inverted page numbers (e.g., "!0" for last page). (Optional)
        unwrap: Unwrap lines into a single line within table cells when lineGrouping is enabled. (Optional)
        rect: Defines coordinates for extraction (e.g., "51.8,114.8,235.5,204.0"). (Optional)
        lang: Language for OCR for scanned documents. Default is 'eng'. (Optional)
        line_grouping: Enables line grouping within table cells when set to "1". (Optional)
        password: Password of the PDF file. (Optional)
        name: File name for the generated output. (Optional)

    Returns:
        The response from the PDF.co API.
    """
    if ctx:
        await ctx.info(f"Converting PDF to XML: {url}")
    
    payload = {
        "url": url,
    }
    
    if httpusername: payload["httpusername"] = httpusername
    if httppassword: payload["httppassword"] = httppassword
    if pages: payload["pages"] = pages
    if unwrap: payload["unwrap"] = unwrap
    if rect: payload["rect"] = rect
    if lang: payload["lang"] = lang
    if line_grouping: payload["lineGrouping"] = line_grouping
    if password: payload["password"] = password
    if name: payload["name"] = name

    if ctx:
        await ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/convert/to/xml", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e

@mcp.tool()
async def pdf_to_html(
    url: str,
    x_api_key: str,
    httpusername: str,
    httppassword: str,
    pages: str,
    unwrap: bool,
    rect: str,
    lang: str,
    line_grouping: str,
    password: str,
    name: str,
    ctx: Context,
    ) -> dict:
    """
    Convert PDF and scanned images to HTML format.

    Ref: https://developer.pdf.co/api/pdf-to-html/index.html

    Args:
        url: URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage.
        x_api_key: The API key.
        httpusername: HTTP auth user name if required to access source url. (Optional)
        httppassword: HTTP auth password if required to access source url. (Optional)
        pages: Comma-separated page indices (e.g., "0, 1, 2-" or "1, 3-7"). Use "!" for inverted page numbers (e.g., "!0" for last page). (Optional)
        unwrap: Unwrap lines into a single line within table cells when lineGrouping is enabled. (Optional)
        rect: Defines coordinates for extraction (e.g., "51.8,114.8,235.5,204.0"). (Optional)
        lang: Language for OCR for scanned documents. Default is 'eng'. (Optional)
        line_grouping: Enables line grouping within table cells when set to "1". (Optional)
        password: Password of the PDF file. (Optional)
        name: File name for the generated output. (Optional)

    Returns:
        The response from the PDF.co API.
    """
    if ctx:
        await ctx.info(f"Converting PDF to HTML: {url}")
    
    payload = {
        "url": url,
    }
    
    if httpusername: payload["httpusername"] = httpusername
    if httppassword: payload["httppassword"] = httppassword
    if pages: payload["pages"] = pages
    if unwrap: payload["unwrap"] = unwrap
    if rect: payload["rect"] = rect
    if lang: payload["lang"] = lang
    if line_grouping: payload["lineGrouping"] = line_grouping
    if password: payload["password"] = password
    if name: payload["name"] = name

    if ctx:
        await ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                "/v1/pdf/convert/to/html", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e

@mcp.tool()
async def pdf_to_image(
    url: str,
    x_api_key: str,
    httpusername: str,
    httppassword: str,
    pages: str,
    password: str,
    name: str,
    ctx: Context,
    type: str = "jpg",
    ) -> dict:
    """
    Convert PDF to various image formats (JPG, PNG, WebP, TIFF).

    Ref: https://developer.pdf.co/api/pdf-to-image/index.html

    Args:
        url: URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage.
        x_api_key: The API key.
        type: Image format to convert to. Must be one of: 'jpg', 'png', 'webp', 'tiff'. (Default: 'jpg')
        httpusername: HTTP auth user name if required to access source url. (Optional)
        httppassword: HTTP auth password if required to access source url. (Optional)
        pages: Comma-separated page indices (e.g., "0, 1, 2-" or "1, 3-7"). Use "!" for inverted page numbers (e.g., "!0" for last page). (Optional)
        password: Password of the PDF file. (Optional)
        name: File name for the generated output. (Optional)

    Returns:
        The response from the PDF.co API.
    """
    if type not in ["jpg", "png", "webp", "tiff"]:
        raise ValueError("Type must be one of: 'jpg', 'png', 'webp', 'tiff'")

    if ctx:
        await ctx.info(f"Converting PDF to {type.upper()}: {url}")
    
    payload = {
        "url": url,
    }
    
    if httpusername: payload["httpusername"] = httpusername
    if httppassword: payload["httppassword"] = httppassword
    if pages: payload["pages"] = pages
    if password: payload["password"] = password
    if name: payload["name"] = name

    if ctx:
        await ctx.info(f"Payload: {payload}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            if ctx:
                await ctx.info(f"Calling PDF.co API")
            response = await client.post(
                f"/v1/pdf/convert/to/{type}", 
                json=payload, 
                headers={
                    "x-api-key": x_api_key,
                })
            if ctx:
                await ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            await ctx.error(f"Error: {e}")
        raise e
