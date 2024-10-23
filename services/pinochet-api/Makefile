.DEFAULT_GOAL := help
.PHONY: help

# source .env file
include .env

postgis_compose_file := ../../docker-compose.postgis.yml
compose_postgis := "-f $(postgis_compose_file)"


help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


db.upd: ## Start db container in detached mode
	@docker compose "$(compose_postgis)" up -d postgis

api.upd.local: ## Start api locally
	@echo "Running api server"
	@docker compose "$(compose_api)" up -d postgis
	@echo "Running prestart.sh"
	@UVICORN_RELOAD=true ./prestart.sh
	@echo "API server is running at http://localhost:8080/docs"
