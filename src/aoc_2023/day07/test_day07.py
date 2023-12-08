from aoc_2023.day07.day07 import (
    which_type,
    Card,
    parse_line,
    rank_hands,
)

import pytest
import polars as pl


hand_params = [
    ([Card.ACE] * 5, "five_of_kind"),
    ([Card.FIVE] * 5, "five_of_kind"),
    ([Card.TEN] * 4 + [Card.ACE], "four_of_kind"),
    ([Card.TWO] + [Card.SEVEN] * 4, "four_of_kind"),
    ([Card.THREE] * 3 + [Card.EIGHT] * 2, "full_house"),
    ([Card.THREE] * 2 + [Card.EIGHT] * 3, "full_house"),
    ([Card.TWO] * 3 + [Card.ACE, Card.JACK], "three_of_kind"),
    ([Card.TWO, Card.TWO, Card.THREE, Card.THREE, Card.FOUR], "two_pair"),
    ([Card.TWO, Card.TWO, Card.THREE, Card.FOUR, Card.FOUR], "two_pair"),
    ([Card.TWO, Card.TWO, Card.ACE, Card.KING, Card.QUEEN], "one_pair"),
    ([Card.TWO, Card.QUEEN, Card.ACE, Card.KING, Card.QUEEN], "one_pair"),
    (list(Card)[:5], "high_card"),
]


@pytest.mark.parametrize("hand, want", hand_params)
def test_of_kind(hand, want):
    got = which_type(hand)
    assert want == got


def test_part1():
    raw_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    parsed = [parse_line(line) for line in raw_input.splitlines()]
    hands = pl.DataFrame(dict(hand=[h[0] for h in parsed], bid=[h[1] for h in parsed]))
    got = rank_hands(hands)
    want = 6440
    assert want == got
