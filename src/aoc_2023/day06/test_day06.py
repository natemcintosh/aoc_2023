from math import prod

import pytest

from aoc_2023.day06.day06 import parse_p1, parse_p2, ways_to_win


races = [(7, 9, 4), (15, 40, 8), (30, 200, 9)]


@pytest.mark.parametrize("time, dist, want", races)
def test_analytic_ways_to_win(time, dist, want):
    got = ways_to_win(time, dist)
    assert want == got


def test_part1_real():
    raw_input = """Time:        51     69     98     78
Distance:   377   1171   1224   1505"""
    times, dists = parse_p1(raw_input)
    got = prod(ways_to_win(t, d) for t, d in zip(times, dists))
    want = 131376
    assert want == got


def test_part2_real():
    raw_input = """Time:        51     69     98     78
Distance:   377   1171   1224   1505"""
    time, dist = parse_p2(raw_input)
    got = ways_to_win(time, dist)
    want = 34123437
    assert want == got
