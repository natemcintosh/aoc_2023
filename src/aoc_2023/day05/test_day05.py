from pathlib import Path

import pytest

from aoc_2023.day05.day05 import (
    Mapping,
    get_seed_location,
    p2_seed_parser,
    parse,
    parse_mapping,
)


class Test_parse_mapping:
    def test_pm1(self):
        input = """light-to-temperature map:
45 77 23
81 45 19
68 64 13"""
        want = Mapping(
            source="light",
            dest="temperature",
            mapping={
                range(77, 77 + 23): range(45, 45 + 23),
                range(45, 45 + 19): range(81, 81 + 19),
                range(64, 64 + 13): range(68, 68 + 13),
            },
        )
        got = parse_mapping(input)
        assert want == got

    def test_pm2(self):
        input = """soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15"""
        want = Mapping(
            source="soil",
            dest="fertilizer",
            mapping={
                range(15, 15 + 37): range(0, 0 + 37),
                range(52, 52 + 2): range(37, 37 + 2),
                range(0, 0 + 15): range(39, 39 + 15),
            },
        )
        got = parse_mapping(input)
        assert want == got


get_params = [(15, 0), (16, 1), (0, 39), (100, 100)]


@pytest.mark.parametrize("x, want", get_params)
def test_get(x, want):
    m = Mapping(
        source="soil",
        dest="fertilizer",
        mapping={
            range(15, 15 + 37): range(0, 0 + 37),
            range(52, 52 + 2): range(37, 37 + 2),
            range(0, 0 + 15): range(39, 39 + 15),
        },
    )
    got = m.get(x)
    assert want == got


@pytest.fixture
def example_text():
    return """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def test_part1(example_text):
    seeds, maps = parse(example_text)
    want = 35
    got = min(get_seed_location(seed, maps) for seed in seeds)
    assert want == got


def test_part1_real():
    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    seeds, maps = parse(raw_input)
    got = min(get_seed_location(seed, maps) for seed in seeds)
    want = 340994526
    assert want == got


def test_part2(example_text):
    seeds, maps = parse(example_text, seed_mapper=p2_seed_parser)
    print(seeds)
    got = min(get_seed_location(seed, maps) for r in seeds for seed in r)
    want = 46
    assert want == got
