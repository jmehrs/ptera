#! /usr/bin/env bash

# if any command fails, exit as a failure
set -o errexit

# Let the DB start
python /app/app/main_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/app/main_init_data.py