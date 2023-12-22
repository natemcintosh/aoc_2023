from pathlib import Path
from typing import NamedTuple

from aoc_2023.utils import format_ns


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


# def eval_rule(part: Part, all_rules: dict[str, str], start: str = "in") -> bool:
#     "True if accepted, else False"
#     # Get the correct set of rules for this flow
#     rules = all_rules[start]

#     for r in rules.split(","):
#         if rule_passes(part, r):
#             rules = all_rules[new_rule].split(",")
#             continue


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()

    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()

    p1_time = format_ns(perf_counter_ns() - p1_start)
    # print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2_time = format_ns(perf_counter_ns() - p2_start)
    # print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
