from pathlib import Path

from aoc_2023.utils import format_ns


def parse_part1(raw_input: str) -> list[int]:
    """
    On each line, the calibration value can be found by combining the first digit and
    the last digit (in that order) to form a single two-digit number.
    """
    no_letters = [[c for c in line if c.isdigit()] for line in raw_input.splitlines()]
    return [int("".join([line[0], line[-1]])) for line in no_letters]


def part1(input: list[int]) -> int:
    return sum(input)


def convert_text_digits(line: str) -> str:
    """
    For a single line

    Designed for cases like 'eightwo' -> '8wo' not 'eigh2'

    For each possible text digits, from longest to shortest, look for it at the
    beginning.
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
    seen_digits: list[str] = []

    # for lidx, c in enumerate(line):
    #     if c.isdigit():
    #         seen_digits.append(c)
    #         continue

    #     for d in tdigits:
    #         if line[lidx:].startswith(d):
    #             seen_digits.append(dmap[d])
    #             break
    rem = line
    idx = 0
    while len(rem) > 0:
        idx += 1
        if idx == 100:
            raise AssertionError("Too many iterations")
        print("start", rem, seen_digits)
        if rem[0].isdigit():
            seen_digits.append(rem[0])
            rem = rem[1:]
            print("found digit", rem, seen_digits)
            continue

        for didx, d in enumerate(tdigits):
            if rem.startswith(d):
                seen_digits.append(str(didx))
                rem = rem[len(d) :]
                print("found text digit", rem, seen_digits)
                continue

        # If reach this point, is not a digit or text digit, skip it
        rem = rem[1:]

    return "".join(seen_digits)


def parse_part2(raw_input: str) -> list[int]:
    """
    our calculation isn't quite right. It looks like some of the digits are actually
    spelled out with letters: one, two, three, four, five, six, seven, eight, and nine
    also count as valid "digits".

    Equipped with this new information, you now need to find the real first and last
    digit on each line.
    """
    # Replace every occurence of a text digit with an actual digit
    # But have to do it in order. 'eightwo' has to be changed into '8wo' not 'eigh2'
    fix_raw = "\n".join([convert_text_digits(line) for line in raw_input.splitlines()])

    return parse_part1(fix_raw)


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
    p2 = part1(parse_part2(raw_input))
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
