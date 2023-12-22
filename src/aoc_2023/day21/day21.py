from pathlib import Path

from aoc_2023.utils import format_ns

import numpy as np
import scipy.sparse


def parse_arr(raw_input: str) -> tuple[tuple[int, int], np.ndarray]:
    """
    raw_input looks like
    ...........
    .....###.#.
    .###.##..#.
    ..#.#...#..
    ....#.#....
    .##..S####.
    .##..#...#.
    .......##..
    .##.#.####.
    .##..##.##.
    ...........

    Starts at 'S'. Can only move onto '.'. 'S' is also a '.'

    Return position of 'S', and an array of booleans, True where you can go, and False
    otherwise.
    """
    # First find the start position
    start_pos = (-1, -1)
    for ridx, line in enumerate(raw_input.splitlines()):
        if "S" in line:
            cidx = line.index("S")
            start_pos = (ridx, cidx)
    if start_pos == (-1, -1):
        raise AssertionError("Could not find start position")

    # Create the array
    arr = np.array(
        [
            [True if c == "." else False for c in line]
            for line in raw_input.replace("S", ".").splitlines()
        ],
        dtype=bool,
    )

    return start_pos, arr


def to_1d(n_cols: int, ridx: int, cidx: int) -> int:
    """
    Convert a 2d index to a 1d index.
    """
    return (ridx * n_cols) + cidx


def part1(start_idx: tuple[int, int], arr: np.ndarray, n_steps: int = 64) -> int:
    """
    Want to know how many different places can be reached after n_steps.
    Assuming that you can only step onto array positions that are `True`.

    Try using Markov chains for this. Create a table `P`, where each row represents
    where you are coming from, and each column represents where you are going to.
    Then can use the property that Pn = a*P^n, where a is the starting state.
    """
    # Create the array P. Because each row represents a 2D index, use row-major indexing
    # to flatten the 2D indices to 1D
    side_len_P = np.prod(arr.shape)
    ncols = arr.shape[1]

    DIRS = (
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    )
    # For each element of arr, look at its neighbors. If a given neighbor is True, give
    # that idx a value
    rows: list[int] = []
    cols: list[int] = []
    vals: list[float] = []
    for ridx, row in enumerate(arr):
        for cidx, item in enumerate(row):
            for d in DIRS:
                try:
                    nbr_idx = (d[0] + ridx, d[1] + cidx)
                    if any(ni < 0 for ni in nbr_idx):
                        continue
                    nbr = arr[nbr_idx]
                    if nbr:
                        # Row represents where we're coming from
                        rows.append(to_1d(ncols, ridx, cidx))
                        # Column represents where we're going to
                        cols.append(to_1d(ncols, nbr_idx[0], nbr_idx[1]))
                        vals.append(0.99)
                except Exception:
                    continue

    P = scipy.sparse.coo_matrix(
        (vals, (rows, cols)), shape=(side_len_P, side_len_P)
    ).tocsc()

    # Create the start position
    a = np.zeros((1, side_len_P))
    a[0, to_1d(ncols, start_idx[0], start_idx[1])] = 1

    Pn = a @ sparse_mat_power(P, n_steps)

    return (Pn > 0).sum()


def sparse_mat_power(mat, power: int):
    result = mat.copy()
    for _ in range(power - 1):
        result = result @ mat

    return result


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    start_idx, arr = parse_arr(raw_input)
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = part1(start_idx, arr)
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
