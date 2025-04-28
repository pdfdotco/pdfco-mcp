import asyncio
import time
from pdfco.mcp.server import mcp
from pdfco.mcp.services.client import PDFCoClient
from pdfco.mcp.models import BaseResponse

from pydantic import Field

@mcp.tool()
async def get_job_check(
    job_id: str = Field(description="The ID of the job to get the status of")
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
        async with PDFCoClient() as client:
            response = await client.post("/v1/job/check", json={
                "jobId": job_id,
            })
            return BaseResponse(
                status=response.json()["status"],
                content=response.json(),
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
    timeout: int = Field(description="The timeout to wait for the job to complete (seconds)", default=300)
) -> BaseResponse:
    """
    Wait for a job to complete
    """
    start_time = time.time()
    while True:
        response = await get_job_check(job_id)
        if response.status == "success":
            return response
        await asyncio.sleep(interval)
        if time.time() - start_time > timeout:
            return BaseResponse(
                status="error",
                content="Job timed out",
            )
