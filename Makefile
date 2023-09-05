.DEFAULT_GOAL := help
.PHONY: help

streamlit_compose_file := docker-compose.streamlit.yml

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dbt_docs.devserver: ## Regenerate dbt docs
	@DBT_PROJECT_DIR=$(DBT_PROJECT_DIR) dbt docs generate && dbt docs serve

streamlit.make_requirements: ## Regenerate requirements.txt
	@echo "Generating requirements.txt for streamlit at ./services/streamlit/requirements.txt"
	@poetry export -f requirements.txt --without-hashes --only streamlit -o ./services/streamlit/requirements.txt

streamlit.devserver: ## Run streamlit dev server in detached mode
	@echo "Running streamlit dev server"
	@docker compose -f $(streamlit_compose_file) up -d

streamlit.build: ## Build streamlit image
	@echo "Building streamlit image"
	@docker compose -f $(streamlit_compose_file) build

streamlit.push: ## Push streamlit image
	@echo "Pushing streamlit image"
	@docker compose -f $(streamlit_compose_file) push