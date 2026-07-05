# AGENTS.md

High-signal notes for OpenCode agents working in this monorepo.

## Common Language Guidelines

* Use English for all code, comments, and documentation.
* Don't use em-dashes (—)
* Don't use emojis

## Project Management Guidelines

* Use Linear for issue tracking and project management.
* This project has a Linear Initiative in <https://linear.app/almudata/initiative/pinochet-50-open-data-220e094715de/overview>
* Issue tracking is entirely done in Linear. Do not use GitHub issues for tracking work.

## Project Structure

Root `pyproject.toml` is **not** a package (`package-mode = false`); it only pins shared dev tooling and dbt dependencies. Each service has its own `pyproject.toml` and must be installed separately.

Do not commit secrets (passwords, API keys, etc.) to the repo. Use `.env` files and `.gitignore` them. Use the `example.env` file as a template for `.env`. The `.env` file is sourced by the `Makefile` and read by FastAPI and Streamlit via `python-decouple`. Favor usage of environment variables when dealing with secrets.

* `pinochet-rettig-dbt/dbt_pinochet/` — dbt project (raw → intermediate → staging → `api` tables).
* `pinochet-rettig-fastapi/` — FastAPI + Strawberry GraphQL + Alembic.
* `pinochet-rettig-streamlit/` — Streamlit exploration app.
* `pinochet-rettig-linked-data/` — Ontop SPARQL virtual knowledge graph.
* `postgis/` — PostGIS container definitions.

## Environment Setup

1. Copy `example.env` to `.env` in the repo root. The `Makefile` sources this file; FastAPI and Streamlit also read it via `python-decouple`.
2. Install dependencies **per project**:
   * **Root**: `uv sync` (dbt, elementary, linting tools). Root `pyproject.toml` is `uv`-based and `package-mode = false`.
   * **FastAPI**: `cd pinochet-rettig-fastapi && uv sync`.
   * **Streamlit**: `cd pinochet-rettig-streamlit && uv sync`.

## Running Services (Makefile)

Run `make help` to see all targets.

Key commands:

* `make db.upd` — Start PostGIS dev container on `localhost:5433`.
* `make api.upd` — Start PostGIS + FastAPI (Docker) on `http://localhost:8888/docs`.
* `make api.upd.local` — Start PostGIS in Docker, then run FastAPI **locally** via `prestart.sh` on `http://localhost:8080/docs` (with `UVICORN_RELOAD=true`).
* `make ontop.upd` — Start PostGIS + Ontop on `http://localhost:8083`.
* `make streamlit.upd` — Start PostGIS + Streamlit on `http://localhost:8501`.

## Database

* **Dev DB**: `pinochet` on `localhost:5433` (user: `dev_user`, password: `dev_password`).
* **Test DB**: `pinochet` on `localhost:5434` (user: `test_user`, password: `test_password`).
* Dev credentials are hardcoded across docker-compose, dbt profiles, and FastAPI `DevSettings`. If you change them, update all three sources.

## dbt (data build tool)

* Project directory: `pinochet-rettig-dbt/dbt_pinochet/`.
* Profile name: `dbt_pinochet`.
* The repo provides `pinochet-rettig-dbt/dbt_pinochet/profiles/profiles.yml`.
* `.env` sets `DBT_PROFILES_DIR` so dbt finds the profile automatically. The `Makefile` also uses this variable.
* Uses `elementary-data`. Generate reports with `edr report`.

## FastAPI

* **Entrypoint**: `pinochet.main:app` (under `src/`).
* **Dependency management**: Uses `uv` with a `uv.lock` file. Dependencies are pinned with version constraints in `pyproject.toml`.
* **Documentation**: See `pinochet-rettig-fastapi/README.md` for endpoint reference, auth details, and architecture overview.
* **Environments**: Controlled by `API_ENV` env var.
  * `dev` (default): connects to `0.0.0.0:5433`.
  * `container_dev`: connects to `postgis:5432` (use inside Docker).
  * `test`: connects to `0.0.0.0:5434`.
  * `container_test`: connects to `postgis-test:5432` (use inside Docker).
  * `prod`: requires full env configuration.
* **Startup**: `prestart.sh` checks DB readiness, runs `alembic upgrade head`, seeds initial data, then starts uvicorn. Do not skip it.
* **Auth**: JWT-based. A default user is created by an Alembic migration for testing (see `alembic/versions/20240302_1709427186_4101c905126c_create_daniel_lopez_as_user.py`).
* **GraphQL**: Served at `/graphql` using `strawberry-graphql`.

## Streamlit

* Entrypoint is `streamlit_app.py`.
* Dependency management: Uses `uv` with `pyproject.toml` (PEP 621). Run `make install` to sync deps.
* **Local dev**: `make run.dev` — starts Streamlit with hardcoded dev credentials on `http://localhost:8501`.
* Version is bumped via `poetry-bumpversion` (legacy tool still referenced in `pyproject.toml`).

## Code Quality

* `pre-commit install` is required.
* Python 3.10 is the default version for hooks.
* **Black**: line-length 88.
* **Ruff**: configured in `ruff.toml`. Ignores `E501` (line length), `D401`, `D400`, `D415`.
* **SQLFluff**: uses `dbt-postgres` templater and `postgres` dialect (`.sqlfluff`). Ensure dbt deps are installed before linting SQL.

## CI / Deployment

* `.github/workflows/dbt-docs-generate.yml` triggers on pushes to `main` that affect dbt or fastapi paths.
* Deploys dbt docs + Elementary report to GitHub Pages.
* Deploys FastAPI to fly.io (requires `FLY_API_TOKEN` secret).
* dbt CI uses a custom image: `ghcr.io/diegoquintanav/pinochet-dbt:latest`.

## Branch Strategy

* `main` is always deployable.
* Short-lived branches from `main` (1-3 days max).
* Branch naming: `<username>/<linear-id>-<slug>` (e.g., `daquintanav/almud-188-fix-runtime-bugs`).
* Never push to `main` directly; merge only via GitHub PR with squash merge.
* Feature flags for risky or multi-merge changes.
* PRs require CI green + at least one approval.

## PR Management Rules

* A PR must always have a Linear issue assigned to the "Pinochet Showcase Portfolio" initiative, with the Linear ID in the PR description.
* Work on **ONE PR at a time**. Do not create multiple open PRs simultaneously unless they are part of the same Linear issue and user explicitly approves.
* Do not merge PRs without explicit user approval.
* **Approval is scoped to the current PR only** — approval for one PR does not carry over.
* Before creating a PR, check for `.github/pull_request_template.md` and use it to fill in the description. Include a summary of changes and the Linear issue reference under the `## References` header.
* Before merging any PR:
  1. Check for any open reviews (human or AI) on the PR.
  2. Verify CI is green (all checks passing).
  3. If both conditions are met, ask explicitly: "Ready to merge?"
  4. Only merge after user confirms.
* If there are unresolved reviews by any user (human or AI such as Copilot), address all comments individually before attempting to merge. Analyze whether the comment and suggested fix are pertinent, and prompt the user if changes are critical or too large.
* If you resolve a comment on the PR, add a reply with an AI disclaimer (e.g., "cuchufli") and mark it as resolved.
* If CI is not green, prompt the user to fix issues before merge.
* After a PR is merged, update the Linear issue to align with specs, and prompt the user if any new issues should be created. If no new Linear issues are pending, move the issue to done.

## AI Review Workflow

When an AI (such as Copilot) completes a review on a PR, follow this workflow:

1. **Fetch the review comments** using the GitHub API or CLI.
2. **Read each comment** and understand the issue.
3. **Explain the comment** to the user:
   * What is the issue?
   * What is the impact if not fixed?
   * Can it be fixed easily?
   * Should it be fixed?
4. **If Copilot proposed a code solution, evaluate it first**:
   * Is it relevant to the issue?
   * What is the impact of implementing it exactly as suggested?
   * Does it fit the project's architecture, patterns, and conventions?
   * Only consider an alternative fix if the proposed solution is inadequate.
5. **Evaluate the comment** and categorize it:
   * **Must fix**: correctness or security issues
   * **Should fix**: defensive practices, code clarity
   * **Optional**: style, preference, or minor issues
   * **Reject**: incorrect or irrelevant suggestions
6. **Summarize all proposed changes and prompt for approval**:
   * Produce a summary of what will be changed and why.
   * Ask the user for explicit approval before implementing any changes.
   * Do not begin implementation until the user confirms.
7. **Implement the fix** or explain why it won't be fixed.
8. **Reply to the comment** with an AI disclaimer (e.g., "cuchufli") and mark it as resolved.
9. **Push the fixes** and ensure CI is green.
10. **Request re-review** if major changes were made.

### Guidelines for AI Review Responses

* Always explain the impact of the issue before fixing it.
* Be transparent about tradeoffs.
* If rejecting a comment, explain why (e.g., "This is a false positive because...").
* Group related comments and fix them together.
* Don't blindly accept all AI suggestions — evaluate each one.
* When in doubt, ask the user for their preference.

## Pre-Push Checks

To avoid CI failures, run checks locally before pushing.

Current repo does not yet have a unified pre-push hook or check script. For now, run manually per service:

* **Root / dbt**: `dbt build --target dev`, `sqlfluff lint` (after `dbt deps`)
* **FastAPI**: `uv run pytest` (requires test DB on `localhost:5434`), `uv run ruff check .`, `uv run black --check .`
* **Streamlit**: `uv run ruff check .`, `uv run black --check .`

If you are unsure, ask the user for guidance on which checks to run.

## Updating this document

If the project structure or workflow changes, update this document accordingly. Notify the user of any significant changes that may affect their workflow.
