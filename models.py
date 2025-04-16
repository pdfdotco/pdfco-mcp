from pydantic import BaseModel

class BaseResponse(BaseModel):
    url: str
    error: bool
    status: int
    name: str
    remainingCredits: int
    
class AsyncRequestResponse(BaseResponse):
    jobId: str
    credits: int
    pageCount: int
    duration: int
    outputLinkValidTill: str

class JobStatusResponse(BaseResponse):
    jobId: str
    status: str
    message: str
    credits: int
    remainingCredits: int
    duration: int
    url: str