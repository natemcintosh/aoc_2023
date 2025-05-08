from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from aoc_2023.utils import format_ns


def HASH(s: str) -> int:
    """
    - Determine the ASCII code for the current character of the string.
    - Increase the current value by the ASCII code you just determined.
    - Set the current value to itself multiplied by 17.
    - Set the current value to the remainder of dividing itself by 256.
    """
    curr = 0
    for si in s:
        curr += ord(si)
        curr *= 17
        curr = curr % 256

    return curr


class Lens(NamedTuple):
    label_str: str
    focal_length: int


def index_of(slabel: str, box: list[Lens]) -> int | None:
    "Find the index of the label in the box. None if not in the box"
    for idx, lens in enumerate(box):
        if slabel == lens.label_str:
            return idx

    return None


def part2(steps: list[str]) -> int:
    """
    The sequence of letters at the start of a step tells you the label of the lens.
    The result of the HASH algorithm on the label tells you the box

    The operation is determined by the '=' or '-'
    - if '-', go to the correct box, and remove the correct lens (if present). Then move
      any remaining lenses as far forward in the box as they can go
    - if '=', the number after the '=' tells you the focal length of the lens to insert
      in the relevant box.
        - if there is already a lens in the box with the same label, replace it with the
          new lens.
        - else put it at the back of the stack of lenses

    Finally, calculate the focusing power of the set of boxes and lenses.
    The focusing power of a single lens is the result of multiplying together:
    - One plus the box number of the lens in question.
    - The slot number of the lens within the box: 1 for the first lens, 2 for the second
        lens, and so on.
    - The focal length of the lens.
    """
    boxes: dict[int, list[Lens]] = defaultdict(list)

    for stp in steps:
        if "-" in stp:
            # Remove the lens with this label if it exists, and move any remaining
            # lenses forward in the box
            slabel = stp[:-1]
            label = HASH(slabel)
            assert label < 256, f"Got box index of {label}"
            box = boxes[label]
            if (idx := index_of(slabel, box)) is not None:
                box.pop(idx)

        else:
            slabel, sfocal = stp.split("=", maxsplit=1)
            label = HASH(slabel)
            focal = int(sfocal)
            box = boxes[label]
            assert label < 256, f"Got box index of {label}"
            if (idx := index_of(slabel, box)) is not None:
                # Replace that lens with the new one
                box[idx] = Lens(label_str=slabel, focal_length=focal)
            else:
                # Stick it at the back of the box
                box.append(Lens(label_str=slabel, focal_length=focal))

    # Calculate the focusing power of the boxes of lenses
    return sum(
        (box_num + 1) * (slot_num + 1) * lens.focal_length
        for box_num, lenses in boxes.items()
        for slot_num, lens in enumerate(lenses)
    )


if __name__ == "__main__":
    from time import perf_counter_ns

    # === Parse ========================================================================
    parse_start = perf_counter_ns()

    input_path = Path(__file__).parent / "input.txt"
    raw_input = input_path.read_text()
    steps = [s for s in raw_input.strip().split(",")]
    parse_time = format_ns(perf_counter_ns() - parse_start)

    # === Part 1 =======================================================================
    p1_start = perf_counter_ns()
    p1 = sum(HASH(step) for step in steps)
    p1_time = format_ns(perf_counter_ns() - p1_start)
    print(f"Part 1: {p1}")

    # === Part 2 =======================================================================
    p2_start = perf_counter_ns()
    p2 = part2(steps)
    p2_time = format_ns(perf_counter_ns() - p2_start)
    print(f"Part 2: {p2}")

    # === Printing =====================================================================
    print(f"\n\nSetup took {parse_time}")
    print(f"Part 1 took {p1_time}")
    print(f"Part 2 took {p2_time}")
