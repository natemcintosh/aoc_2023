from pathlib import Path

from aoc_2023.utils import format_ns

import numpy as np


def parse(raw_input: str) -> np.ndarray:
    "Convert '#' to True and '.' to False"
    return np.array(
        [
            [True if item == "#" else False for item in row]
            for row in raw_input.splitlines()
        ]
    )


def solve(arr: np.ndarray, spread_factor: int = 2) -> int:
    """
    Find indices of galaxies.
    Then find the inds of the rows and columns where there are no galaxies.
    Update the indices of all the galaxies based on the expansions
    For each pair, calculate taxi-cab distance
    """
    # Each row represents an axis in the original image array; rows, then columns
    pts = np.vstack(arr.nonzero())

    max_row, max_col = arr.shape

    empty_rows = np.setdiff1d(np.arange(max_row), pts[0, :])
    empty_cols = np.setdiff1d(np.arange(max_col), pts[1, :])

    to_add = np.zeros_like(pts)

    for er in empty_rows:
        to_add[0, pts[0, :] > er] += spread_factor - 1

    for ec in empty_cols:
        to_add[1, pts[1, :] > ec] += spread_factor - 1

    pts += to_add

    # This is a tuple. Each tuple represents one of the pair of two
    paired_inds = np.triu_indices(pts.shape[1], 1)
    pairs = np.stack((pts[:, paired_inds[0]], pts[:, paired_inds[1]]), axis=1)
    dists = pairs[:, 1, :] - pairs[:, 0, :]
    return np.linalg.norm(dists, ord=1, axis=1).sum(dtype=int)


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    arr = parse(raw_input)
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = solve(arr)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2 = solve(arr, spread_factor=1_000_000)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
