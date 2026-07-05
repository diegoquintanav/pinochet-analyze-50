# AGENTS.md

High-signal notes for OpenCode agents working in this monorepo.

## Project Structure

Root `pyproject.toml` is **not** a package (`package-mode = false`); it only pins shared dev tooling and dbt dependencies. Each service has its own `pyproject.toml` and must be installed separately.

- `pinochet-rettig-dbt/dbt_pinochet/` — dbt project (raw → intermediate → staging → `api` tables).
- `pinochet-rettig-fastapi/` — FastAPI + Strawberry GraphQL + Alembic.
- `pinochet-rettig-streamlit/` — Streamlit exploration app.
- `pinochet-rettig-linked-data/` — Ontop SPARQL virtual knowledge graph.
- `postgis/` — PostGIS container definitions.

## Environment Setup

1. Copy `example.env` to `.env` in the repo root. The `Makefile` sources this file; FastAPI and Streamlit also read it via `python-decouple`.
2. Install dependencies **per project**:
   - Root: `poetry install` (dbt, elementary, linting tools).
   - FastAPI: `cd pinochet-rettig-fastapi && poetry install`.
   - Streamlit: `cd pinochet-rettig-streamlit && poetry install`.

## Running Services (Makefile)

Run `make help` to see all targets.

Key commands:

- `make db.upd` — Start PostGIS dev container on `localhost:5433`.
- `make api.upd` — Start PostGIS + FastAPI (Docker) on `http://localhost:8888/docs`.
- `make api.upd.local` — Start PostGIS in Docker, then run FastAPI **locally** via `prestart.sh` on `http://localhost:8080/docs` (with `UVICORN_RELOAD=true`).
- `make ontop.upd` — Start PostGIS + Ontop on `http://localhost:8083`.
- `make streamlit.upd` — Start PostGIS + Streamlit on `http://localhost:8501`.

## Database

- **Dev DB**: `pinochet` on `localhost:5433`.
- **Test DB**: `pinochet_test` on `localhost:5434`.
- The `.env` credentials must match the dbt profile (see below) and `pinochet-rettig-fastapi/src/pinochet/settings.py`.

## dbt (data build tool)

- Project directory: `pinochet-rettig-dbt/dbt_pinochet/`.
- Profile name: `dbt_pinochet`.
- The repo provides `pinochet-rettig-dbt/dbt_pinochet/profiles/profiles.yml`. For local dbt CLI runs, copy or symlink it to `~/.dbt/profiles.yml`.
- Uses `elementary-data`. Generate reports with `edr report`.

## FastAPI

- **Entrypoint**: `pinochet.main:app` (under `src/`).
- **Environments**: Controlled by `API_ENV` env var.
  - `dev` (default): connects to `0.0.0.0:5433`.
  - `container_dev`: connects to `postgis:5432` (use inside Docker).
  - `test`: connects to `0.0.0.0:5434`.
  - `container_test`: connects to `postgis-test:5432` (use inside Docker).
  - `prod`: requires full env configuration.
- **Startup**: `prestart.sh` checks DB readiness, runs `alembic upgrade head`, seeds initial data, then starts uvicorn. Do not skip it.
- **Auth**: JWT-based. A default user is created by an Alembic migration for testing (see `alembic/versions/20240302_1709427186_4101c905126c_create_daniel_lopez_as_user.py`).
- **GraphQL**: Served at `/graphql` using `strawberry-graphql`.

## Streamlit

- Entrypoint is `src/app.py`.
- Version is bumped via `poetry-bumpversion` (configured in its `pyproject.toml`).

## Code Quality

- `pre-commit install` is required.
- Python 3.10 is the default version for hooks.
- **Black**: line-length 88.
- **Ruff**: configured in `ruff.toml`. Ignores `E501` (line length), `D401`, `D400`, `D415`.
- **SQLFluff**: uses `dbt-postgres` templater and `postgres` dialect (`.sqlfluff`). Ensure dbt deps are installed before linting SQL.

## CI / Deployment

- `.github/workflows/dbt-docs-generate.yml` triggers on pushes to `main` that affect dbt or fastapi paths.
- Deploys dbt docs + Elementary report to GitHub Pages.
- Deploys FastAPI to fly.io (requires `FLY_API_TOKEN` secret).
- dbt CI uses a custom image: `ghcr.io/diegoquintanav/pinochet-dbt:latest`.
