from pathlib import Path
from typing import NamedTuple

import networkx as nx

from aoc_2023.utils import format_ns


class P(NamedTuple):
    r: int
    c: int

    def __add__(self, other: "P") -> "P":
        return P(self.r + other.r, self.c + other.c)


def get_nodes(
    raw_input: str, replace_slopes: bool = False
) -> tuple[P, P, dict[P, str]]:
    """
    Get just the nodes that you can walk on
    """
    snode = P(0, 1)

    lines = raw_input.splitlines()
    enode = P(len(lines) - 1, lines[-1].index("."))

    if replace_slopes:
        raw_input = (
            raw_input.replace("<", ".")
            .replace(">", ".")
            .replace("^", ".")
            .replace("v", ".")
        )

    nodes = {
        P(ridx, cidx): v
        for ridx, row in enumerate(lines)
        for cidx, v in enumerate(row)
        if v != "#"
    }

    return snode, enode, nodes


def build_p1_graph(nodes: dict[P, str]) -> nx.DiGraph:
    """
    Connect each node to any neighbors if both are '.'.
    If node is a slope (<, >, ^, v), can connect to neighbor it points to, but that
    neighbor can't connect to it.
    """
    DIRS = (
        P(-1, 0),
        P(0, 1),
        P(1, 0),
        P(0, -1),
    )

    g = nx.DiGraph()

    for n, frm in nodes.items():
        for d in DIRS:
            if n + d not in nodes:
                continue

            to = nodes[n + d]
            match (frm, d, to):
                # If '<' and d is left of `n`, and can go into `to`
                case ("<", P(0, -1), to) if to != ">":
                    g.add_edge(n, n + d)
                case (".", P(0, -1), to) if to != ">":
                    g.add_edge(n, n + d)
                case (">", P(0, 1), to) if to != "<":
                    g.add_edge(n, n + d)
                case (".", P(0, 1), to) if to != "<":
                    g.add_edge(n, n + d)
                case ("^", P(-1, 0), to) if to != "v":
                    g.add_edge(n, n + d)
                case (".", P(-1, 0), to) if to != "v":
                    g.add_edge(n, n + d)
                case ("v", P(1, 0), to) if to != "^":
                    g.add_edge(n, n + d)
                case (".", P(1, 0), to) if to != "^":
                    g.add_edge(n, n + d)

    return g


def build_p2_graph(nodes: dict[P, str]) -> nx.DiGraph:
    """
    Connect each node to any neighbors if both are '.'. Slopes have been removed.
    """
    DIRS = (
        P(-1, 0),
        P(0, 1),
        P(1, 0),
        P(0, -1),
    )

    g = nx.DiGraph()

    for n in nodes.keys():
        for d in DIRS:
            if n + d not in nodes:
                continue
            g.add_edge(n, n + d)
    return g


def longest_path(g: nx.DiGraph, snode: P, enode: P) -> int:
    """What's the longest path from snode to enode"""
    return max(len(p) for p in nx.all_simple_edge_paths(g, snode, enode))


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    snode, enode, nodes = get_nodes(raw_input)
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    g = build_p1_graph(nodes)
    p1 = longest_path(g, snode, enode)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    snode, enode, nodes = get_nodes(raw_input, replace_slopes=True)
    g = build_p2_graph(nodes)
    p2 = longest_path(g, snode, enode)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    # print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
