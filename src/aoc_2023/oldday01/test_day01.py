from pathlib import Path

import pytest

from aoc_2023.oldday01.day01 import parse, part1, part2


@pytest.fixture
def test_input() -> list[list[int]]:
    return [[1000, 2000, 3000], [4000], [5000, 6000], [7000, 8000, 9000], [10000]]


def test_parse(test_input):
    raw_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
    got = parse(raw_input)
    assert test_input == got


def test_part1(test_input):
    got = part1(test_input)
    want = 24000
    assert want == got


def test_part1_real(test_input):
    raw_input = (Path(__file__).parent / "input.txt").read_text()
    snacks = parse(raw_input)
    got = part1(snacks)
    want = 69836
    assert want == got


def test_part2(test_input):
    got = part2(test_input)
    want = 45000
    assert want == got


def test_part2_real():
    raw_input = (Path(__file__).parent / "input.txt").read_text()
    snacks = parse(raw_input)
    got = part2(snacks)
    want = 207968
    assert want == got
