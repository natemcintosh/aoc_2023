from pathlib import Path
from dataclasses import dataclass

from aoc_2023.utils import format_ns


@dataclass
class Blueprint:
    raw_parts: str
    fail_groups: list[int]
    # parts_known: str

    @staticmethod
    def parse(line: str) -> "Blueprint":
        """
        lines look like
        ???.### 1,1,3
        where '?' means we don't know what the object is, '.' means operational, and '#'
        means broken. The numbers at the end tell us the groups of broken springs.
        """
        raw_parts, groups = line.split(maxsplit=1)
        fail_groups = [int(x) for x in groups.split(",")]

        # To see if a failed part matches a group, it must be the exact number of the
        # group, and surrounded by either '?' or '.'
        for idx, grp in enumerate(fail_groups):
            pass

        return Blueprint(raw_parts, fail_groups)

    # def gen_posibilities(self) -> Generator:
    #     pass


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    # arr = parse(raw_input)
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
