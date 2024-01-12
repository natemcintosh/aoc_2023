from aoc_2023.day23.day23 import (
    get_nodes,
    build_p1_graph,
    build_p2_graph,
    longest_path,
    P,
)


def test_p1_easy():
    raw_input = """#.######
#.......
#######."""
    snode, enode, nodes = get_nodes(raw_input)
    g = build_p1_graph(nodes)
    want = 8
    got = longest_path(g, snode, enode)
    assert want == got


def test_p1_2():
    raw_input = ".>.>."
    snode, enode, nodes = get_nodes(raw_input)
    snode = P(0, 0)
    enode = P(0, 4)
    g = build_p1_graph(nodes)
    want = 4
    got = longest_path(g, snode, enode)
    assert want == got


def test_part1():
    raw_input = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
    snode, enode, nodes = get_nodes(raw_input)
    g = build_p1_graph(nodes)
    want = 94
    got = longest_path(g, snode, enode)
    assert want == got


def test_part2():
    raw_input = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
    snode, enode, nodes = get_nodes(raw_input, replace_slopes=True)
    g = build_p2_graph(nodes)
    want = 154
    got = longest_path(g, snode, enode)
    assert want == got
