from aoc_2023.day21.day21 import parse_arr, part1, to_1d

import pytest

tarr = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
params = [(3, ridx, cidx, tarr[ridx][cidx]) for ridx in range(3) for cidx in range(3)]


@pytest.mark.parametrize("n_cols, ridx, cidx, want", params)
def test_to_1d(n_cols, ridx, cidx, want):
    got = to_1d(n_cols, ridx, cidx)
    assert want == got


p1_params = [(1, 2), (2, 4), (3, 6), (6, 16)]


@pytest.mark.parametrize("n_steps, want", p1_params)
def test_part1(n_steps, want):
    raw_input = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    start_idx, arr = parse_arr(raw_input)
    got = part1(start_idx=start_idx, arr=arr, n_steps=n_steps)
    assert want == got
