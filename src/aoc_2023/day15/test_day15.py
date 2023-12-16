from aoc_2023.day15.day15 import HASH, part2

import pytest

hash_params = [
    ("HASH", 52),
    ("rn=1", 30),
    ("cm-", 253),
    ("qp=3", 97),
    ("cm=2", 47),
    ("qp-", 14),
    ("pc=4", 180),
    ("ot=9", 9),
    ("ab=5", 197),
    ("pc-", 48),
    ("pc=6", 214),
    ("ot=7", 231),
]


@pytest.mark.parametrize("step, want", hash_params)
def test_hash(step, want):
    got = HASH(step)
    assert want == got


def test_part1():
    raw_input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    steps = [s for s in raw_input.strip().split(",")]
    got = part2(steps)
    want = 145
    assert want == got
