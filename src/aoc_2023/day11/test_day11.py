from aoc_2023.day11.day11 import parse, solve

import pytest


def test_part1():
    raw_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    arr = parse(raw_input)
    got = solve(arr)
    want = 374
    assert want == got


p2_params = [(10, 1030), (100, 8410)]


@pytest.mark.parametrize("spread_factor, want", p2_params)
def test_part2(spread_factor, want):
    raw_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    arr = parse(raw_input)
    got = solve(arr, spread_factor)
    assert want == got
