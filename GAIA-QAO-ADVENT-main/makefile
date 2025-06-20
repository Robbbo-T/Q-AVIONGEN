# Makefile for GAIA-QAO-AdVent Project
#
# Provides a standard, unified interface for common development and operational tasks.
# Run 'make help' to see a list of available commands.

# --- Variables and Configuration ---
# Use the shell to find all service directories that have a Dockerfile.dev
# This makes the Makefile more dynamic.
SERVICES := $(shell find * -maxdepth 1 -type d -print)

# Default shell to bash for more advanced features
SHELL := /bin/bash

# --- Helper for Self-documented Commands ---
# This is a common pattern to make 'help' target work.
# It finds comments starting with ## and prints them.
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# --- Local Development Environment (Docker Compose) ---
.PHONY: setup start stop down restart logs ps clean
setup: ## ✨ First-time setup: Initializes the entire local development environment.
	@echo "--- Running full project setup ---"
	@./scripts/setup.sh

start: ## 🚀 Start: Starts all local services in detached mode. Alias for 'up'.
up:
	@echo "--- Starting local services ---"
	@./scripts/start.sh up

stop: ## 🛑 Stop: Stops all running local services without removing them.
	@echo "--- Stopping local services ---"
	@./scripts/start.sh stop

down: ## 🔽 Down: Stops and removes all containers, networks, and services.
	@echo "--- Bringing down local environment ---"
	@./scripts/start.sh down

restart: ## 🔄 Restart: Restarts the entire local environment (down + up).
	@echo "--- Restarting local environment ---"
	@./scripts/start.sh restart

logs: ## 📜 Logs: Follows the logs of all running services.
	@echo "--- Tailing logs (Press Ctrl+C to exit) ---"
	@./scripts/start.sh logs

ps: ## 📊 Status: Shows the status of all running services.
	@echo "--- Current service status ---"
	@./scripts/start.sh ps

clean: ## 🧹 Clean: Stops services and removes all volumes and orphaned containers. DANGEROUS!
	@echo "--- Cleaning local environment (includes volumes) ---"
	@./scripts/start.sh clean

# --- Testing ---
.PHONY: test test-unit test-integration test-e2e test-quantum test-all
test: test-unit ## 🧪 Test: Runs the default (unit) test suite.

test-unit: ## Runs only the fast unit tests.
	@echo "--- Running unit test suite ---"
	@./scripts/test.sh unit

test-integration: ## Runs integration tests (requires Docker environment to be running).
	@echo "--- Running integration test suite ---"
	@./scripts/test.sh integration

test-e2e: ## Runs end-to-end tests simulating a full user/mission flow.
	@echo "--- Running E2E test suite ---"
	@./scripts/test.sh e2e

test-quantum: ## Runs tests specific to quantum algorithms and simulators.
	@echo "--- Running quantum test suite ---"
	@./scripts/test.sh quantum

test-all: ## Runs ALL test suites sequentially.
	@echo "--- Running all test suites ---"
	@./scripts/test.sh all

# --- Build & Deployment ---
# Note: These are placeholders for a more complex CI/CD pipeline.
.PHONY: build-prod deploy-staging deploy-prod
build-prod: ## 📦 Build (Prod): Builds all production-ready container images.
	@echo "--- Building production images ---"
	@docker-compose -f docker-compose.prod.yml build

deploy-staging: ## 🚢 Deploy (Staging): Deploys the 'develop' branch to the staging environment.
	@echo "--- Deploying to Staging Environment ---"
	@./scripts/deploy.sh staging BWBQ100

deploy-prod: ## 🚀 Deploy (Production): Deploys the 'main' branch to the production environment.
	@echo "--- DEPLOYING TO PRODUCTION ENVIRONMENT ---"
	@read -p "ARE YOU ABSOLUTELY SURE YOU WANT TO DEPLOY TO PRODUCTION? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		./scripts/deploy.sh production BWBQ100; \
	else \
		echo "Production deployment cancelled."; \
	fi

# --- Linting & Formatting ---
.PHONY: lint format
lint: ## 📜 Lint: Runs linters across the codebase (e.g., ESLint, Flake8).
	@echo "--- Running linters ---"
	# Add specific linting commands here, e.g.:
	# npm run lint
	# flake8 .
	@echo "Linting complete (simulation)."

format: ## 🎨 Format: Automatically formats code using tools like Prettier, Black, rustfmt.
	@echo "--- Formatting codebase ---"
	# Add specific formatting commands here, e.g.:
	# npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,md}"
	# black .
	@echo "Formatting complete (simulation)."
