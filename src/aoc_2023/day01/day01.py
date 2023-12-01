from pathlib import Path

from aoc_2023.utils import format_ns


def parse_part1(raw_input: str) -> list[int]:
    """
    On each line, the calibration value can be found by combining the first digit and
    the last digit (in that order) to form a single two-digit number.
    """
    no_letters = [[c for c in line if c.isdigit()] for line in raw_input.splitlines()]
    return [
        int("".join([line[0], line[-1]]))
        if len(line) > 1
        else int("".join([line[0], line[0]]))
        for line in no_letters
    ]


def part1(input: list[int]) -> int:
    return sum(input)


def part2(line: str) -> int:
    """
    For a single line

    Designed for cases like 'eightwothree'; should produce '83'

    Start at the beginning of the line, look for a digit, then look for a text digit,
    then drop anything that isn't a digit
    """
    tdigits = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    seen: list[str] = []

    rem = line
    idx = 0
    while len(rem) > 0:
        idx += 1
        if idx == 100:
            raise AssertionError("Too many iterations")

        if rem[0].isdigit():
            seen.append(rem[0])
            rem = rem[1:]
            continue

        bflag = False
        for didx, d in enumerate(tdigits):
            if rem.startswith(d):
                seen.append(str(didx))
                rem = rem[1:]
                bflag = True
                break

        if bflag:
            continue

        # If reach this point, is not a digit or text digit
        rem = rem[1:]

    return (
        int("".join([seen[0], seen[-1]]))
        if len(seen) > 1
        else int("".join([seen[0], seen[0]]))
    )


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()

    input = parse_part1(raw_input)
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = part1(input)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2 = sum(part2(line) for line in raw_input.splitlines())
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
