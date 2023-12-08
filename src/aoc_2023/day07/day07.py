from pathlib import Path
from enum import IntEnum
from collections import Counter

import polars as pl

from aoc_2023.utils import format_ns


class Card(IntEnum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    JOKER = 1


def parse_card(s: str, w_joker: bool) -> Card:
    match s:
        case "2":
            return Card.TWO
        case "3":
            return Card.THREE
        case "4":
            return Card.FOUR
        case "5":
            return Card.FIVE
        case "6":
            return Card.SIX
        case "7":
            return Card.SEVEN
        case "8":
            return Card.EIGHT
        case "9":
            return Card.NINE
        case "T":
            return Card.TEN
        case "J":
            if w_joker:
                return Card.JOKER
            else:
                return Card.JACK
        case "Q":
            return Card.QUEEN
        case "K":
            return Card.KING
        case "A":
            return Card.ACE

    raise ValueError(f"Card {s} was not expected")


def parse_line(line: str, w_joker: bool = False) -> tuple[list[Card], int]:
    """
    A hand looks likes
    32T3K 765
    """
    cards, bid = line.split(maxsplit=1)
    return [parse_card(c, w_joker) for c in cards], int(bid)


def five_of_kind(hand: list[Card]) -> bool:
    "Is this hand five of a kind?"
    return [5] == sorted(Counter(hand).values())


def four_of_kind(hand: list[Card]) -> bool:
    "Are there 4 of the same?"
    return [1, 4] == sorted(Counter(hand).values())


def full_house(hand: list[Card]) -> bool:
    """
    Full house, where three cards have the same label, and the remaining two cards share
    a different label: 23332
    """
    return [2, 3] == sorted(Counter(hand).values())


def three_of_kind(hand: list[Card]) -> bool:
    """
    Three of a kind, where three cards have the same label, and the remaining two cards
    are each different from any other card in the hand: TTT98
    """
    return [1, 1, 3] == sorted(Counter(hand).values())


def two_pair(hand: list[Card]) -> bool:
    """
    Two pair, where two cards share one label, two other cards share a second label, and
    the remaining card has a third label: 23432
    """
    return [1, 2, 2] == sorted(Counter(hand).values())


def one_pair(hand: list[Card]) -> bool:
    """
    One pair, where two cards share one label, and the other three cards have a
    different label from the pair and each other: A23A4
    """
    return [1, 1, 1, 2] == sorted(Counter(hand).values())


def high_card(hand: list[Card]) -> bool:
    """
    High card, where all cards' labels are distinct: 23456
    """
    return [1, 1, 1, 1, 1] == sorted(Counter(hand).values())


def which_type(hand: list[Card]) -> str:
    match sorted(Counter(hand).values()):
        case [1, 1, 3]:
            return "three_of_kind"
        case [1, 2, 2]:
            return "two_pair"
        case [1, 1, 1, 2]:
            return "one_pair"
        case [1, 1, 1, 1, 1]:
            return "high_card"
        case [2, 3]:
            return "full_house"
        case [1, 4]:
            return "four_of_kind"
        case [5]:
            return "five_of_kind"

    raise AssertionError(f"Did not recognize hand {hand}")


def type_score() -> pl.Expr:
    return (
        pl.when(pl.col.type.eq("five_of_kind"))
        .then(7)
        .when(pl.col.type.eq("four_of_kind"))
        .then(6)
        .when(pl.col.type.eq("full_house"))
        .then(5)
        .when(pl.col.type.eq("three_of_kind"))
        .then(4)
        .when(pl.col.type.eq("two_pair"))
        .then(3)
        .when(pl.col.type.eq("one_pair"))
        .then(2)
        .when(pl.col.type.eq("high_card"))
        .then(1)
    )


def rank_hands(hands: pl.DataFrame) -> int:
    """
    Sorts the cards, from least to best.

    `hands` has columns `hand` which is the list of cards, and `bid`.

    If two hands have the same type, a second ordering rule takes effect. Start by
    comparing the first card in each hand. If these cards are different, the hand with
    the stronger first card is considered stronger. If the first card in each hand have
    the same label, however, then move on to considering the second card in each hand.
    If they differ, the hand with the higher second card wins; otherwise, continue with
    the third card in each hand, then the fourth, then the fifth.
    """
    return (
        hands.with_columns(type=pl.col.hand.map_elements(which_type))
        .with_columns(type_score=type_score())
        .with_columns(s=pl.col.hand.list.to_struct())
        .unnest("s")
        .sort(
            "type_score",
            "field_0",
            "field_1",
            "field_2",
            "field_3",
            "field_4",
        )
        .with_row_count(name="rank")
        .with_columns(pl.col.rank + 1)
        .select(winning=(pl.col.rank * pl.col.bid).sum())
        .item()
    )


def joker_which_type(hand: list[Card]) -> str:
    pass


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    parsed = [parse_line(line) for line in raw_input.splitlines()]
    hands = pl.DataFrame(dict(hand=[h[0] for h in parsed], bid=[h[1] for h in parsed]))

    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = rank_hands(hands)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    # time, dist = parse_p2(raw_input)
    # p2 = ways_to_win(time, dist)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    # print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
