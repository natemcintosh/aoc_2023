from day01 import parse


def test_parse():
    raw_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""
    want = [[1000, 2000, 3000], [4000], [5000, 6000], [7000, 8000, 9000], [10000]]
    got = parse(raw_input)
    assert want == got
