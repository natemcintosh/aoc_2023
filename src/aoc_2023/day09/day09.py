import functools
from pathlib import Path

import numpy as np

from aoc_2023.utils import format_ns


def parse(file: Path) -> np.ndarray:
    return np.loadtxt(file, dtype=int)


def predict(line: np.ndarray, forward: bool = True) -> int:
    """
    Diff till you get only zeros, then add a 0 to the front of that last row, and
    predict. E.g.

    0   3   6   9  12  15  18
      3   3   3   3   3   3
        0   0   0   0   0

    Where 3 and 18 are the predictions

    If `forward`, then extrapolate forward. Otherwise extrapolate backwards.
    """
    idx = -1 if forward else 0
    final_values: list[int] = [line[idx]]

    def func(x: int, y: int) -> int:
        return x + y if forward else y - x

    deriv = line.copy()

    for _ in range(100):
        deriv = np.diff(deriv)
        if (deriv == 0).all():
            final_values.reverse()
            return functools.reduce(func, final_values)
        final_values.append(deriv[idx])

    raise AssertionError("Too many iterations")


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    arr = parse(input_path)
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = sum(predict(line) for line in arr)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2 = sum(predict(line, False) for line in arr)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
