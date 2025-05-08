from itertools import combinations
from pathlib import Path
from typing import NamedTuple

from aoc_2023.utils import format_ns


class Ray(NamedTuple):
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @staticmethod
    def parse(line: str) -> "Ray":
        spos, svel = line.split("@", maxsplit=1)
        x, y, z = spos.split(",", maxsplit=2)
        vx, vy, vz = svel.split(",", maxsplit=2)
        return Ray(int(x), int(y), int(z), int(vx), int(vy), int(vz))

    def intersects(self, other: "Ray") -> list[float] | None:
        """
        Where does this ray intersect with other. If it does not, return `None`

        Calculate slope for each line, m.

        For any pair, calculate the x-crossing with
        x = (m1*x1 - m2*x2 + y2 - y1) / (m1 - m2)
        plug that value into
        y = m1*(x - x1) + y1

        Then check that the intersection does not happen on the wrong side of the ray
        """
        m1 = self.vy / self.vx
        m2 = other.vy / other.vx

        if (m1 - m2) == 0:
            return None

        x_cross = ((m1 * self.x - m2 * other.x) + (other.y - self.y)) / (m1 - m2)
        y_cross = m1 * (x_cross - self.x) + self.y

        # If vx > 0, x_cross must be > x
        if ((self.vx > 0) and (x_cross < self.x)) or (
            (other.vx > 0) and (x_cross < other.x)
        ):
            return None

        # If vy > 0, y must be > y
        if ((self.vy > 0) and (y_cross < self.y)) or (
            (other.vy > 0) and (y_cross < other.y)
        ):
            return None

        # If vx < 0, x must be < x
        if ((self.vx < 0) and (x_cross > self.x)) or (
            (other.vx < 0) and (x_cross > other.x)
        ):
            return None

        # If vy < 0, y must be < y
        if ((self.vy < 0) and (y_cross > self.y)) or (
            (other.vy < 0) and (y_cross > other.y)
        ):
            return None

        return [x_cross, y_cross]


def part1(rays: list[Ray], minmax: tuple[int, int]) -> int:
    """
    How many crossing points in the box defined by the min and max in the x and y
    directions.
    """
    mn, mx = minmax

    return sum(
        1
        for r1, r2 in combinations(rays, 2)
        if (xing := r1.intersects(r2)) is not None
        if xing[0] >= mn
        if xing[0] <= mx
        if xing[1] >= mn
        if xing[1] <= mx
    )


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    rays = [Ray.parse(line) for line in raw_input.splitlines()]
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = part1(rays, minmax=(200000000000000, 400000000000000))
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()

    p2_time = format_ns(perf_counter_ns() - p2_start)
    # print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
