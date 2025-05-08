from pathlib import Path

import pytest

from aoc_2023.day01.day01 import parse_part1, part1, part2

p1_params = [
    ("1abc2", [12]),
    ("pqr3stu8vwx", [38]),
    ("a1b2c3d4e5f", [15]),
    ("treb7uchet", [77]),
]


@pytest.mark.parametrize("line, want", p1_params)
def test_parse_part1(line, want):
    got = parse_part1(line)
    assert want == got


def test_part1():
    raw_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
    parsed = parse_part1(raw_input)
    print(parsed)
    got = part1(parsed)
    want = 142
    assert want == got


def test_part1_real():
    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    parsed = parse_part1(raw_input)
    print(parsed)
    got = part1(parsed)
    want = 54940
    assert want == got


@pytest.fixture
def p2_input() -> str:
    return """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def test_part2(p2_input):
    got = sum(part2(line) for line in p2_input.splitlines())
    want = 281
    assert want == got


def test_part2_edge_case():
    got = part2("oneight")
    want = 18
    assert want == got


def test_part2_real():
    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    got = sum(part2(line) for line in raw_input.splitlines())
    want = 54208
    assert want == got
