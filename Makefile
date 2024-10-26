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

dbt_project_dir := $(shell pwd)/pionchet-rettig-dbt/dbt_pinochet
dbt_profiles_dir := $(dbt_project_dir)/profiles

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

streamlit.upd: ## Run streamlit server in detached mode
	@echo "Running streamlit server"
	@docker compose "$(compose_streamlit)" up -d
	@echo "Streamlit server is running at http://localhost:8501"

streamlit.logs: ## Get streamlit logs
	@docker compose "$(compose_streamlit)" logs --follow --tail 100

streamlit.down: ## Shut down streamlit containers
	@docker compose "$(compose_streamlit)" down