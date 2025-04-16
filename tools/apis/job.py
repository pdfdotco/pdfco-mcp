from mcp_server import mcp, base_url
from models import JobStatusResponse
from httpx import AsyncClient
from mcp.server.fastmcp import Context

@mcp.tool()
async def get_job_check(job_id: str, x_api_key: str, ctx: Context) -> JobStatusResponse:
    """
    Check the status and results of a job
    
    Args:
        job_id: The ID of the job to get the status of
        x_api_key: The API key to use for the job status check
    Returns:
        The response from the PDF.co API
    """
    if ctx:
        ctx.info(f"Getting job status for: {job_id}")
    try:
        async with AsyncClient(base_url=base_url) as client:
            response = await client.post("/v1/job/check", json={
                "jobId": job_id,
            }, headers={
                "x-api-key": x_api_key,
            })
            if ctx:
                ctx.info(f"Response: {response.json()}")
            return response.json()
    except Exception as e:
        if ctx:
            ctx.error(f"Error: {e}")
        raise e
