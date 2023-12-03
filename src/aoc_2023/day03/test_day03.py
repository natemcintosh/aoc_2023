from aoc_2023.day03.day03 import parse, part1


def test_part1():
    raw_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    input = parse(raw_input)
    want = 4361
    got = part1(input)
    assert want == got
