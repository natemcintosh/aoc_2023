from aoc_2023.day03.day03 import parse, solve, Type


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
    all_part_symbols: set[str] = set(
        item.value for item in input if item.typ == Type.Part
    )
    got, _ = solve(input, all_part_symbols)
    assert want == got


def test_part2():
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
    want = 467835
    keep_parts = {"*"}
    _, got = solve(input, keep_parts)
    assert want == got
