#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

if [[  -d ".pytest_cache" ]];then
    echo "🤖 ⟶  Removing .pytest_cache subdirectory…"
    rm -rf .pytest_cache
fi

echo "🤖 ⟶  Removing __pycache__ subdirectories…"
find . -type d -name "__pycache__" -exec rm -r "{}" \; -prune
