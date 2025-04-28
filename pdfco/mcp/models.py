from pydantic import BaseModel, Field
from typing import Any

class BaseResponse(BaseModel):
    status: str
    content: Any
    credits_used: int | None = None
    credits_remaining: int | None = None
    tips: str | None = None

class ConversionParams(BaseModel):
    url: str = Field(description="URL to the source file. Supports publicly accessible links including Google Drive, Dropbox, PDF.co Built-In Files Storage. Use 'upload_file' tool to upload local files.", default="")
    httpusername: str = Field(description="HTTP auth user name if required to access source url. (Optional)", default="")
    httppassword: str = Field(description="HTTP auth password if required to access source url. (Optional)", default="")
    pages: str = Field(description="Comma-separated page indices (e.g., '0, 1, 2-' or '1, 3-7'). Use '!' for inverted page numbers (e.g., '!0' for last page). Processes all pages if None. (Optional)", default="")
    unwrap: bool = Field(description="Unwrap lines into a single line within table cells when lineGrouping is enabled. Must be true or false. (Optional)", default=False)
    rect: str = Field(description="Defines coordinates for extraction (e.g., '51.8,114.8,235.5,204.0'). (Optional)", default="")
    lang: str = Field(description="Language for OCR for scanned documents. Default is 'eng'. See PDF.co docs for supported languages. (Optional, Default: 'eng')", default="eng")
    line_grouping: str = Field(description="Enables line grouping within table cells when set to '1'. (Optional)", default="0")
    password: str = Field(description="Password of the PDF file. (Optional)", default="")
    name: str = Field(description="File name for the generated output. (Optional)", default="")
    autosize: bool = Field(description="Controls automatic page sizing. If true, page dimensions adjust to content. If false, uses worksheet’s page setup. (Optional)", default=False)

    html: str = Field(description="Input HTML code to be converted. To convert the link to a PDF use the /pdf/convert/from/url endpoint instead.", default="")
    templateId: str = Field(description="Set to the ID of your HTML template. You can find and copy the ID from HTML to PDF Templates.", default="")
    templateData: str = Field(description="Set it to a string with input JSON data (recommended) or CSV data.", default="")
    margins: str = Field(description="Set to CSS style margins like 10px, 5mm, 5in for all sides or 5px 5px 5px 5px (the order of margins is top, right, bottom, left). (Optional)", default="")
    paperSize: str = Field(description="A4 is set by default. Can be Letter, Legal, Tabloid, Ledger, A0, A1, A2, A3, A4, A5, A6 or a custom size. Custom size can be set in px (pixels), mm or in (inches) with width and height separated by space like this: 200 300, 200px 300px, 200mm 300mm, 20cm 30cm or 6in 8in. (Optional)", default="")
    orientation: str = Field(description="Set to Portrait or Landscape. Portrait is set by default. (Optional)", default="")
    printBackground: bool = Field(description="true by default. Set to false to disable printing of background. (Optional)", default=True)
    mediaType: str = Field(description="Uses print by default. Set to screen to convert HTML as it appears in a browser or print to convert as it appears for printing or none to set none as mediaType for CSS styles. (Optional)", default="")
    DoNotWaitFullLoad: bool = Field(description="false by default. Set to true to skip waiting for full load (like full video load etc. that may affect the total conversion time). (Optional)", default=False)
    header: str = Field(description="User definable HTML for the header to be applied on every page header. (Optional)", default="")
    footer: str = Field(description="User definable HTML for the footer to be applied on every page footer. (Optional)", default="")

    worksheetIndex: str = Field(description="Index of the worksheet to convert. (Optional)", default="")

    def parse_payload(self, async_mode: bool = True):
        payload = {
            "async": async_mode,
        }
        if self.url: payload["url"] = self.url
        if self.httpusername: payload["httpusername"] = self.httpusername
        if self.httppassword: payload["httppassword"] = self.httppassword
        if self.pages: payload["pages"] = self.pages
        if self.unwrap: payload["unwrap"] = self.unwrap
        if self.rect: payload["rect"] = self.rect
        if self.lang: payload["lang"] = self.lang
        if self.line_grouping: payload["lineGrouping"] = self.line_grouping
        if self.password: payload["password"] = self.password
        if self.name: payload["name"] = self.name
        if self.autosize: payload["autosize"] = self.autosize
        
        if self.html: payload["html"] = self.html
        if self.templateId: payload["templateId"] = self.templateId
        if self.templateData: payload["templateData"] = self.templateData
        if self.margins: payload["margins"] = self.margins
        if self.paperSize: payload["paperSize"] = self.paperSize
        if self.orientation: payload["orientation"] = self.orientation
        if self.printBackground: payload["printBackground"] = self.printBackground
        if self.mediaType: payload["mediaType"] = self.mediaType
        if self.DoNotWaitFullLoad: payload["DoNotWaitFullLoad"] = self.DoNotWaitFullLoad
        if self.header: payload["header"] = self.header
        if self.footer: payload["footer"] = self.footer
        
        if self.worksheetIndex: payload["worksheetIndex"] = self.worksheetIndex
        
        return payload
