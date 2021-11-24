#! /usr/bin/env bash
set -e

python /app/app/main_pre_start.py

bash ./scripts/test.sh "$@"