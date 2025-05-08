from pathlib import Path

import pytest

from aoc_2023.day02.day02 import RGB, parse_game, part1, smallest_RGB

params = [
    (
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        [RGB(r=4, g=0, b=3), RGB(r=1, g=2, b=6), RGB(g=2)],
    ),
    (
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        [RGB(b=1, g=2), RGB(g=3, b=4, r=1), RGB(b=1, g=1)],
    ),
    (
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        [RGB(g=8, b=6, r=20), RGB(b=5, r=4, g=13), RGB(g=5, r=1)],
    ),
    (
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        [RGB(g=1, r=3, b=6), RGB(g=3, r=6), RGB(g=3, b=15, r=14)],
    ),
    (
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
        [RGB(r=6, b=1, g=3), RGB(b=2, r=1, g=2)],
    ),
]


@pytest.mark.parametrize("game, want", params)
def test_parse(game, want):
    got = parse_game(game)
    assert want == got


def test_part1():
    raw_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    games = [parse_game(game) for game in raw_input.splitlines()]
    got = part1(games)
    want = 8
    assert want == got


def test_part1_real():
    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    games = [parse_game(game) for game in raw_input.splitlines()]
    got = part1(games)
    want = 2449
    assert want == got


def test_part2():
    raw_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    games = [parse_game(game) for game in raw_input.splitlines()]
    got = sum(smallest_RGB(game).power() for game in games)
    want = 2286
    assert want == got


def test_part2_real():
    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    games = [parse_game(game) for game in raw_input.splitlines()]
    got = sum(smallest_RGB(game).power() for game in games)
    want = 63981
    assert want == got
