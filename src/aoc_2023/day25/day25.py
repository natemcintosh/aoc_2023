from pathlib import Path

import numpy as np
from scipy.sparse import csr_array

from aoc_2023.utils import format_ns


def parse_into_matrix(input_str: str) -> tuple[csr_array, list[str]]:
    """
    Inputs look like

    jqt: rhn xhk nvd
    rsh: frs pzl lsr
    xhk: hfx
    cmg: qnr nvd lhk bvb
    rhn: xhk bvb hfx
    bvb: xhk hfx
    pzl: lsr hfx nvd
    qnr: nvd
    ntq: jqt hfx bvb xhk
    nvd: lhk
    lsr: lhk
    rzs: qnr cmg lsr rsh
    frs: qnr lhk lsr

    Where each line is a two-way connection. Want to create a connections matrix
    """
    # First get a dict of all the nodes, mapped to indexes
    nodes: dict[str, int] = {
        s: idx
        for idx, s in enumerate(
            sorted(set(input_str.replace(":", "").replace("\n", " ").split()))
        )
    }

    # Create a connections matrix
    arr = np.full(shape=(len(nodes), len(nodes)), dtype=bool, fill_value=False)

    # Add the connections to a matrix
    for line in input_str.splitlines():
        head, tail = line.split(":", maxsplit=1)
        hidx = nodes[head]
        rest = tail.split()
        for r in rest:
            ridx = nodes[r]
            # Add the connections on both sides of the diagonal
            arr[hidx, ridx] = True
            arr[ridx, hidx] = True

    return csr_array(arr), sorted(nodes.keys())


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
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
