# aoc-2023

Advent of Code 2023 in Python.

## Running the code
[Rye](https://github.com/mitsuhiko/rye) was used to set up the repo structure. With `rye` installed
```sh
git clone https://github.com/natemcintosh/aoc_2023/
cd aoc_2023

# Will set up virtual environment and download deps
rye sync

# Activate the virtual environment
. .venv/bin/activate

# Run a day
python src/aoc_2023/day01/day01.py

# Run the tests
pytest
```
