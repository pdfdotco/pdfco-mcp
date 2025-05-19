import sys
from pdfco.mcp.models import BaseResponse, ConversionParams
from pdfco.mcp.services.client import PDFCoClient

async def convert_to(_from: str, _to: str, params: ConversionParams) -> BaseResponse:
    return await request(f'{_from}/convert/to/{_to}', params)

async def convert_from(_to: str, _from: str, params: ConversionParams) -> BaseResponse:
    return await request(f'{_to}/convert/from/{_from}', params)

async def merge_pdf(params: ConversionParams) -> BaseResponse:
    return await request(f'pdf/merge2', params)

async def split_pdf(params: ConversionParams) -> BaseResponse:
    return await request(f'pdf/split', params)

async def optimize_pdf(params: ConversionParams) -> BaseResponse:
    return await request('pdf/optimize', params)

async def get_pdf_form_fields_info(params: ConversionParams) -> BaseResponse:
    return await request('pdf/info/fields', params)

async def fill_pdf_form_fields(params: ConversionParams, fields: list = None, annotations: list = None) -> BaseResponse:
    custom_payload = {}
    if fields:
        custom_payload["fields"] = fields
    if annotations:
        custom_payload["annotations"] = annotations
    return await request('pdf/edit/add', params, custom_payload=custom_payload)

async def find_text_in_pdf(params: ConversionParams, search_string: str, regex_search: bool = False, word_matching_mode: str = None) -> BaseResponse:
    custom_payload = {
        "searchString": search_string,
        "regexSearch": regex_search
    }
    if word_matching_mode:
        custom_payload["wordMatchingMode"] = word_matching_mode
    return await request('pdf/find', params, custom_payload=custom_payload)

async def find_table_in_pdf(params: ConversionParams) -> BaseResponse:
    return await request('pdf/find/table', params)

async def make_pdf_searchable(params: ConversionParams) -> BaseResponse:
    return await request('pdf/makesearchable', params)

async def make_pdf_unsearchable(params: ConversionParams) -> BaseResponse:
    return await request('pdf/makeunsearchable', params)

async def delete_pdf_pages(params: ConversionParams) -> BaseResponse:
    return await request('pdf/edit/delete-pages', params)

async def rotate_pdf_pages(params: ConversionParams, angle: int) -> BaseResponse:
    custom_payload = {"angle": angle}
    return await request('pdf/edit/rotate', params, custom_payload=custom_payload)

async def auto_rotate_pdf_pages(params: ConversionParams) -> BaseResponse:
    return await request('pdf/edit/rotate/auto', params)

async def request(endpoint: str, params: ConversionParams, custom_payload: dict = None) -> BaseResponse:
    payload = params.parse_payload(async_mode=True)
    if custom_payload:
        payload.update(custom_payload)
        
    try:
        async with PDFCoClient() as client:
            url = f"/v1/{endpoint}"
            print(f"Requesting {url} with payload {payload}", file=sys.stderr)
            response = await client.post(url, json=payload)
            print(f"response: {response}", file=sys.stderr)
            json_data = response.json()
            return BaseResponse(
                status="working",
                content=json_data,
                credits_used=json_data.get("credits"),
                credits_remaining=json_data.get("remainingCredits"),
                tips=f"You **should** use the 'wait_job_completion' tool to wait for the job [{json_data['jobId']}] to complete",
            )
    except Exception as e:
        return BaseResponse(
            status="error",
            content=f'{type(e)}: {[arg for arg in e.args if arg]}',
        )
