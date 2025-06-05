import asyncio
import time
from pdfco.mcp.server import mcp
from pdfco.mcp.services.client import PDFCoClient
from pdfco.mcp.models import BaseResponse

from pydantic import Field

@mcp.tool()
async def get_job_check(
    job_id: str = Field(description="The ID of the job to get the status of"),
    api_key: str = Field(description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)", default=None)
) -> BaseResponse:
    """
    Check the status and results of a job
    Status can be:
    - working: background job is currently in work or does not exist.
    - success: background job was successfully finished.
    - failed: background job failed for some reason (see message for more details).
    - aborted: background job was aborted.
    - unknown: unknown background job id. Available only when force is set to true for input request.
    """
    try:
        async with PDFCoClient(api_key=api_key) as client:
            response = await client.post("/v1/job/check", json={
                "jobId": job_id,
            })
            json_data = response.json()
            return BaseResponse(
                status=json_data["status"],
                content=json_data,
                credits_used=json_data.get("credits"),
                credits_remaining=json_data.get("remainingCredits"),
                tips="You can download the result if status is success",
            )
    except Exception as e:
        return BaseResponse(
            status="error",
            content=str(e),
        )

@mcp.tool()
async def wait_job_completion(
    job_id: str = Field(description="The ID of the job to get the status of"),
    interval: int = Field(description="The interval to check the status of the job (seconds)", default=1),
    timeout: int = Field(description="The timeout to wait for the job to complete (seconds)", default=300),
    api_key: str = Field(description="PDF.co API key. If not provided, will use X_API_KEY environment variable. (Optional)", default=None)
) -> BaseResponse:
    """
    Wait for a job to complete
    """
    start_time = time.time()
    job_check_count = 0
    credits_used = 0
    credits_remaining = 0
    while True:
        response = await get_job_check(job_id, api_key=api_key)
        job_check_count += 1
        credits_used += response.credits_used
        credits_remaining = response.credits_remaining
        if response.status == "success":
            return BaseResponse(
                status="success",
                content=response.content,
                credits_used=credits_used,
                credits_remaining=credits_remaining,
                tips=f"Job check count: {job_check_count}",
            )
        elif response.status == "failed":
            return BaseResponse(
                status="error",
                content=response.message,
                credits_used=credits_used,
                credits_remaining=credits_remaining,
            )
        await asyncio.sleep(interval)
        if time.time() - start_time > timeout:
            return BaseResponse(
                status="error",
                content="Job timed out",
                credits_used=credits_used,
                credits_remaining=credits_remaining,
                tips=f"Job check count: {job_check_count}",
            )
