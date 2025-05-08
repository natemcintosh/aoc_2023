import itertools
import math
import re
from pathlib import Path

from aoc_2023.utils import format_ns


def parse(raw_input: str) -> tuple[list[int], dict[str, tuple[str, str]]]:
    """
    input looks like

    RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)

    Convert 'R' to 1, and 'L' to 0 so we can use indexing
    """
    sdirs, smaps = raw_input.split("\n\n", maxsplit=1)

    dirs = [int(d) for d in sdirs.replace("L", "0").replace("R", "1")]

    pat = re.compile(r"(\w\w\w) = \((\w\w\w), (\w\w\w)\)")

    maps = {m[1]: (m[2], m[3]) for m in pat.finditer(smaps)}

    return dirs, maps


def part1(dirs: list[int], maps: dict[str, tuple[str, str]]) -> int:
    """
    Starting with AAA, you need to look up the next element based on the next left/right
    instruction in your input. In this example, start with AAA and go right (R) by
    choosing the right element of AAA, CCC. Then, L means to choose the left element of
    CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

    Of course, you might not find ZZZ right away. If you run out of left/right
    instructions, repeat the whole sequence of instructions as necessary: RL really
    means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6
    steps to reach ZZZ:

    LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)

    Starting at AAA, follow the left/right instructions. How many steps are required to
    reach ZZZ?
    """
    steps = 0
    curr = "AAA"
    for d in itertools.chain.from_iterable(itertools.repeat(dirs)):
        steps += 1
        curr: str = maps[curr][d]
        if curr == "ZZZ":
            return steps

        if steps == 100_000:
            raise AssertionError("Too many iterations")

    raise AssertionError("Should never have gotten out of the loop")


def n_steps(dirs: list[int], maps: dict[str, tuple[str, str]], start_node: str) -> int:
    """
    Like `part1()`, except start on `start_node`, and go until reaching a node ending in
    'Z'
    """
    steps = 0
    curr = start_node
    for d in itertools.chain.from_iterable(itertools.repeat(dirs)):
        steps += 1
        curr: str = maps[curr][d]
        if curr.endswith("Z"):
            return steps

        if steps == 100_000:
            raise AssertionError("Too many iterations")

    raise AssertionError("Should never have gotten out of the loop")


def part2(dirs: list[int], maps: dict[str, tuple[str, str]]) -> int:
    ends_with_a = {k: v for k, v in maps.items() if k.endswith("A")}
    return math.lcm(*[n_steps(dirs, maps, sn) for sn in ends_with_a])


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    dirs, maps = parse(raw_input)
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = part1(dirs, maps)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2 = part2(dirs, maps)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
