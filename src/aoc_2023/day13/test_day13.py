import pytest

from aoc_2023.day13.day13 import (
    parse_arr,
    find_vert_reflection,
    find_horz_reflection,
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
    got = find_vert_reflection(arr)
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
