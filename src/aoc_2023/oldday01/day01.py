import heapq
from pathlib import Path

from aoc_2023.utils import format_ns


def parse(raw_input: str) -> list[list[int]]:
    """
    Lines look like:

    1000
    2000
    3000

    4000

    5000
    6000

    want each group of numbers in their own list
    """
    elves = raw_input.split("\n\n")
    str_snacks = [snacks.splitlines() for snacks in elves]
    return [[int(snack) for snack in snacks] for snacks in str_snacks]


def part1(snacks: list[list[int]]) -> int:
    """
    In case the Elves get hungry and need extra snacks, they need to know which Elf to
    ask: they'd like to know how many Calories are being carried by the Elf carrying the
    most Calories. In the example above, this is 24000 (carried by the fourth Elf).

    Find the Elf carrying the most Calories. How many total Calories is that Elf
    carrying?
    """
    return max(sum(s) for s in snacks)


def part2(snacks: list[list[int]]) -> int:
    """
    Find the top three Elves carrying the most Calories. How many Calories are those
    Elves carrying in total?
    """
    return sum(heapq.nlargest(3, [sum(s) for s in snacks]))


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
    p2 = part2(input)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
