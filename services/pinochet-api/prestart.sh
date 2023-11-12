#! /usr/bin/env bash

# Let the DB start
python /src/api/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /src/api/initial_data.py