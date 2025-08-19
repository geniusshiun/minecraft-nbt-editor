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

release: ## Build and prepare release
	@echo "🚀 準備 Release..."
	@echo "1. 檢查 git 狀態..."
	@git status --porcelain || echo "⚠️  有未提交的變更"
	@echo "2. 建置套件..."
	uv build
	@echo "3. 檢查 dist 檔案..."
	@ls -la dist/ || echo "❌ dist 目錄不存在"
	@echo "✅ Release 準備完成！"
	@echo "📋 下一步：在 GitHub 上建立 Release 並上傳 dist/ 檔案"

tag: ## Create and push git tag
	@echo "🏷️  建立 Git Tag..."
	@read -p "輸入版本號 (例如: v0.2.0): " version; \
	git tag -a $$version -m "Release $$version"; \
	git push origin $$version; \
	echo "✅ Tag $$version 已建立並推送"

install-uv: ## Install uv if not already installed
	curl -LsSf https://astral.sh/uv/install.sh | sh

setup: install-uv install-dev ## Setup development environment
	@echo "Development environment setup complete!"
