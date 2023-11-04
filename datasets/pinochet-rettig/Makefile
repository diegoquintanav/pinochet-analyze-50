.DEFAULT_GOAL := help
.PHONY: help
ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

help: ## Print this help
	@grep -E '^[0-9a-zA-Z_\-\.]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

csv: ## Create csv files needed for the mapping
	@python3 scripts/prepare.py

yarrrml.parse: ## Parse rules.rml.ttl
	yarrrml-parser -i mapping.yarrrml.yml -o rules.rml.ttl

rmlmapper.run: ## Run rmlmapper from docker
	docker run --rm -v $(ROOT_DIR):/data rmlmapper -m rules.rml.ttl > mapped.rml.ttl