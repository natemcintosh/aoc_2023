import pytest
from aoc_2023.day01.day01 import parse_part2, part1, convert_text_digits


params = [
    ("two1nine", "219"),
    ("eightwothree", "8wo3"),
    ("abcone2threexyz", "123"),
    ("xtwone3four", "234"),
]


@pytest.mark.parametrize("line, want", params)
def test_convert_text_digits(line, want):
    got = convert_text_digits(line)
    assert want == got


def test_part2():
    raw_input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    parsed = parse_part2(raw_input)
    print(parsed)
    want = 281
    got = part1(parsed)
    assert want == got
