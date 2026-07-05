#! /usr/bin/env bash

# Let the DB start
uv run python ./src/pinochet/backend_pre_start.py

# Run migrations
uv run alembic upgrade head

# Create initial data in DB
uv run python ./src/pinochet/initial_data.py

# launch uvicorn
uv run uvicorn pinochet.main:app --host "0.0.0.0" --port 8080
