"""Egyszerű távoli MCP szerver, Renderen futtatva.

Helyi teszt:  python server.py   ->  http://localhost:8000/mcp
"""
import os

from mcp.server.fastmcp import FastMCP

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


if __name__ == "__main__":
    # Streamable HTTP: a végpont az /mcp útvonalon érhető el
    mcp.run(transport="streamable-http")
