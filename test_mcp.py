"""Teszt a Renderen futó MCP szerverhez.

Futtatás:
    pip install -r requirements.txt
    python test_mcp.py
"""
import asyncio
import json

from mcp import Client

URL = "https://egyszeru-mcp.onrender.com/mcp"


def text_of(result):
    """A tool-hívás eredményéből kiszedi a szöveget."""
    return "".join(c.text for c in result.content if c.type == "text")


async def run_tests():
    async with Client(URL) as client:
        print(f"[OK] Kapcsolódva: {client.server_info.name}")

        # 2) Eszközök listája
        tools = await client.list_tools()
        names = [t.name for t in tools.tools]
        print(f"[OK] Eszközök: {names}")
        assert "koszon" in names, "Hiányzik a koszon eszköz"
        assert "osszead" in names, "Hiányzik az osszead eszköz"
        assert "verzio" in names, "Hiányzik a verzio eszköz"
        assert "matrix_check_direction" in names, (
            "Hiányzik a matrix_check_direction eszköz"
        )
        assert "matrix_start_point" in names, "Hiányzik a matrix_start_point eszköz"
        assert "matrix_directions" in names, "Hiányzik a matrix_directions eszköz"
        assert "matrix_cellNames" in names, "Hiányzik a matrix_cellNames eszköz"

        # 3) verzio eszköz hívása
        res = await client.call_tool("verzio", {})
        out = text_of(res)
        print(f"[OK] verzio -> {out}")
        assert int(out) == 1, f"Váratlan verzió: {out}"

        # 4) koszon eszköz hívása
        res = await client.call_tool("koszon", {"nev": "Peter"})
        out = text_of(res)
        print(f"[OK] koszon -> {out}")
        assert "Peter" in out, f"Váratlan válasz: {out}"

        # 5) osszead eszköz hívása
        res = await client.call_tool("osszead", {"a": 2, "b": 3})
        out = text_of(res)
        print(f"[OK] osszead(2, 3) -> {out}")
        assert float(out) == 5.0, f"Váratlan válasz: {out}"

        # 6) matrix_check_direction eszköz hívása
        res = await client.call_tool(
            "matrix_check_direction",
            {"row": 1, "col": 0, "direction": "R"},
        )
        out = text_of(res)
        print(f"[OK] matrix_check_direction -> {out}")
        assert out == "start", f"Váratlan irányeredmény: {out}"

        # 7) matrix_start_point eszköz hívása
        res = await client.call_tool("matrix_start_point", {})
        out = text_of(res)
        start_point = json.loads(out)
        print(f"[OK] matrix_start_point -> {start_point}")
        assert start_point == {"row": 1, "col": 1}, (
            f"Váratlan kezdőpont: {start_point}"
        )

        # 8) matrix_directions eszköz hívása
        res = await client.call_tool("matrix_directions", {})
        out = text_of(res)
        directions = json.loads(out)
        expected_directions = {
            "U": [-1, 0],
            "D": [1, 0],
            "L": [0, -1],
            "R": [0, 1],
        }
        print(f"[OK] matrix_directions -> {directions}")
        assert directions == expected_directions, (
            f"Váratlan irányok: {directions}"
        )

        # 9) matrix_cellNames eszköz hívása
        res = await client.call_tool("matrix_cellNames", {})
        out = text_of(res)
        cell_names = json.loads(out)
        expected_cell_names = {
            "0": "passageway",
            "1": "wall",
            "2": "start",
            "3": "end",
        }
        print(f"[OK] matrix_cellNames -> {cell_names}")
        assert cell_names == expected_cell_names, (
            f"Váratlan cellanevek: {cell_names}"
        )

        # 10) get_weather eszköz hívása
        res = await client.call_tool("get_weather", {"city": "Budapest"})
        assert not res.is_error, f"A get_weather hívás sikertelen: {text_of(res)}"
        out = text_of(res)
        weather = json.loads(out)
        print(f"[OK] get_weather(Budapest) -> {weather}")
        assert isinstance(weather, dict), f"Váratlan válaszformátum: {weather}"
        assert weather["city"] == "Budapest", f"Váratlan város: {weather}"
        for field in ("temperature_celsius", "humidity", "condition"):
            assert isinstance(weather[field], str) and weather[field], (
                f"Hiányzó vagy hibás {field}: {weather}"
            )
    print("\nMinden teszt sikeres.")


async def main():
    # A Render Free csomag elalszik, az első kapcsolódás lassú vagy sikertelen lehet
    for attempt in range(1, 4):
        try:
            await asyncio.wait_for(run_tests(), timeout=90)
            return
        except Exception as e:
            print(f"[{attempt}/3] Hiba: {type(e).__name__}: {e}")
            if attempt == 3:
                raise
            print("Újrapróbálom 20 másodperc múlva (a szerver talán ébredezik)...")
            await asyncio.sleep(20)


if __name__ == "__main__":
    asyncio.run(main())
