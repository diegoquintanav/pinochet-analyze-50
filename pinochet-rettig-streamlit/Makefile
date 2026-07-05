.DEFAULT_GOAL := help
.PHONY: help install run run.dev

# Load env from repo root if available
-include ../.env

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies with uv
	@uv sync

run: ## Run Streamlit app (requires ../.env or manual env vars)
	@uv run streamlit run streamlit_app.py

run.dev: ## Run Streamlit app with hardcoded dev credentials
	@POSTGRES_USER=dev_user \
	 POSTGRES_PASSWORD=dev_password \
	 POSTGRES_DB=pinochet \
	 POSTGRES_HOST=localhost \
	 POSTGRES_PORT=5433 \
	 uv run streamlit run streamlit_app.py
