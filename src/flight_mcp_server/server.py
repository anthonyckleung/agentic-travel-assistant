from mcp.server.fastmcp import FastMCP
import sys
import os
import httpx
import json
from typing import Dict, Any, Optional, List
from core.config import config

RAPIDAPI_BASE_URL = config.RAPIDAPI_BASE_URL
RAPIDAPI_API_KEY = config.RAPIDAPI_API_KEY

mcp = FastMCP("google-flights-mcp")


@mcp.tool()
async def flight_api_request(endpoint:str, params: Dict[str, Any]=None) -> Dict[str, Any]:
    """Make a request to the TripAdvisor API"""
    if not RAPIDAPI_API_KEY:
        return {"error": "TripAdvisor API key not configured. Set RAPIDAPI_API_KEY environment variable."}

    headers = {
        "x-rapidapi-host": RAPIDAPI_BASE_URL, 
        "x-rapidapi-key": RAPIDAPI_API_KEY,
    }

    if params is None:
        params = {}

    url = f"https://{RAPIDAPI_BASE_URL}/api/v1/{endpoint}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP error occurred: {e}",
                "details": str(e)
            }


if __name__ == "__main__":
    mcp.run(transport='http', host="0.0.0.0", port=8000)