from mcp_server import mcp, base_url
from mcp.server.fastmcp import Context
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
import json
import httpx

with open("openapi.json", "r", encoding="utf-8") as f:
    raw_spec = json.load(f)
spec = reduce_openapi_spec(raw_spec)

@mcp.prompt("planner")
async def planner_prompt(query: str) -> str:
    return f"""
    You are a helpful PDF.co API agent.
    You are given a user query and you need to plan the next action to take.
    You can use the following tools to help you:
    - get_all_pdf_co_apis
    - call_pdf_co_api
    
    Here is the user query:
    {query}
    """

@mcp.tool()
async def get_all_pdf_co_apis() -> str:
    """
    Get the OpenAPI spec for the PDF.co API
    """
    return spec

@mcp.tool()
async def call_pdf_co_api(method: str, path: str, body: dict, x_api_key: str, ctx: Context) -> dict:
    """
    Call a PDF.co API
    Use async mode if you can.
    
    Args:
        method: The HTTP method to use
        path: The path to call
        body: The body to send
        x_api_key: The API key to use
        
    Returns:
        The response from the API
    """
    async with httpx.AsyncClient(base_url=base_url) as client:
        ctx.info(f"Calling {method} {path} with body {body}")
        try:    
            response = await client.request(method, path, json=body, headers={"x-api-key": x_api_key})
            ctx.info(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            ctx.error(f"Error: {e}")
            return {"error": e}
        
if __name__ == "__main__":
    endpoints = spec.endpoints
    for endpoint in endpoints:
        print(endpoint[0], endpoint[1])