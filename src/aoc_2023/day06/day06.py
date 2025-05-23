from math import ceil, floor, prod, sqrt
from pathlib import Path

from aoc_2023.utils import format_ns


def parse_p1(raw_input: str) -> tuple[list[int], list[int]]:
    """
    input looks like

    Time:        51     69     98     78
    Distance:   377   1171   1224   1505
    """
    time, dist = raw_input.strip().split("\n", maxsplit=1)
    _, stimes = time.split(":", maxsplit=1)
    _, sdists = dist.split(":", maxsplit=1)

    times = [int(x) for x in stimes.strip().split()]
    dists = [int(x) for x in sdists.strip().split()]

    return times, dists


def parse_p2(raw_input: str) -> tuple[int, int]:
    time, dist = raw_input.strip().split("\n", maxsplit=1)
    _, stimes = time.split(":", maxsplit=1)
    _, sdists = dist.split(":", maxsplit=1)

    time = int(stimes.replace(" ", ""))
    dist = int(sdists.replace(" ", ""))

    return time, dist


def ways_to_win(time: int, record_distance: int) -> int:
    """
    We want values of charge_time that give us distances greater than record_distance

    solving:
    d < v*t - v*v
    where v is velocity (charge time)
    gives
    1/2 * (t - sqrt(t*t - 4d)) < v < 1/2 * (sqrt(t*t - 4d) + t)
    Thank you Wolfram Alpha

    So we can just find the integers between those two values, and count how many of
    them there are.
    """
    # Need to have the very small numbers in the equation so that if we end up with a
    # whole number, we do not include it. This is because of they are hard inequalities,
    # not <=
    gt = ceil(1 / 2 * (time - sqrt(time * time - 4 * record_distance)) + 1e-9)
    lt = floor(1 / 2 * (sqrt(time * time - 4 * record_distance) + time) - 1e-9)

    return lt - gt + 1


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()

    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    times, dists = parse_p1(raw_input)
    p1 = prod(ways_to_win(t, d) for t, d in zip(times, dists))
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    time, dist = parse_p2(raw_input)
    p2 = ways_to_win(time, dist)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
