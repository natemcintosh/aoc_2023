from aoc_2023.day24.day24 import parse, part1


def test_part1():
    raw_input = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    pos, vel = parse(raw_input)
    want = 2
    got = part1(pos, vel, (7, 27))
    assert want == got
