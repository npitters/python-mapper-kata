#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

export PYTHONPATH="./app"

poetry install

poetry run pytest -vv ./tests
poetry run coverage report -m
