# Pinochet Streamlit App

Visual exploration of the Pinochet-Rettig dataset. Displays events on an interactive map with filtering by date range and nationality.

## Quick start

Requires a running PostGIS dev database on `localhost:5433` with the dbt staging model built (see root `docker-compose.postgis.yml` and dbt project).

```bash
# 1. Install dependencies
make install

# 2. Run with hardcoded dev credentials
make run.dev
```

The app will be available at `http://localhost:8501`.

## Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies via `uv sync` |
| `make run` | Run with env vars from `../.env` |
| `make run.dev` | Run with hardcoded dev credentials (no `.env` needed) |
| `make help` | Show all available targets |

## What it shows

- **Interactive map**: Events plotted by location (via `st.map`)
- **PyDeck scatterplot**: 3D-style visualization with tooltips
- **Date range filter**: Slider to narrow events by `start_date_daily`
- **Nationality filter**: Multi-select to filter victims by nationality
- **Data table**: Raw data view below the map

## Data source

Currently reads directly from the DB table `api.stg_pinochet__base`. This requires dbt to have built the staging model first.

## Stack

- Streamlit
- GeoPandas + PyDeck
- SQLAlchemy + psycopg2-binary (direct DB access)
- python-decouple (env var loading)
