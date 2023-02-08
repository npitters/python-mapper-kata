#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

FILE=$1

poetry install -q

poetry run python app --file ${FILE}
