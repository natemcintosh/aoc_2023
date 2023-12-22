from pathlib import Path

import numpy as np

from aoc_2023.utils import format_ns


def parse_arr(sarr: str) -> np.ndarray:
    return np.array(
        [[1 if c == "#" else 0 for c in row] for row in sarr.splitlines()],
        dtype=np.uint8,
    )


def find_horz_reflection(arr: np.ndarray) -> int:
    """
    If there is a horizontal reflection, return the number of rows to the left of the
    reflection line.

    If no horizontal reflection, return 0
    """
    # For each row. Don't need to do the last row because we'll have already compared
    # the second last to the last
    for ridx in range(arr.shape[0] - 1):
        top = np.flipud(arr[: ridx + 1, :])
        btm = arr[ridx + 1 :, :]

        nrows = min(top.shape[0], btm.shape[0])

        if np.equal(top[:nrows, :], btm[:nrows, :]).all():
            return top.shape[0]

    return 0


def part1(arrays: list[np.ndarray]) -> int:
    total = 0
    for arr in arrays:
        # If there is a horizontal component, add it
        horz = find_horz_reflection(arr)
        if horz > 0:
            total += horz * 100
        else:
            # Otherwise, rotate so the columns on the left become rows on top
            vert = find_horz_reflection(np.rot90(arr, k=-1))
            assert vert > 0, f"Found one with no reflection: {arr.tolist()}"
            total += vert

    return total


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    arrays = [parse_arr(sarr) for sarr in raw_input.strip().split("\n\n")]
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = part1(arrays)
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
