import numpy as np
import pytest

from aoc_2023.day13.day13 import (
    find_horz_reflection,
    parse_arr,
    part1,
)

varrays = [
    (
        parse_arr(
            """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""
        ),
        5,
    ),
    (
        parse_arr(
            """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        ),
        0,
    ),
]


@pytest.mark.parametrize("arr, want", varrays)
def test_find_vert_reflection(arr, want):
    got = find_horz_reflection(np.rot90(arr, k=-1))
    assert want == got


harrays = [
    (
        parse_arr(
            """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""
        ),
        0,
    ),
    (
        parse_arr(
            """#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        ),
        4,
    ),
    (
        np.array(
            [
                [1, 1, 0, 1, 1, 1, 0],
                [0, 0, 1, 0, 1, 0, 1],
                [1, 1, 0, 1, 1, 1, 0],
                [1, 1, 1, 1, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 0, 1],
                [1, 1, 0, 1, 1, 1, 0],
                [0, 0, 1, 0, 1, 0, 1],
                [1, 1, 0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1, 0, 0],
                [1, 0, 1, 1, 1, 0, 0],
                [1, 0, 1, 1, 1, 0, 0],
            ]
        ),
        12,
    ),
]


@pytest.mark.parametrize("arr, want", harrays)
def test_find_horz_reflection(arr, want):
    got = find_horz_reflection(arr)
    assert want == got


def test_part1():
    raw_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    arrays = [parse_arr(arr) for arr in raw_input.split("\n\n")]
    got = part1(arrays)
    want = 405
    assert want == got
