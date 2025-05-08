default:
    uv run ruff check --select I --fix
    uv run ruff check
    uv run ruff format

alias t := test
test:
    uv run pytest

run day:
    uv run python src/aoc_2023/day{{ day }}/day{{ day }}.py
