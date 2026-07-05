# Pinochet FastAPI Service

REST API + GraphQL gateway for the Pinochet-Rettig dataset, backed by PostGIS.

## Quick start

Requires a running PostGIS dev database on `localhost:5433` (see root `docker-compose.postgis.yml`).

```bash
# 1. Install dependencies
uv sync

# 2. Start the API (includes DB readiness, alembic migrations, seeding)
API_ENV=dev ./prestart.sh
```

The API docs will be available at `http://localhost:8080/docs`.

## Environment variables

The app reads from `.env` via `python-decouple`. Dev defaults are hardcoded in `src/pinochet/settings.py`.

| Variable | Dev default | Purpose |
|----------|-------------|---------|
| `API_ENV` | `dev` | Runtime environment |
| `POSTGRES_HOST` | `0.0.0.0` | Database host |
| `POSTGRES_PORT` | `5433` | Database port |
| `POSTGRES_USER` | `dev_user` | Database user |
| `POSTGRES_PASSWORD` | `dev_password` | Database password |
| `POSTGRES_DB` | `pinochet` | Database name |
| `SECRET_KEY` | `dontusemeinprod` | JWT signing key |

## API overview

### REST endpoints (`/api/v1`)

All data endpoints require JWT authentication via `Authorization: Bearer <token>`.

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/auth/token` | `POST` | No | Login (OAuth2 password form) |
| `/api/v1/victims/` | `GET` | Yes | List victims |
| `/api/v1/victims/{id}` | `GET` | Yes | Get victim by ID |
| `/api/v1/events/` | `GET` | Yes | List events |
| `/api/v1/events/{id}` | `GET` | Yes | Get event by ID |
| `/api/v1/events/{id}/get_events_around/{radius}` | `GET` | Yes | Spatial query: events near a given event |
| `/api/v1/locations/` | `GET` | Yes | List or filter locations by name/ID |
| `/api/v1/locations/all` | `GET` | Yes | Paginated list of all locations |
| `/api/v1/users/me` | `GET` | Yes | Current user info |
| `/health` | `GET` | No | Health check (includes DB connectivity) |

### GraphQL (`/graphql`)

Strawberry GraphQL schema with queries for `victims`, `events`, and `locations`. Protected by `IsAuthenticated`.

## Default test user

The Alembic migration `4101c905126c_create_daniel_lopez_as_user.py` seeds a default user for local testing:

- **Username**: `daniel.lopez`
- **Password**: `rettig`

Get a token:

```bash
curl -X POST http://localhost:8080/api/v1/auth/token \
  -d "username=daniel.lopez" \
  -d "password=rettig"
```

## Architecture

- `src/pinochet/main.py` — App factory with CORS, health checks, GraphQL router
- `src/pinochet/api/v1/router.py` — V1 API router wiring
- `src/pinochet/models.py` — SQLAlchemy ORM models (Victim, Event, Location, User)
- `src/pinochet/settings.py` — Environment-based settings dispatch
- `alembic/` — Database migrations
- `prestart.sh` — Startup script: wait for DB, run migrations, seed data, start uvicorn

## Testing

```bash
# Requires test DB on localhost:5434
cd pinochet-rettig-fastapi
API_ENV=test uv run pytest
```

## Stack

- FastAPI + uvicorn
- SQLAlchemy 2.0 + Alembic
- Strawberry GraphQL
- JWT auth (python-jose + passlib)
- PostGIS (psycopg2-binary)
