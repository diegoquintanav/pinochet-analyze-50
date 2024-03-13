.DEFAULT_GOAL := help
.PHONY: help

# source .env file
include .env

postgis_compose_file := docker-compose.postgis.yml
fastapi_compose_file := docker-compose.fastapi.yml
streamlit_compose_file := docker-compose.streamlit.yml
superset_compose_file:= docker-compose.superset-non-dev.yml

compose_postgis := "-f $(postgis_compose_file)"
compose_superset := "-f $(postgis_compose_file) -f $(superset_compose_file)"
compose_streamlit := "-f $(postgis_compose_file) -f $(streamlit_compose_file)"
compose_api := "-f $(postgis_compose_file) -f $(fastapi_compose_file)"

dbt_project_dir := $(shell pwd)/dbt_pinochet
dbt_profiles_dir := $(dbt_project_dir)/profiles

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dbt_docs.devserver: ## Regenerate dbt docs
	@DBT_PROJECT_DIR=$(dbt_project_dir) dbt docs generate && dbt docs serve --port 8089

dbt_build.dev_target: ## Run dbt build on target dev
	@DBT_PROJECT_DIR=$(dbt_project_dir) dbt build --profiles-dir $(dbt_profiles_dir) --target dev

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

