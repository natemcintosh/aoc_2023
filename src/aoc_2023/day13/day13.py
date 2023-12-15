from math import floor
from pathlib import Path

import numpy as np

from aoc_2023.utils import format_ns


def parse_arr(sarr: str) -> np.ndarray:
    return np.array(
        [[1 if c == "#" else 0 for c in row] for row in sarr.splitlines()],
        dtype=np.uint8,
    )


def find_vert_reflection(arr: np.ndarray) -> int:
    """
    If there is a vertical reflection, return the number of columns to the left of the
    reflection line.

    If no vertical reflection, return 0
    """
    # For each column
    for cidx in range(arr.shape[1] - 2):
        # What's the min number of columns on either side?
        ncols = min(cidx + 1, arr.shape[1] - cidx - 1)
        left = np.fliplr(arr[:, cidx - ncols + 1 : cidx + 1])
        right = arr[:, cidx + 1 : cidx + 1 + ncols]
        if np.equal(left, right).all():
            return ncols + 1

    return 0


def find_horz_reflection(arr: np.ndarray) -> int:
    """
    If there is a horizontal reflection, return the number of rows to the left of the
    reflection line.

    If no horizontal reflection, return 0
    """
    # For each column
    for ridx in range(arr.shape[0] - 2):
        # What's the min number of rows on either side?
        nrows = min(ridx + 1, arr.shape[0] - ridx - 1)
        top = np.flipud(arr[ridx - nrows + 1 : ridx + 1, :])
        btm = arr[ridx + 1 : ridx + 1 + nrows, :]
        if np.equal(top, btm).all():
            return nrows + 1

    return 0


def part1(arrays: list[np.ndarray]) -> int:
    total = 0
    for arr in arrays:
        total += find_vert_reflection(arr)
        total += 100 * find_horz_reflection(arr)

    return total


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    arrays = [parse_arr(sarr) for sarr in raw_input.split("\n\n")]
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
