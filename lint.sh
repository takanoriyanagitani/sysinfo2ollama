#!/bin/sh

python3 -m uv run \
    mypy \
    --check-untyped-defs \
    --ignore-missing-imports \
    ./main.py

python3 -m uv run \
    ruff check
