import pytest

from aoc_2023.day12.day12 import Blueprint

lines = [
    ("#.#.### 1,1,3", Blueprint("#.#.###", [1, 1, 3])),
    ("#....######..#####. 1,6,5", Blueprint("#....######..#####.", [1, 6, 5])),
    ("?#?#?#?#?#?#?#? 1,3,1,6", Blueprint("?#?#?#?#?#?#?#?", [1, 3, 1, 6])),
    ("?###???????? 3,2,1", Blueprint("?###????????", [3, 2, 1])),
]


@pytest.mark.parametrize("line, want", lines)
def test_bp_parse(line, want):
    got = Blueprint.parse(line)
    assert want == got
