from pathlib import Path

from aoc_2023.day08.day08 import parse, part1, part2


def test_part1_real():
    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    dirs, maps = parse(raw_input)
    got = part1(dirs, maps)
    want = 12643
    assert want == got


def test_part2():
    raw_input = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    dirs, maps = parse(raw_input)
    got = part2(dirs, maps)
    want = 6
    assert want == got


def test_part2_real():
    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    dirs, maps = parse(raw_input)
    got = part2(dirs, maps)
    want = 13133452426987
    assert want == got
