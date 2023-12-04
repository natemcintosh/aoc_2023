import re
from pathlib import Path
from dataclasses import dataclass

from aoc_2023.utils import format_ns


@dataclass
class Cards:
    have: set[int]
    want: set[int]
    n_copies: int

    def points_won(self) -> int:
        intersection = self.want.intersection(self.have)
        return 2 ** (len(intersection) - 1) if len(intersection) > 0 else 0


def parse_card(line: str) -> Cards:
    pieces = line.split(":")[-1]
    have, want = pieces.split("|", maxsplit=1)
    return Cards(
        have=set(int(n) for n in re.split(r"\s+", have.strip())),
        want=set(int(n) for n in re.split(r"\s+", want.strip())),
        n_copies=1,
    )


def part2(cards: list[Cards]) -> int:
    """
    you win copies of the scratchcards below the winning card equal to the number of
    matches. So, if card 10 were to have 5 matching numbers, you would win one copy each
    of cards 11, 12, 13, 14, and 15.
    """
    cs = cards.copy()

    # Iterate over the list
    for idx, card in enumerate(cs):
        n_matches = len(card.have.intersection(card.want))

        # For each extra, go to that card, and increase the number of copies
        for extra in range(1, n_matches + 1):
            this_idx = idx + extra
            cs[this_idx].n_copies += card.n_copies

    return sum(c.n_copies for c in cs)


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    cards = [parse_card(line) for line in raw_input.splitlines()]

    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = sum(c.points_won() for c in cards)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2 = part2(cards)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
