import numpy as np
import pytest

from aoc_2023.day24.day24 import Ray, part1

ps = [
    (Ray(19, 13, 20, -2, 1, -2), Ray(18, 19, 22, -1, -1, -2), [14.33333, 15.333333]),
    (Ray(19, 13, 20, -2, 1, -2), Ray(12, 31, 28, -1, -2, -1), [6.2, 19.4]),
    (Ray(18, 19, 22, -1, -1, -2), Ray(20, 25, 34, -2, -2, -4), None),
]


@pytest.mark.parametrize("r1, r2, want", ps)
def test_ray_intersects(r1, r2, want):
    got = r1.intersects(r2)
    if want is None:
        assert want == got
        return

    assert np.allclose(want, got)


def test_part1():
    raw_input = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    rays = [Ray.parse(line) for line in raw_input.splitlines()]
    want = 2
    got = part1(rays, (7, 27))
    assert want == got
