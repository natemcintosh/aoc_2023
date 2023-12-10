from __future__ import annotations  # Need this so class can reference itself
from pathlib import Path
from dataclasses import dataclass

from aoc_2023.utils import format_ns


def parse(raw_input: str) -> list[list[str]]:
    "Just create a 2D array of characters"
    return [[c for c in line] for line in raw_input.splitlines()]


@dataclass
class Node:
    value: str
    pos: tuple[int, int]
    forward: Node | None = None
    backward: Node | None = None
    stps: int = -1

    def fd_link(self, other: Node):
        """
        Adds `other` as the forward Node, and vice versa

        Also set `other.stps = self.stps + 1` as long as `other` is not the origin
        """
        self.forward = other
        other.backward = self

        if other.value != "S":
            other.stps = self.stps + 1

    def bk_link(self, other: Node):
        """
        Adds `other` as the backward Node, and vice versa

        Also set `self.stps = other.stps + 1`
        """
        self.backward = other
        other.forward = self

        self.stps = other.stps + 1

    def is_loop(self) -> bool:
        """Tests if there is a full loop"""
        nxt = self
        while (nxt := nxt.forward) != self:
            if nxt is None:
                return False

        return True


# In a clockwise direction from the top
DIRS = (
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
)


def find_first_connecting_pt(
    arr: list[list[str]], start_idx: tuple[int, int]
) -> tuple[int, int]:
    """
    Given the starting point, find one of the two connecting points.

    Broken out into its own function for ease of testing.
    """
    # Directly above
    nbr = (start_idx[0] - 1, start_idx[1])
    if arr[nbr[0]][nbr[1]] in ("|", "7", "F"):
        return nbr

    # To the right
    nbr = (start_idx[0], start_idx[1] + 1)
    if arr[nbr[0]][nbr[1]] in ("-", "J", "7"):
        return nbr

    # Directly below
    nbr = (start_idx[0] + 1, start_idx[1])
    if arr[nbr[0]][nbr[1]] in ("|", "L", "J"):
        return nbr

    # To the left
    nbr = (start_idx[0], start_idx[1] - 1)
    if arr[nbr[0]][nbr[1]] in ("-", "L", "F"):
        return nbr

    raise AssertionError("Never found a match")


def build_loop(arr: list[list[str]]) -> Node:
    """
    Try to build an entire loop
    """
    # === Find the starting point ======================================================
    start_idx = (-1, -1)
    for ridx, row in enumerate(arr):
        for cidx, item in enumerate(row):
            if item == "S":
                start_idx = (ridx, cidx)

    assert start_idx != (-1, -1), "Failed to find starting point"
    n0 = Node(value="S", pos=start_idx, stps=0)
    prev_node = n0

    # === Find one of the connecting points ============================================
    nxt = find_first_connecting_pt(arr, start_idx)

    # === Iterate until back to start ==================================================
    while True:
        if arr[nxt[0]][nxt[1]] == "S":
            # Connect final node to the start, and return

            return n0

        # Create and link the new node
        new_node = Node(value=arr[nxt[0]][nxt[1]], pos=nxt)
        new_node.bk_link(prev_node)

        # Find the next node
        # match arr[nxt[0]][nxt[1]]:
        #     case "-":

        prev_node = new_node

    return n0


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    arr = parse(raw_input)
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()

    p1_time = format_ns(perf_counter_ns() - p1_start)
    # print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()

    p2_time = format_ns(perf_counter_ns() - p2_start)
    # print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
