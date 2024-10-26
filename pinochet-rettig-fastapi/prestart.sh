#! /usr/bin/env bash

# Let the DB start
python ./src/pinochet/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./src/pinochet/initial_data.py

# launch uvicorn
uvicorn pinochet.main:app --host "0.0.0.0" --port 8080
