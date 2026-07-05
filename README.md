# pinochet-analyze-50

![dbt-badge](https://github.com/diegoquintanav/pinochet-analyze-50/actions/workflows/dbt-docs-generate.yml/badge.svg)

A repository portfolio for exploring the Pinochet-Rettig dataset. Read more about the dataset at [github.com/danilofreire/pinochet](https://github.com/danilofreire/pinochet).

**Live demos:**

- [dbt Docs](https://diegoquintanav.github.io/pinochet-analyze-50/dbt_docs)
- [Elementary Report](https://diegoquintanav.github.io/pinochet-analyze-50/elementary)
- [FastAPI Docs](https://pinochet-api.fly.dev/docs)
- [GraphQL](https://pinochet-api.fly.dev/graphql)

## Quick start

```bash
cp example.env .env
make install
make up
```

Then open:

- FastAPI: <http://localhost:8888/docs>
- Streamlit: <http://localhost:8501>
- Ontop SPARQL: <http://localhost:8083>

## Development

### One-time setup

```bash
# 1. Install dependencies for all services
make install

# 2. Install git hooks
pre-commit install
```

### Running services

| Command | Description |
|---------|-------------|
| `make up` | Start full stack (PostGIS + FastAPI + Streamlit + Ontop) |
| `make up.local` | Start PostGIS in Docker, run FastAPI + Streamlit locally |
| `make down` | Stop all services |
| `make test` | Run dbt tests + FastAPI pytest |
| `make db.upd` | Start PostGIS only |
| `make api.upd` | Start FastAPI in Docker |
| `make streamlit.upd` | Start Streamlit in Docker |
| `make ontop.upd` | Start Ontop SPARQL endpoint |

Check `make help` for a full list of available targets.

### Pre-commit

Run all hooks on staged files:

```bash
pre-commit run
```

Run all hooks on all files:

```bash
pre-commit run --all-files
```

Run a specific hook:

```bash
pre-commit run ruff
pre-commit run sqlfluff-lint
```

### Linting SQL

The root `.sqlfluff` uses the `dbt` templater for local runs (slower but more accurate). Pre-commit uses `.sqlfluff.fast` for speed.

```bash
# Lint all SQL files
sqlfluff lint pinochet-rettig-dbt/dbt_pinochet/models/

# Fix auto-fixable issues
sqlfluff fix pinochet-rettig-dbt/dbt_pinochet/models/
```

## Project structure

| Service | Description |
|---------|-------------|
| `pinochet-rettig-dbt/` | dbt project: raw CSV -> intermediate -> staging -> API tables |
| `pinochet-rettig-fastapi/` | FastAPI + Strawberry GraphQL + Alembic migrations |
| `pinochet-rettig-streamlit/` | Streamlit data exploration app |
| `pinochet-rettig-linked-data/` | Ontop virtual knowledge graph (SPARQL) |
| `postgis/` | PostGIS container definitions |

Every project has its own `README.md` and/or its own `Makefile` with more details.

## Stack

- **Data**: dbt, PostgreSQL 15 + PostGIS
- **API**: FastAPI, Strawberry GraphQL, Alembic, SQLAlchemy
- **Frontend**: Streamlit, GeoPandas, PyDeck
- **Linked Data**: Ontop, OWL, SPARQL
- **Tooling**: uv, pre-commit, Ruff, Black, sqlfluff
