from pathlib import Path
from typing import NamedTuple

import polars as pl

from aoc_2023.utils import format_ns


class Instruction(NamedTuple):
    direction: str
    cnt: int
    hexcode: str

    @staticmethod
    def parse(line: str) -> "Instruction":
        direction, count, hexcode = line.split(maxsplit=2)
        return Instruction(
            direction=direction, cnt=int(count), hexcode=hexcode.strip("()")
        )


def dig_trench(instructions: list[Instruction]) -> pl.DataFrame:
    """
    Will have columns:
    - row
    - col
    - hexcolor
    """
    # Start the trench at row=0, col=0
    row = 0
    col = 0
    pts_visited: list[tuple[int, int, str]] = list()
    for inst in instructions:
        match inst.direction:
            case "R":
                pts_visited.extend([
                    (row, coli, inst.hexcode) for coli in range(col, col + inst.cnt)
                ])
                col += inst.cnt
            case "L":
                pts_visited.extend([
                    (row, coli, inst.hexcode) for coli in range(col, col - inst.cnt, -1)
                ])
                col -= inst.cnt
            case "U":
                pts_visited.extend([
                    (rowi, col, inst.hexcode) for rowi in range(row, row - inst.cnt, -1)
                ])
                row -= inst.cnt
            case "D":
                pts_visited.extend([
                    (rowi, col, inst.hexcode) for rowi in range(row, row + inst.cnt)
                ])
                row += inst.cnt

    return pl.DataFrame(
        data=pts_visited, schema=["row", "col", "hexcode"], orient="row"
    ).sort("row", "col")


def part1(lake_boundary: pl.DataFrame) -> int:
    """
    Count how many cubic meters of lava fit in the filled in shape described by the
    trech boundary.

    Find the rough center of the shape. Starting from there, find neighbors, and add
    them to `seen`.

    When an edge is found, add it to seen, but don't get its neighbors
    """
    # Where's the middle? (row, col)
    srow = int(lake_boundary["row"].mean())  # type: ignore
    scol = int(lake_boundary["col"].mean())  # type: ignore

    # What are the extremeties
    # rmax = lake_boundary["row"].max()
    # rmin = lake_boundary["row"].min()
    # cmax = lake_boundary["col"].max()
    # cmin = lake_boundary["col"].min()

    dirs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    # We've seen all the edges
    seen: set[tuple[int, int]] = set(zip(lake_boundary["row"], lake_boundary["col"]))

    # Initialize the frontier
    frontier: set[tuple[int, int]] = set(
        new_pt for d in dirs if (new_pt := (srow + d[0], scol + d[1])) not in seen
    )

    while len(frontier) > 0:
        # Add everything on the frontier to seen
        seen.update(frontier)

        # For each item on the frontier, if it's not an edge, and not already seen, add
        # its neighbors to the frontier. Here, the existing items are overwritten, bc
        # we already added them all to seen.
        frontier = set(
            pt
            for fpt in frontier
            for d in dirs
            if (pt := (fpt[0] + d[0], fpt[1] + d[1])) not in seen
        )

    return len(seen)


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    instructions = [Instruction.parse(line) for line in raw_input.splitlines()]
    trench = dig_trench(instructions)
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = part1(trench)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2_time = format_ns(perf_counter_ns() - p2_start)
    # print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
