import functools
from pathlib import Path

from aoc_2023.utils import format_ns

import numpy as np

np.seterr(divide="ignore")

# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection


def parse_line(line: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    spos, svel = line.split("@", maxsplit=1)
    pos = tuple(int(x) for x in spos.split(",", maxsplit=2))
    vel = tuple(int(x) for x in svel.split(",", maxsplit=2))
    return pos, vel  # type: ignore


def parse(raw_input: str) -> tuple[np.ndarray, np.ndarray]:
    """
    input looks like many rows of
    176253337504656, 321166281702430, 134367602892386 @ 190, 8, 338
    Before the '@' is position, after is velocity

    Return two nx3 arrays, first for position, second for velocity
    """
    pos: list[tuple[int, int, int]] = []
    vel: list[tuple[int, int, int]] = []

    for line in raw_input.splitlines():
        p, v = parse_line(line)
        pos.append(p)
        vel.append(v)

    return np.array(pos, order="F"), np.array(vel, order="F")


def calc_ray_intersections(pos: np.ndarray, vel: np.ndarray) -> np.ndarray:
    """
    Input arrays are nx3. For the 2D case, ignore the 3rd column.

    Calculate slope for each line, m.

    For any pair, calculate the x-crossing with
    x = (m1*x1 - m2*x2 + y2 - y1) / (m1 - m2)
    plug that value into
    y = m1*(x - x1) + y1
    """
    # Calculte the 2D slope
    ms = vel[:, 1] / vel[:, 0]

    # Calculate components
    mx = ms * pos[:, 0]

    # Get indices of all pairs. `idx1` is an array of all the first items, and `idx2` is
    # an array of all the second items.
    idx1, idx2 = np.triu_indices(mx.shape[0], k=1)

    # Calculate m1*x1 - m2*x2. Note 1 - 2
    term1 = mx[idx1] - mx[idx2]

    # Calculate y2 - y1. Note 2 - 1
    term2 = pos[:, 1][idx2] - pos[:, 1][idx1]

    # Calculate m1 - m2. Note 1 - 2
    denom = ms[idx1] - ms[idx2]

    # Calculate x
    x = (term1 + term2) / denom

    # Calculate y
    y = ms[idx1] * (x - pos[:, 0][idx1]) + pos[:, 1][idx1]

    xings = np.stack((x, y), axis=1)

    # When vel is negative, pos must be >= intersections
    x_vel_is_neg = vel[:, 0] < 0
    x_vel_is_pos = vel[:, 0] > 0
    y_vel_is_neg = vel[:, 1] < 0
    y_vel_is_pos = vel[:, 1] > 0

    # When x vel is negative, x pos must be >= x intersections
    x_valid_neg_xings = np.logical_and(
        (x_vel_is_neg[idx1] & (pos[:, 0][idx1] >= x)),
        (x_vel_is_neg[idx2] & (pos[:, 0][idx2] >= x)),
    )

    # When x vel is positive, x pos must be <= x intersections
    x_valid_pos_xings = np.logical_and(
        (x_vel_is_pos[idx1] & (pos[:, 0][idx1] <= x)),
        (x_vel_is_pos[idx2] & (pos[:, 0][idx2] <= x)),
    )

    # When y vel is negative, y pos must be >= y intersections
    y_valid_neg_xings = np.logical_and(
        (y_vel_is_neg[idx1] & (pos[:, 1][idx1] >= y)),
        (y_vel_is_neg[idx2] & (pos[:, 1][idx2] >= y)),
    )

    # When y vel is positive, y pos must be <= y intersections
    y_valid_pos_xings = np.logical_and(
        (y_vel_is_pos[idx1] & (pos[:, 1][idx1] <= y)),
        (y_vel_is_pos[idx2] & (pos[:, 1][idx2] <= y)),
    )

    valid_ray_xings = functools.reduce(
        np.logical_or,
        [x_valid_neg_xings, x_valid_pos_xings, y_valid_neg_xings, y_valid_pos_xings],
    )

    xings[np.logical_not(valid_ray_xings), :] = np.inf
    return xings


def part1(pos: np.ndarray, vel: np.ndarray, minmax: tuple[int, int]) -> int:
    """
    How many crossing points in the box defined by the min and max in the x and y
    directions.
    """
    mn, mx = minmax
    xings = calc_ray_intersections(pos, vel)

    # Are crossings on the right side of the rays?
    # For each pair on rays, if the x velocity is negative, then x-crossing must be less
    # than x position. If the x position

    return (
        (xings[:, 0] >= mn)
        & (xings[:, 0] <= mx)
        & (xings[:, 1] >= mn)
        & (xings[:, 1] <= mx)
    ).sum()


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    pos, vel = parse(raw_input)
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = part1(pos, vel, minmax=(200000000000000, 400000000000000))
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
