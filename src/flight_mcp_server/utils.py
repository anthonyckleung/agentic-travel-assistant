import sys
import os
import httpx
from src.flight_mcp_server.core.config import config
from typing import Dict, Any


RAPIDAPI_API_KEY = config.RAPIDAPI_API_KEY
RAPIDAPI_BASE_URL = config.RAPIDAPI_BASE_URL


#Helper Functions
async def flight_api_request(params: Dict[str, Any]=None, top_k=3) -> Dict[str, Any]:
    """Make a request to the TripAdvisor API"""
    if not RAPIDAPI_API_KEY:
        return {"error": "TripAdvisor API key not configured. Set RAPIDAPI_API_KEY environment variable."}

    headers = {
        "x-rapidapi-host": RAPIDAPI_BASE_URL, 
        "x-rapidapi-key": RAPIDAPI_API_KEY,
    }

    if params is None:
        params = {}

    endpoint = 'searchFlights'

    url = f"https://{RAPIDAPI_BASE_URL}/api/v1/{endpoint}"

    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        flights = []
        itineraries = data['data']['itineraries']['topFlights']
        for itinerary in itineraries[:top_k]:
            flight = itinerary.get('flights')[0]
            flights.append({
                "price": itinerary.get("price"),
                "departure_time": itinerary.get("departure_time"),
                "arrival_time": itinerary.get("arrival_time"),
                "departure_airport": flight.get('departure_airport'),
                "arrival_airport": flight.get('arrival_airport'),
                "duration": flight.get('duration'),
                "airline": flight.get('airline'),
                "airline_logo": flight.get('airline_logo')
            })
        return {"flights": flights}
    except httpx.HTTPStatusError as e:
        # Handle specific HTTP errors
        return {"isError": True, "error": f"HTTP error occurred: {str(e)}"}
    except httpx.RequestError as e:
        # Handle network/request errors
        return {"isError": True, "error": f"Network error occurred: {str(e)}"}
    except Exception as e:
        # Catch-all for unexpected errors
        return {"isError": True, "error": f"An unexpected error occurred: {str(e)}"}
    

def format_flight_results(flight_data, top_k=3):
    flights = flight_data.get("flights", [])[:top_k]
    if not flights:
        return "No flight options found."

    result_lines = []
    for i, flight in enumerate(flights, start=1):
        price = flight.get("price", "N/A")
        airline = flight.get("airline", "Unknown Airline")
        departure_time = flight.get("departure_time", "N/A")
        arrival_time = flight.get("arrival_time", "N/A")
        duration = flight.get("duration", {}).get("text", "N/A")
        
        dep_airport = flight.get("departure_airport", {})
        dep_name = dep_airport.get("airport_name", "Unknown Airport")
        dep_code = dep_airport.get("airport_code", "")
        
        arr_airport = flight.get("arrival_airport", {})
        arr_name = arr_airport.get("airport_name", "Unknown Airport")
        arr_code = arr_airport.get("airport_code", "")

        flight_text = (
            f"{i}. Flight by {airline} from {dep_name} ({dep_code}) "
            f"to {arr_name} ({arr_code})\n"
            f"   - Departure: {departure_time}\n"
            f"   - Arrival: {arrival_time}\n"
            f"   - Duration: {duration}\n"
            f"   - Price: ${price}"
        )
        result_lines.append(flight_text)

    return "\n\n".join(result_lines)