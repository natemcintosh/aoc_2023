import pytest
from aoc_2023.day01.day01 import parse_part1, parse_part2, part1, convert_text_digits

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


p2_params = [
    ("two1nine", "219"),
    ("eightwothree", "8wo3"),
    ("abcone2threexyz", "abc123xyz"),
    ("xtwone3four", "x2ne34"),
    ("4nineeightseven2", "49872"),
    ("zoneight234", "z1ight234"),
    ("7pqrstsixteen", "7pqrst6teen"),
    ("fouronevhnrz44", "41vhnrz44"),
    ("eightg1", "8g1"),
    (
        "4ninejfpd1jmmnnzjdtk5sjfttvgtdqspvmnhfbm",
        "49jfpd1jmmnnzjdtk5sjfttvgtdqspvmnhfbm",
    ),
    ("78seven8", "7878"),
    ("6pcrrqgbzcspbd", "6pcrrqgbzcspbd"),
    ("7sevenseven", "777"),
    ("1threeeight66", "13866"),
]


@pytest.mark.parametrize("line, want", p2_params)
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


def test_part2_again():
    raw_input = """fouronevhnrz44
eightg1
4ninejfpd1jmmnnzjdtk5sjfttvgtdqspvmnhfbm
78seven8
6pcrrqgbzcspbd
7sevenseven
1threeeight66"""
    parsed = parse_part2(raw_input)
    print(parsed)
    want = sum([44, 81, 45, 78, 66, 77, 16])
    got = part1(parsed)
    assert want == got
