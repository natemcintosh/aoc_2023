from aoc_2023.utils import format_ns

import pytest

format_ns_cases = list(
    zip(
        [
            1,
            10,
            100,
            1_000,
            10_000,
            100_000,
            1_000_000,
            10_000_000,
            100_000_000,
            1_000_000_000,
        ],
        ["1ns", "10ns", "100ns", "1us", "10us", "100us", "1ms", "10ms", "100ms", "1s"],
    )
)


@pytest.mark.parametrize("input,want", format_ns_cases)
def test_format_ns(input, want):
    assert want == format_ns(input)
