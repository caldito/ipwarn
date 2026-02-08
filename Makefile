VERSION ?= 2.0.0
VENV ?= .venv
UV ?= uv

.PHONY: help setup install dev-install test lint format build-docker build-docker-multi push-docker clean run run-once

help:           ## Show this help message
	@echo 'Usage: make [target]'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup:          ## Setup development environment with uv and venv
	@command -v $(UV) >/dev/null 2>&1 || { echo "uv not found. Install it from https://github.com/astral-sh/uv"; exit 1; }
	$(UV) venv $(VENV)
	$(UV) pip install -e ".[dev]"

install:        ## Install the package locally
	$(UV) pip install -e .

dev-install:    ## Setup development environment (alias for setup)
	$(MAKE) setup

test:           ## Run tests
	$(VENV)/bin/pytest tests/ -v

lint:           ## Run linters
	$(VENV)/bin/ruff check ipwarn/ tests/
	$(VENV)/bin/mypy ipwarn/

format:         ## Format code
	$(VENV)/bin/black ipwarn/ tests/
	$(VENV)/bin/ruff check --fix ipwarn/ tests/

build-docker:   ## Build Docker image for current architecture
	docker build -t pablogcaldito/ipwarn:$(VERSION) .

build-docker-multi:  ## Build Docker image for multiple architectures
	docker buildx build --platform linux/amd64,linux/arm64 -t pablogcaldito/ipwarn:$(VERSION) .

push-docker:    ## Push Docker image to registry
	docker push pablogcaldito/ipwarn:$(VERSION)

run:            ## Run ipwarn with default config
	$(VENV)/bin/python -m ipwarn --config config/ipwarn.conf

run-once:       ## Run ipwarn once (for testing)
	$(VENV)/bin/python -m ipwarn --config config/ipwarn.conf --once

clean:          ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info __pycache__ ipwarn/__pycache__ ipwarn/**/*.pyc
	find . -type d -name __pycache__ -exec rm -rf {} + || true
