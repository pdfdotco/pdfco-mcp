import sys
from pdfco.mcp.models import BaseResponse, ConversionParams
from pdfco.mcp.services.client import PDFCoClient

async def convert_to(_from: str, _to: str, params: ConversionParams) -> BaseResponse:
    return await request(f'{_from}/convert/to/{_to}', params)

async def convert_from(_to: str, _from: str, params: ConversionParams) -> BaseResponse:
    return await request(f'{_to}/convert/from/{_from}', params)

async def request(endpoint: str, params: ConversionParams) -> BaseResponse:
    payload = params.parse_payload(async_mode=True)
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
