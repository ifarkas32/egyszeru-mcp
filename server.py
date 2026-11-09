"""Egyszerű távoli MCP szerver, Renderen futtatva.

Helyi teszt:  python server.py   ->  http://localhost:8000/mcp
"""
import os
from urllib.parse import quote

from mcp.server import MCPServer
import requests

# A Render a PORT környezeti változóban adja meg a portot, és 0.0.0.0-n kell hallgatni
mcp = MCPServer("egyszeru-mcp")

@mcp.tool()
def verzio() -> int:
    """Visszaadja a szerver verziószámát."""
    return 1

@mcp.tool()
def koszon(nev: str) -> str:
    """Üdvözli a megadott nevű embert."""
    return f"Szia {nev}! Ez a Renderen futó MCP szerverből jön."


@mcp.tool()
def osszead(a: float, b: float) -> float:
    """Összead két számot."""
    return a + b

@mcp.tool()
def get_weather(city: str) -> dict[str, str]:
    url = f"https://wttr.in/{quote(city)}?format=j1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    current = response.json()["current_condition"][0]
    #print(f"eee1:{response.json()}")
    #print(f"eee2:{len(response.json()["current_condition"])}")
    #print(f"eee3:{response.json()["current_condition"][0]}")
    #print(f"eee4:{response.json()["current_condition"][0].keys()}")
    print(f"eee4:{current["temp_C"]}")
    return {
        "city": city,
        "temperature_celsius": current["temp_C"],
        "humidity": current["humidity"],
        "condition": current["weatherDesc"][0]["value"],
    }

# @mcp.tool()
# def get_weather(city: str) -> dict[str, str]:
#     """Get the current temperature, humidity, and weather condition for a city."""
#     print(f"1Get weather for {city}...")
#     url = f"https://wttr.in/{quote(city)}?format=j1"
#     print(f"2Get weather for {city}...")
#     response = requests.get(url, timeout=10)
#     print(f"3Get weather for {city}...")
#     response.raise_for_status()
#     print(f"4Get weather for {city}...")

#     current = response.json()["current_condition"][0]
#     print(f"5Get weather for {city}... {response.json()}")
#     return {
#         "city": city,
#         "temperature_celsius": current["temp_C"],
#         "humidity": current["humidity"],
#         "condition": current["weatherDesc"][0]["value"],
#     }



if __name__ == "__main__":
    import sys, traceback
    print("Indul a szerver...", flush=True)
    try:
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8000)),
        )
    except BaseException:
        traceback.print_exc()
        sys.stdout.flush()
        sys.exit(1)
