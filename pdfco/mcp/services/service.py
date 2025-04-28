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
            response = await client.post(url, json=payload)
            json_data = response.json()
            return BaseResponse(
                status="working",
                content=json_data,
                tips=f"You **should** use the 'wait_job_completion' tool to wait for the job [{json_data['jobId']}] to complete",
            )
    except Exception as e:
        return BaseResponse(
            status="error",
            content=str(e),
        )
