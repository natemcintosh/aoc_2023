import pytest

from aoc_2023.day10.day10 import Node, build_loop, parse, find_first_connecting_pt


@pytest.mark.skip()
def test_build_ll():
    raw_input = """.....
.S-7.
.|.|.
.L-J.
....."""
    arr = parse(raw_input)
    got = build_loop(arr)
    n0 = Node(value="S", pos=(1, 1), stps=0)

    n1 = Node(value="-", pos=(1, 2))
    n1.bk_link(n0)

    n2 = Node(value="7", pos=(1, 3))
    n2.bk_link(n1)

    n3 = Node(value="|", pos=(2, 3))
    n3.bk_link(n2)

    n4 = Node(value="J", pos=(3, 3))
    n4.bk_link(n3)

    n5 = Node(value="-", pos=(3, 2))
    n5.bk_link(n4)

    n6 = Node(value="L", pos=(3, 1))
    n6.bk_link(n5)

    n7 = Node(value="|", pos=(2, 1))
    n7.bk_link(n6)
    n7.fd_link(n0)

    assert n0.is_loop()

    assert got == n0


ps = [
    (
        parse(
            """.....
.S-7.
.|.|.
.L-J.
....."""
        ),
        (1, 1),
        (1, 2),
    ),
    (
        parse(
            """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
        ),
        (1, 1),
        (1, 2),
    ),
    (
        parse(
            """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
        ),
        (2, 0),
        (2, 1),
    ),
]


@pytest.mark.parametrize("arr, start_idx, want", ps)
def test_find_first_connecting_pt(arr, start_idx, want):
    got = find_first_connecting_pt(arr, start_idx)
    assert want == got


def test_find_first_connecting_pt_failure_case():
    raw_input = """.....
.S.7.
...|.
.L-J.
....."""
    arr = parse(raw_input)
    with pytest.raises(AssertionError):
        find_first_connecting_pt(arr, (1, 1))
