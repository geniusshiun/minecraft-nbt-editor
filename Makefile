# Minecraft NBT 編輯器 Makefile

.PHONY: help install install-dev test lint format clean build

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	uv pip install -e .

install-dev: ## Install development dependencies
	uv pip install -r requirements-dev.txt
	uv pip install -e .

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=src --cov-report=html

lint: ## Run linting
	flake8 src/
	mypy src/

format: ## Format code with black
	black src/

format-check: ## Check if code is formatted correctly
	black --check src/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build the package
	uv build

install-uv: ## Install uv if not already installed
	curl -LsSf https://astral.sh/uv/install.sh | sh

setup: install-uv install-dev ## Setup development environment
	@echo "Development environment setup complete!"
