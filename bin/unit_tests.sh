#!/usr/bin/env bash

set -e

export PYTHONPATH="./app"

poetry install

poetry run pytest ./tests/unit_tests
