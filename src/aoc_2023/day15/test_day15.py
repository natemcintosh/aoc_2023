from aoc_2023.day15.day15 import HASH

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
