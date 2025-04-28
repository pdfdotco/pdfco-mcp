from pydantic import BaseModel, Field
from typing import Any

class BaseResponse(BaseModel):
    status: str
    content: Any
    tips: str | None = None

class ConversionParams(BaseModel):
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files.")
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default="")
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default="")
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default="")
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False)
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default="")
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng")
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0")
    password: str = Field(description="Password of the PDF file. (Optional)", default="")
    name: str = Field(description="File name for the generated output. (Optional)", default="")

    def parse_payload(self, async_mode: bool = True):
        payload = {
            "url": self.url,
            "async": async_mode,
        }
        
        if self.httpusername: payload["httpusername"] = self.httpusername
        if self.httppassword: payload["httppassword"] = self.httppassword
        if self.pages: payload["pages"] = self.pages
        if self.unwrap: payload["unwrap"] = self.unwrap
        if self.rect: payload["rect"] = self.rect
        if self.lang: payload["lang"] = self.lang
        if self.line_grouping: payload["lineGrouping"] = self.line_grouping
        if self.password: payload["password"] = self.password
        if self.name: payload["name"] = self.name

        return payload
