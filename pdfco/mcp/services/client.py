from contextlib import asynccontextmanager
from httpx import AsyncClient
import os
from typing import AsyncGenerator

__BASE_URL = "https://api.pdftest.co"
X_API_KEY = os.getenv("X_API_KEY")  
if not X_API_KEY:
    raise ValueError("Please set X_API_KEY in the environment variables. To get the API key please sign up at https://pdf.co and you can get the API key from the dashboard.")

@asynccontextmanager
async def PDFCoClient() -> AsyncGenerator[AsyncClient, None]:
    client = AsyncClient(
            base_url=__BASE_URL,
            headers={"x-api-key": X_API_KEY},
        )
    try:
        yield client
    finally:
        await client.aclose()
