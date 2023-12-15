from pathlib import Path

from aoc_2023.utils import format_ns


def HASH(s: str) -> int:
    """
    - Determine the ASCII code for the current character of the string.
    - Increase the current value by the ASCII code you just determined.
    - Set the current value to itself multiplied by 17.
    - Set the current value to the remainder of dividing itself by 256.
    """
    curr = 0
    for si in s:
        curr += ord(si)
        curr *= 17
        curr = curr % 256

    return curr


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    steps = [s for s in raw_input.strip().split(",")]
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = sum(HASH(step) for step in steps)
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
