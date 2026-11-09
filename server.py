"""Egyszerű távoli MCP szerver, Renderen futtatva.

Helyi teszt:  python server.py   ->  http://localhost:8000/mcp
"""
import os
from urllib.parse import quote

from mcp.server.fastmcp import FastMCP
import requests

# A Render a PORT környezeti változóban adja meg a portot, és 0.0.0.0-n kell hallgatni
mcp = FastMCP(
    "egyszeru-mcp",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
)


@mcp.tool()
def koszon(nev: str) -> str:
    """Üdvözli a megadott nevű embert."""
    return f"Szia {nev}! Ez a Renderen futó MCP szerverből jön."


@mcp.tool()
def osszead(a: float, b: float) -> float:
    """Összead két számot."""
    return a + b


@mcp.tool()
def get_weather(city: str) -> str:
#def get_weather(city: str) -> dict[str, str]:
    """Get the current temperature, humidity, and weather condition for a city."""
    # url = f"https://wttr.in/{quote(city)}?format=j1"
    # response = requests.get(url, timeout=10)
    # response.raise_for_status()

    # current = response.json()["current_condition"][0]
    print(f"Get weather for {city} (simulated response)")   
    return "aaa"
    # return {
    #     "city": city,
    #     "temperature_celsius": "20",
    #     "humidity": "60",
    #     "condition": "Sunny",
    # }



if __name__ == "__main__":
    import sys, traceback
    print("Indul a szerver...", flush=True)
    try:
        mcp.run(transport="streamable-http")
    except BaseException:
        traceback.print_exc()
        sys.stdout.flush()
        sys.exit(1)
