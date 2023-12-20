from aoc_2023.day18.day18 import Instruction, dig_trench, part1


def test_part1():
    raw_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
    instructions = [Instruction.parse(line) for line in raw_input.splitlines()]
    df = dig_trench(instructions)
    got = part1(df)
    want = 62
    assert want == got
