from collections import Counter
from collections.abc import Callable
from enum import IntEnum
from pathlib import Path

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


def which_type(hand: list, count: bool = True) -> str:
    m: list[int] = sorted(Counter(hand).values()) if count else hand

    match m:
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

    raise AssertionError(f"Did not recognize pairings {m}")


def joker_which_type(hand) -> str:
    """
    Jokers will act like whatever card would make the hand the strongest possible.
    """
    h = list(hand)
    n_jokers = list(h).count(1)

    # Count everything that isn't a joker
    counts = sorted(Counter([x for x in h if x != 1]).values())

    if len(counts) > 0:
        # Add the count of jokers to the card with the most counts
        counts[-1] += n_jokers
    else:
        counts = [5]

    return which_type(counts, count=False)


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


def rank_hands(hands: pl.DataFrame, rank_fn: Callable) -> int:
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
        hands.with_columns(
            type=pl.col.hand.map_elements(function=rank_fn, return_dtype=pl.String)
        )
        .with_columns(type_score=type_score())
        .with_columns(s=pl.col.hand.arr.to_struct())
        .unnest("s")
        .sort(
            "type_score",
            "field_0",
            "field_1",
            "field_2",
            "field_3",
            "field_4",
        )
        .with_row_index(name="rank")
        .with_columns(pl.col.rank + 1)
        .select(winning=(pl.col.rank * pl.col.bid).sum())
        .item()
    )


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    parsed = [parse_line(line) for line in raw_input.splitlines()]
    hands = pl.DataFrame(
        dict(hand=[h[0] for h in parsed], bid=[h[1] for h in parsed])
    ).with_columns(hand=pl.col.hand.list.to_array(5))

    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = rank_hands(hands, rank_fn=which_type)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    parsed = [parse_line(line, w_joker=True) for line in raw_input.splitlines()]
    hands = pl.DataFrame(
        dict(hand=[h[0] for h in parsed], bid=[h[1] for h in parsed])
    ).with_columns(hand=pl.col.hand.list.to_array(5))
    p2 = rank_hands(hands, rank_fn=joker_which_type)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
