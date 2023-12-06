from math import prod

from aoc_2023.day06.day06 import parse, parse_p2, part2, ways_to_win


def test_part1_real():
    raw_input = """Time:        51     69     98     78
Distance:   377   1171   1224   1505"""
    times, dists = parse(raw_input)
    got = prod(ways_to_win(t, d) for t, d in zip(times, dists))
    want = 131376
    assert want == got


def test_part2_real():
    raw_input = """Time:        51     69     98     78
Distance:   377   1171   1224   1505"""
    time, dist = parse_p2(raw_input)
    got = part2(time, dist)
    want = 34123437
    assert want == got
