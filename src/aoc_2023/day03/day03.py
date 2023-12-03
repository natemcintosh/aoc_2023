import re
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


from aoc_2023.utils import format_ns


class Type(Enum):
    Part = 1
    Number = 2


@dataclass
class Item:
    value: str
    typ: Type
    inds: list[tuple[int, int]]


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
    pat = re.compile(r"([#|$|%|&|*|+|-|/|=|@]|\d+)")

    for row, line in enumerate(raw_input.splitlines()):
        for m in pat.finditer(line):
            t = Type.Number if m.group().isdigit() else Type.Part
            inds = [(row, col) for col in range(m.start(), m.end())]
            items.append(Item(value=m.group(), typ=t, inds=inds))

    return items


def part1(items: list[Item]) -> int:
    """
    Once we have a list of all the Items, iterate over just the Parts, and find their
    Number neighbors. Then add the values of the number neighbors
    """
    # Create a dictionary mapping from index to number
    numbers: dict[tuple[int, int], int] = {
        idx: int(i.value) for i in items for idx in i.inds if i.typ == Type.Number
    }

    DIRS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    total = 0
    for item in items:
        # Only examine symbols
        if item.typ == Type.Number:
            continue

        # A list of seen row number and number pairs
        seen: list[tuple[int, int]] = []
        # It is a symbol. Look in the row above, this row, and the row below for numbers
        for d in DIRS:
            if (
                neighbor := (d[0] + item.inds[0][0], d[1] + item.inds[0][1])
            ) in numbers:
                # Check if we've already added this number for this symbol
                n = numbers[neighbor]
                if (neighbor[0], n) in seen:
                    continue
                else:
                    seen.append((neighbor[0], n))
                    total += n

    return total


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    input = parse(raw_input)

    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = part1(input)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    # p2 = sum(smallest_RGB(game).power() for game in games)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    # print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
