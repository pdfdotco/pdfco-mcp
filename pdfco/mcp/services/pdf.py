import sys
from pdfco.mcp.models import BaseResponse, ConversionParams
from pdfco.mcp.services.client import PDFCoClient


async def convert_to(
    _from: str, _to: str, params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request(f"{_from}/convert/to/{_to}", params, api_key=api_key)


async def convert_from(
    _to: str, _from: str, params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request(f"{_to}/convert/from/{_from}", params, api_key=api_key)


async def merge_pdf(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("pdf/merge2", params, api_key=api_key)


async def split_pdf(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("pdf/split", params, api_key=api_key)


async def get_pdf_form_fields_info(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("pdf/info/fields", params, api_key=api_key)


async def fill_pdf_form_fields(
    params: ConversionParams,
    fields: list | None = None,
    annotations: list | None = None,
    api_key: str | None = None,
) -> BaseResponse:
    custom_payload = {}
    if fields:
        custom_payload["fields"] = fields
    if annotations:
        custom_payload["annotations"] = annotations
    return await request(
        "pdf/edit/add", params, custom_payload=custom_payload, api_key=api_key
    )


async def pdf_add(
    params: ConversionParams, api_key: str | None = None, **kwargs
) -> BaseResponse:
    """General PDF Add function that supports all PDF Add API parameters"""
    custom_payload = {}

    # Add all supported parameters
    for key, value in kwargs.items():
        if value is not None and value != "":
            custom_payload[key] = value

    return await request(
        "pdf/edit/add", params, custom_payload=custom_payload, api_key=api_key
    )


async def find_text_in_pdf(
    params: ConversionParams,
    search_string: str,
    regex_search: bool = False,
    word_matching_mode: str | None = None,
    api_key: str | None = None,
) -> BaseResponse:
    custom_payload = {"searchString": search_string, "regexSearch": regex_search}
    if word_matching_mode:
        custom_payload["wordMatchingMode"] = word_matching_mode
    return await request(
        "pdf/find", params, custom_payload=custom_payload, api_key=api_key
    )


async def find_table_in_pdf(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("pdf/find/table", params, api_key=api_key)


async def make_pdf_searchable(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("pdf/makesearchable", params, api_key=api_key)


async def make_pdf_unsearchable(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("pdf/makeunsearchable", params, api_key=api_key)


async def get_pdf_info(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("pdf/info", params, api_key=api_key)


async def add_pdf_password(
    params: ConversionParams, api_key: str | None = None, **kwargs
) -> BaseResponse:
    return await request(
        "pdf/security/add", params, custom_payload=kwargs, api_key=api_key
    )


async def remove_pdf_password(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("pdf/security/remove", params, api_key=api_key)


async def parse_invoice(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("ai-invoice-parser", params, api_key=api_key)


async def extract_pdf_attachments(
    params: ConversionParams, api_key: str | None = None
) -> BaseResponse:
    return await request("pdf/attachments/extract", params, api_key=api_key)


ERROR_TIPS = {
    401: "The API key is missing or invalid. Check the api_key parameter or the X_API_KEY environment variable.",
    402: "The account has no credits left. Top up or change the subscription at https://app.pdf.co before retrying.",
    429: "Too many requests. Wait a moment and retry.",
}


def _error_tip(code: int | None, message: str | None) -> str:
    if code in ERROR_TIPS:
        return ERROR_TIPS[code]
    return f"The API rejected the request: {message or 'no message'}. Fix the input before retrying."


def _error_code(status_code: int, json_data: dict) -> int:
    code = json_data.get("errorCode", json_data.get("status"))
    return code if isinstance(code, int) else status_code


async def request(
    endpoint: str,
    params: ConversionParams,
    custom_payload: dict | None = None,
    api_key: str | None = None,
) -> BaseResponse:
    payload = params.parse_payload(async_mode=True)
    if custom_payload:
        payload.update(custom_payload)

    url = f"/v1/{endpoint}"
    try:
        async with PDFCoClient(api_key=api_key) as client:
            response = await client.post(url, json=payload)
    except Exception as e:
        return BaseResponse(
            status="error",
            content=f"{type(e).__name__}: {' '.join(str(arg) for arg in e.args if arg)}",
        )

    try:
        json_data = response.json()
    except ValueError:
        print(
            f"pdfco-mcp: POST {url} -> {response.status_code} (non-JSON body)",
            file=sys.stderr,
        )
        return BaseResponse(
            status="error",
            content=f"HTTP {response.status_code}: {response.text[:500]}",
        )

    if not isinstance(json_data, dict):
        json_data = {"result": json_data}
    job_id = json_data.get("jobId")
    print(
        f"pdfco-mcp: POST {url} -> {response.status_code} jobId={job_id}",
        file=sys.stderr,
    )

    if response.status_code >= 400 or json_data.get("error") is True:
        code = _error_code(response.status_code, json_data)
        return BaseResponse(
            status="error",
            content=json_data,
            credits_used=json_data.get("credits"),
            credits_remaining=json_data.get("remainingCredits"),
            tips=_error_tip(code, json_data.get("message")),
        )

    if job_id:
        return BaseResponse(
            status="working",
            content=json_data,
            credits_used=json_data.get("credits"),
            credits_remaining=json_data.get("remainingCredits"),
            tips=f"You **should** use the 'wait_job_completion' tool to wait for the job [{job_id}] to complete.",
        )

    return BaseResponse(
        status="success",
        content=json_data,
        credits_used=json_data.get("credits"),
        credits_remaining=json_data.get("remainingCredits"),
    )
