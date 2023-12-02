import re
from pathlib import Path
from dataclasses import dataclass

from aoc_2023.utils import format_ns


@dataclass
class RGB:
    r: int = 0
    g: int = 0
    b: int = 0

    def contains(self, other: "RGB") -> bool:
        return (self.r >= other.r) and (self.g >= other.g) and (self.b >= other.b)

    def power(self) -> int:
        return self.r * self.g * self.b


def parse_RGB(parts: list[tuple[str, str]]) -> RGB:
    """
    In each tuple, first item is the number, second is the letter
    """
    r = RGB()
    for p in parts:
        match p:
            case (n, "r"):
                r.r += int(n)
            case (n, "g"):
                r.g += int(n)
            case (n, "b"):
                r.b += int(n)

    return r


def parse_game(game: str) -> list[RGB]:
    """
    For example, the record of a few games might look like this:

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

    In game 1, three sets of cubes are revealed from the bag (and then put back again).
    The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green
    cubes, and 6 blue cubes; the third set is only 2 green cubes.
    """
    # Split into draws
    draws = game.split(";")

    # To search for
    pattern = re.compile(r"(\d+) ([b|r|g])")

    # Break it into easy to digest chunks
    pairings = [pattern.findall(d) for d in draws]

    return [parse_RGB(parts) for parts in pairings]


def part1(games: list[list[RGB]]) -> int:
    """
    The Elf would first like to know which games would have been possible if the bag
    contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

    In the example above, games 1, 2, and 5 would have been possible if the bag had been
    loaded with that configuration. However, game 3 would have been impossible because
    at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also
    have been impossible because the Elf showed you 15 blue cubes at once. If you add up
    the IDs of the games that would have been possible, you get 8.
    """
    no_more_than = RGB(r=12, g=13, b=14)

    return sum(
        idx + 1
        for idx, game in enumerate(games)
        if all(no_more_than.contains(draw) for draw in game)
    )


def smallest_RGB(game: list[RGB]) -> RGB:
    """
    in each game you played, what is the fewest number of cubes of each color that could
    have been in the bag to make the game possible?
    """
    r = RGB()
    for g in game:
        if g.r > r.r:
            r.r = g.r

        if g.g > r.g:
            r.g = g.g

        if g.b > r.b:
            r.b = g.b

    return r


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    games = [parse_game(game) for game in raw_input.splitlines()]

    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = part1(games)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2 = sum(smallest_RGB(game).power() for game in games)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
