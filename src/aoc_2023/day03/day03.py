import re
from pathlib import Path
from dataclasses import dataclass
from math import prod
from enum import Enum


from aoc_2023.utils import format_ns


class Type(Enum):
    Part = 1
    Number = 2


@dataclass(frozen=True)
class Item:
    value: str
    typ: Type
    inds: tuple[tuple[int, int], ...]


def parse(raw_input: str) -> list[Item]:
    """
    Input looks like

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

    Going line by line, find the pattern of a symbol or multiple digits
    For each match, create an `Item` object
    """
    items: list[Item] = []
    pat = re.compile(r"([#|$|%|&|*|+|\-|/|=|@]|\d+)")

    for row, line in enumerate(raw_input.splitlines()):
        for m in pat.finditer(line):
            t = Type.Number if m.group().isdigit() else Type.Part
            inds = tuple((row, col) for col in range(m.start(), m.end()))
            items.append(Item(value=m.group(), typ=t, inds=inds))

    return items


def solve(items: list[Item], keep_parts: set[str]) -> tuple[int, int]:
    """
    Once we have a list of all the Items, iterate over just the Parts, and find their
    Number neighbors. Then add the values of the number neighbors

    First returned item is for part 1, second item is for part 2
    """
    # Create a dictionary mapping from index to number
    numbers = {idx: i for i in items for idx in i.inds if i.typ == Type.Number}

    DIRS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    seen: list[Item] = []

    total = 0
    gear_ratio = 0
    for item in items:
        # Only examine symbols we care about
        if (item.typ == Type.Number) or (item.value not in keep_parts):
            continue

        # Don't use anything from previous iteration
        seen.clear()

        # For each possible direction
        for d in DIRS:
            # If the neighbor is a number we know of
            if (
                neighbor := (d[0] + item.inds[0][0], d[1] + item.inds[0][1])
            ) in numbers:
                # Check if we've already added this number for this symbol
                n = numbers[neighbor]
                if n in seen:
                    continue
                else:
                    seen.append(n)
                    total += int(n.value)

        # Calculate the gear ratio if there's more than one number
        gr = prod(int(s.value) for s in seen) if len(seen) > 1 else 0
        gear_ratio += gr

    return total, gear_ratio


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    input = parse(raw_input)

    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Both Parts ===================================================================
    p1_start = perf_counter_ns()
    all_part_symbols: set[str] = set(
        item.value for item in input if item.typ == Type.Part
    )
    p1, p2 = solve(input, keep_parts=all_part_symbols)
    solve_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")
    print(f"Part 1: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Solving both took {solve_time}")
