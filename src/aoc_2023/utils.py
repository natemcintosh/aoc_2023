import math


def order_of_magnitude(x: int | float) -> int:
    "From somewhere on the internet"
    return int(math.floor(math.log10(abs(x))))


def format_ns(nanosecs: int) -> str:
    """
    The idea here is to take in some number of nanoseconds, and automatically format it
    into ns, us, ms, s, etc.
    """
    match order_of_magnitude(nanosecs):
        case 0 | 1 | 2:
            return f"{nanosecs}ns"
        case 3 | 4 | 5:
            return f"{int(nanosecs / 1e3)}μs"
        case 6 | 7 | 8:
            return f"{int(nanosecs / 1e6)}ms"
        case _:
            return f"{int(nanosecs / 1e9)}s"
