from mcp.server.fastmcp import FastMCP
import sys
import os
import json
import asyncio
from typing import Dict, Any, Optional, List
from src.flight_mcp_server.core.config import config
from src.flight_mcp_server.utils import flight_api_request, format_flight_results

mcp = FastMCP("flights")

mcp.settings.host = "0.0.0.0"
mcp.settings.port = 8000
mcp.settings.sse_path = "/mcp"


@mcp.tool()
async def get_flights(params: Dict[str, Any]=None, top_k=3) -> str:
    """
    Get the top k contexts, each representing a flight itinerary for a given query.

    Args:
        query: The query to get top k context for
        top_k: the number of context chunks to retrieve

    Returns:
        A dictionary of the top k context chunks, each representing flight itinerary for a given query
    """
    flight_data = await flight_api_request(params, top_k)
    formatted_flight_data = format_flight_results(flight_data, top_k)
    return formatted_flight_data


if __name__ == "__main__":
    mcp.run(transport="streamable-http")