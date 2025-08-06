#!/bin/sh

export ENV_PROMPT='Get current storage/mem info and write short health report(<350 chars)'

export ENV_MODEL_NAME=magistral:24b  # too slow
export ENV_MODEL_NAME=gpt-oss:20b    # may not work?
export ENV_MODEL_NAME=mistral:7b     # may not work?
export ENV_MODEL_NAME=phi4-mini:3.8b # may not work?

export ENV_MODEL_NAME=mistral-small:24b # less readable, slow
export ENV_MODEL_NAME=granite3.3:8b     # less readable
export ENV_MODEL_NAME=mistral-nemo:12b  # balanced
export ENV_MODEL_NAME=llama3.2:3b       # faster

python3 -m uv run \
    ./main.py
