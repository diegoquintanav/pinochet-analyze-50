.DEFAULT_GOAL := help
.PHONY: help

# source .env file
include .env

postgis_compose_file := docker-compose.postgis.yml
fastapi_compose_file := docker-compose.fastapi.yml
streamlit_compose_file := docker-compose.streamlit.yml
ontop_compose_file := docker-compose.ontop.yml

compose_postgis := "-f $(postgis_compose_file)"
compose_streamlit := "-f $(postgis_compose_file) -f $(streamlit_compose_file)"
compose_api := "-f $(postgis_compose_file) -f $(fastapi_compose_file)"
compose_ontop := "-f $(postgis_compose_file) -f $(ontop_compose_file)"

dbt_project_dir ?= $(DBT_PROJECT_DIR)
dbt_project_dir ?= $(shell pwd)/pinochet-rettig-dbt/dbt_pinochet
dbt_profiles_dir ?= $(DBT_PROFILES_DIR)
dbt_profiles_dir ?= $(dbt_project_dir)/profiles

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dbt_docs.devserver: ## Regenerate dbt docs
	@DBT_PROJECT_DIR=$(dbt_project_dir) dbt docs generate && dbt docs serve --port 8089

dbt_build.dev_target: ## Run dbt build on target dev
	@DBT_PROJECT_DIR=$(dbt_project_dir) dbt build --profiles-dir $(dbt_profiles_dir) --target dev

db.upd: ## Start db container in detached mode
	@docker compose "$(compose_postgis)" up -d postgis

db.psql: ## Run psql on postgres container
	@docker compose "$(compose_postgis)" exec postgis psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

api.upd: ## Run api server in detached mode
	@echo "Running api server"
	@docker compose "$(compose_api)" up -d
	@echo "API server is running at http://localhost:8888/docs"

api.down: ## Shut down api containers
	@echo "Shutting down containers"
	@docker compose "$(compose_api)" down

api.bash: ## Run bash on fastapi container
	@docker compose "$(compose_api)" exec -it fastapi bash

api.ps: ## Get current api services in compose format
	@docker compose "$(compose_api)" ps

api.build: ## Build fastapi image
	@docker compose "$(compose_api)" build fastapi

api.logs: ## Get api logs
	@docker compose "$(compose_api)" logs --follow --tail 100

api.push: ## Push fastapi image to registry
	@docker compose "$(compose_api)" push fastapi

api.upd.local: ## Start api locally
	@echo "Running api server"
	@docker compose "$(compose_api)" up -d postgis
	@echo "Running prestart.sh"
	@cd pinochet-rettig-fastapi && UVICORN_RELOAD=true ./prestart.sh
	@echo "API server is running at http://localhost:8080/docs"

ontop.upd: ## Run ontop server in detached mode
	@echo "Running ontop server"
	@docker compose "$(compose_ontop)" up -d
	@echo "Ontop server is running at http://localhost:8083"

ontop.logs: ## Get ontop logs
	@docker compose "$(compose_ontop)" logs --follow --tail 100

ontop.down: ## Shut down ontop containers
	@docker compose "$(compose_ontop)" down

streamlit.build: ## Build streamlit image
	@docker compose "$(compose_streamlit)" build streamlit

streamlit.upd: ## Run streamlit server in detached mode
	@echo "Running streamlit server"
	@docker compose "$(compose_streamlit)" up -d
	@echo "Streamlit server is running at http://localhost:8501"

streamlit.logs: ## Get streamlit logs
	@docker compose "$(compose_streamlit)" logs --follow --tail 100

streamlit.down: ## Shut down streamlit containers
	@docker compose "$(compose_streamlit)" down

# ---------------------------------------------------------------------------- #
#                           unified stack commands                             #
# ---------------------------------------------------------------------------- #

install: ## Install dependencies for all services via uv
	@echo "Installing root dependencies..."
	@uv sync
	@echo "Installing FastAPI dependencies..."
	@cd pinochet-rettig-fastapi && uv sync
	@echo "Installing Streamlit dependencies..."
	@cd pinochet-rettig-streamlit && uv sync
	@echo "Installing dbt dependencies..."
	@cd pinochet-rettig-dbt && uv sync
	@echo "Done. Run 'pre-commit install' to set up git hooks."

up: ## Start full stack (PostGIS + FastAPI + Streamlit + Ontop) via docker compose
	@docker compose -f docker-compose.yml up -d
	@echo "Full stack is starting..."
	@echo "  FastAPI:    http://localhost:8888/docs"
	@echo "  Streamlit:  http://localhost:8501"
	@echo "  Ontop:      http://localhost:8083"

down: ## Stop all services
	@docker compose -f docker-compose.yml down

up.local: ## Start PostGIS in Docker, then FastAPI and Streamlit locally
	@echo "Starting PostGIS..."
	@docker compose -f docker-compose.postgis.yml up -d postgis
	@echo "Waiting for PostGIS to be ready..."
	@sleep 5
	@echo "Running dbt build..."
	@DBT_PROJECT_DIR=$(dbt_project_dir) DBT_PROFILES_DIR=$(dbt_profiles_dir) uv run dbt build --target dev || true
	@echo "Starting FastAPI locally..."
	@export POSTGRES_USER=dev_user POSTGRES_PASSWORD=dev_password POSTGRES_DB=pinochet POSTGRES_HOST=localhost POSTGRES_PORT=5433 && cd pinochet-rettig-fastapi && API_ENV=dev ./prestart.sh &
	@echo "Starting Streamlit locally..."
	@cd pinochet-rettig-streamlit && POSTGRES_USER=dev_user POSTGRES_PASSWORD=dev_password POSTGRES_DB=pinochet POSTGRES_HOST=localhost POSTGRES_PORT=5433 uv run streamlit run streamlit_app.py &
	@echo "Local services started:"
	@echo "  FastAPI:   http://localhost:8080/docs"
	@echo "  Streamlit: http://localhost:8501"

test: ## Run all tests (dbt tests + FastAPI pytest + smoke checks)
	@echo "Running dbt tests..."
	@DBT_PROJECT_DIR=$(dbt_project_dir) DBT_PROFILES_DIR=$(dbt_profiles_dir) uv run dbt test --target dev
	@echo "Running FastAPI tests..."
	@cd pinochet-rettig-fastapi && API_ENV=test uv run pytest
	@echo "All tests passed."