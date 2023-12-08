from aoc_2023.day07.day07 import (
    five_of_kind,
    four_of_kind,
    Card,
    full_house,
    three_of_kind,
    two_pair,
    one_pair,
    high_card,
    parse_line,
    rank_hands,
)

import pytest
import polars as pl


hand_params = [
    (five_of_kind, [Card.ACE] * 5, True),
    (five_of_kind, [Card.FIVE] * 5, True),
    (five_of_kind, [Card.TEN] * 4 + [Card.ACE], False),
    (four_of_kind, [Card.TEN] * 4 + [Card.ACE], True),
    (four_of_kind, [Card.TWO] + [Card.SEVEN] * 4, True),
    (four_of_kind, [Card.TWO] * 2 + [Card.SEVEN] * 3, False),
    (full_house, [Card.THREE] * 3 + [Card.EIGHT] * 2, True),
    (full_house, [Card.THREE] * 2 + [Card.EIGHT] * 3, True),
    (full_house, [Card.THREE, Card.NINE] + [Card.EIGHT] * 3, False),
    (three_of_kind, [Card.TWO] * 3 + [Card.ACE, Card.JACK], True),
    (three_of_kind, [Card.THREE] * 2 + [Card.EIGHT] * 3, False),
    (two_pair, [Card.TWO, Card.TWO, Card.THREE, Card.THREE, Card.FOUR], True),
    (two_pair, [Card.TWO, Card.TWO, Card.THREE, Card.FOUR, Card.FOUR], True),
    (two_pair, [Card.TWO, Card.TWO, Card.THREE, Card.FIVE, Card.FOUR], False),
    (one_pair, [Card.TWO, Card.TWO, Card.ACE, Card.KING, Card.QUEEN], True),
    (one_pair, [Card.TWO, Card.QUEEN, Card.ACE, Card.KING, Card.QUEEN], True),
    (one_pair, [Card.TWO, Card.TEN, Card.ACE, Card.KING, Card.QUEEN], False),
    (high_card, list(Card)[:5], True),
    (high_card, [Card.TWO, Card.TWO, Card.ACE, Card.KING, Card.QUEEN], False),
]


@pytest.mark.parametrize("fn, hand, want", hand_params)
def test_of_kind(fn, hand, want):
    got = fn(hand)
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
