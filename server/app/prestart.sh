#! /usr/bin/env bash

# Let the DB start
echo "Waiting for postgres..."
python ./app/server_pre_start.py

# Run migrations
alembic upgrade head
