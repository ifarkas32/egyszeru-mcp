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


# 10x10 maze matrix: 0 = free, 1 = wall, 2 = start point, 3 = end point
# Initial setup: everything is a wall, written out line by line
matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 3, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

PASSAGEWAY = 0
WALL = 1
START = 2
END = 3

CELL_NAMES = {
    PASSAGEWAY: "passageway",
    WALL: "wall",
    START: "start",
    END: "end",
}

# row/col offset for each direction
DIRECTIONS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

@mcp.tool()
def matrix_check_direction(
    row: int, col: int, direction: str
) -> str:
    """Return what lies one step in `direction` from (row, col)."""
    direction = direction.upper()
    if direction not in DIRECTIONS:
        raise ValueError(f"Invalid direction: {direction}. Use one of L, R, U, D.")

    d_row, d_col = DIRECTIONS[direction]
    new_row, new_col = row + d_row, col + d_col

    if not (0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0])):
        return "wall"  # treat out-of-bounds as a wall

    return CELL_NAMES[matrix[new_row][new_col]]

@mcp.tool()
def matrix_start_point() -> dict[str, int]:
    """Return the row and column of the start point in the maze matrix."""
    for row_index, row_values in enumerate(matrix):
        for col_index, cell_value in enumerate(row_values):
            if cell_value == START:
                return {"row": row_index, "col": col_index}
    raise ValueError("The maze matrix has no start point.")

@mcp.tool()
def matrix_directions() -> dict[str, list[int]]:
    """Return the row and column offsets for each maze direction."""
    return {
        direction: list(offset)
        for direction, offset in DIRECTIONS.items()
    }

@mcp.tool()
def matrix_cell_names() -> dict[int, str]:
    """Return the names assigned to each maze cell value."""
    return CELL_NAMES



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
