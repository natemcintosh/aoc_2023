import re
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Callable

from more_itertools import chunked
from tqdm import tqdm

from aoc_2023.utils import format_ns


def p1_seed_parser(seed_line: str) -> list[int]:
    str_seeds = seed_line.split(":", maxsplit=1)[-1].strip().split()
    return [int(s) for s in str_seeds]


def p2_seed_parser(seed_line: str) -> list[range]:
    str_seeds = seed_line.split(":", maxsplit=1)[-1].strip().split()
    nums = [int(s) for s in str_seeds]
    return [range(x, x + y) for x, y in chunked(nums, 2)]


def parse(raw_input: str, seed_mapper: Callable = p1_seed_parser):
    """
    Example input looks like:
    seeds: 79 14 55 13

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
    56 93 4

    Where each number triplet corresponds to:
    - destination start
    - source start
    - range length
    """
    parts = raw_input.split("\n\n")
    seed_line = parts[0]
    seeds = seed_mapper(seed_line)

    return seeds, [parse_mapping(m) for m in parts[1:]]


@dataclass
class Mapping:
    source: str
    dest: str
    mapping: dict[range, range]

    def get(self, x: int) -> int:
        for s, d in self.mapping.items():
            if x in s:
                offset: int = x - s[0]
                return d[0] + offset
        return x


def parse_mapping(s: str) -> Mapping:
    """
    A mapping looks like this in text form:
    temperature-to-humidity map:
    0 69 1
    1 0 69
    """
    lines = s.splitlines()
    m = re.findall(r"(\w+)-to-(\w+) map:$", lines[0])
    source = m[0][0]
    dest = m[0][1]
    nums = [[int(s) for s in line.split()] for line in lines[1:]]
    mappings = {range(l[1], l[1] + l[2]): range(l[0], l[0] + l[2]) for l in nums}
    return Mapping(source=source, dest=dest, mapping=mappings)


def get_seed_location(seed: int, mappings: list[Mapping]) -> int:
    """
    The mappings are in order, so use the output of one as the input of the next
    """
    x = seed
    for m in mappings:
        x = m.get(x)
    return x


def part2(seeds: list[range], maps: list[Mapping]) -> int:
    smallest = 1_000_000_000
    total_iterations = sum(len(s) for s in seeds)
    with tqdm(total=total_iterations) as pbar:
        for r in seeds:
            for seed in r:
                x = get_seed_location(seed, maps)
                smallest = min(smallest, x)
                pbar.update()

    return smallest


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    seeds1, maps = parse(raw_input)
    seeds2, maps = parse(raw_input, seed_mapper=p2_seed_parser)

    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = min(get_seed_location(seed, maps) for seed in seeds1)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2 = part2(seeds2, maps)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
