from mcp_server import mcp, base_url
from models import JobStatusResponse
from httpx import AsyncClient

@mcp.tool()
async def get_job_status(job_id: str, x_api_key: str) -> JobStatusResponse:
    """
    Get the status of a job
    Args:
        job_id: The ID of the job to get the status of
        x_api_key: The API key to use for the job status check
    Returns:
        The response from the PDF.co API
    """
    async with AsyncClient() as client:
        response = await client.post(f"{base_url}/v1/job/check", json={
            "jobId": job_id,
        }, headers={
            "x-api-key": x_api_key,
        })
    return response.json()
