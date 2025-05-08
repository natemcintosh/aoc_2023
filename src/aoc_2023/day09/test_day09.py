from pathlib import Path

import numpy as np
import pytest

from aoc_2023.day09.day09 import parse, predict

pred_params = [
    (np.array([0, 3, 6, 9, 12, 15]), True, 18),
    (np.array([1, 3, 6, 10, 15, 21]), True, 28),
    (np.array([10, 13, 16, 21, 30, 45]), True, 68),
    (np.array([0, 3, 6, 9, 12, 15]), False, -3),
    (np.array([1, 3, 6, 10, 15, 21]), False, 0),
    (np.array([10, 13, 16, 21, 30, 45]), False, 5),
]


@pytest.mark.parametrize("line, forward, want", pred_params)
def test_predict(line, forward, want):
    got = predict(line, forward)
    assert want == got


def test_part1_real():
    input_path = Path(__file__).parent / "input.txt"
    arr = parse(input_path)
    got = sum(predict(line) for line in arr)
    want = 1731106378
    assert want == got


def test_part2():
    arr = np.array(
        [
            [0, 3, 6, 9, 12, 15],
            [1, 3, 6, 10, 15, 21],
            [10, 13, 16, 21, 30, 45],
        ]
    )
    got = sum(predict(line, forward=False) for line in arr)
    want = 2
    assert want == got


def test_part2_real():
    input_path = Path(__file__).parent / "input.txt"
    arr = parse(input_path)
    got = sum(predict(line, False) for line in arr)
    want = 1087
    assert want == got
