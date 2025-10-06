import sys
import os
import httpx
from src.flight_mcp_server.core.config import config
from typing import Dict, Any


#Helper Functions
async def tripadvisor_api_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make a request to the TripAdvisor API"""
    if not config.RAPIDAPI_API_KEY:
        return {"error": "TripAdvisor API key not configured. Set RAPIDAPI_API_KEY environment variable."}
    
    headers = {"accept": "application/json", "key": config.RAPIDAPI_API_KEY}

    if params is None:
        params = {}

    params["key"] = config.RAPIDAPI_API_KEY

    url = f"{config.RAPIDAPI_BASE_URL}/{endpoint}"
    
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