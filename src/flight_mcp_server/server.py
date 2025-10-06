from mcp.server.fastmcp import FastMCP
import sys
import os
import httpx
import json
from typing import Dict, Any, Optional, List



async def get_flights() -> str:
    params = {
        
    }