.DEFAULT_GOAL := help
.PHONY: help

postgis_compose_file := docker-compose.postgis.yml
streamlit_compose_file := docker-compose.streamlit.yml
superset_compose_file:= docker-compose.superset-non-dev.yml

compose_superset := "-f $(postgis_compose_file) -f $(superset_compose_file)"
compose_streamlit := "-f $(postgis_compose_file) -f $(streamlit_compose_file)"

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dbt_docs.devserver: ## Regenerate dbt docs
	@DBT_PROJECT_DIR=$(DBT_PROJECT_DIR) dbt docs generate && dbt docs serve

streamlit.make_requirements: ## Regenerate requirements.txt
	@echo "Generating requirements.txt for streamlit at ./services/streamlit/requirements.txt"
	@poetry export -f requirements.txt --without-hashes --only streamlit -o ./services/streamlit/requirements.txt

streamlit.upd: ## Run streamlit dev server in detached mode
	@echo "Running streamlit dev server"
	@docker compose "$(compose_streamlit)" up -d

streamlit.down: ## Shut down streamlit containers
	@echo "Shutting down containers"
	@docker compose "$(compose_streamlit)" down

streamlit.ps: ## Get current streamlit services
	@docker compose "$(compose_streamlit)" ps

streamlit.build: streamlit.make_requirements ## Build streamlit image
	@echo "Building streamlit image"
	@docker compose "$(compose_streamlit)" build streamlit

streamlit.push: ## Push streamlit image
	@echo "Pushing streamlit image"
	@docker compose "$(compose_streamlit)" push streamlit

superset.upd: ## Run superset server in detached mode
	@echo "Running superset"
	@docker compose "$(compose_superset)" up -d

superset.down: ## Shut down superset containers
	@echo "Shutting down containers"
	@docker compose "$(compose_superset)" down

superset.ps: ## Get current superset services
	@docker compose "$(compose_superset)" ps