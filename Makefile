# Makefile for handy-fingers development
# Targets: run, test, lint, demo, clean

PYTHON := python3
PIP := $(PYTHON) -m pip
SRC_DIR := src/handy_fingers
TEST_DIR := tests

.PHONY: help install install-dev run test lint format clean demo

help:  ## Show this help message
	@echo "🖐️  handy-fingers Makefile"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in editable mode
	$(PIP) install -e .

install-dev:  ## Install package with dev dependencies
	$(PIP) install -e ".[dev]"

run:  ## Run the finger counter (default camera)
	$(PYTHON) -m handy_fingers.app

demo:  ## Run with spell mode and watermark
	$(PYTHON) -m handy_fingers.app --spell-mode --watermark

test:  ## Run test suite
	$(PYTHON) -m pytest $(TEST_DIR) -v

test-cov:  ## Run tests with coverage report
	$(PYTHON) -m pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html

lint:  ## Run linters (ruff)
	$(PYTHON) -m ruff check $(SRC_DIR) $(TEST_DIR)

format:  ## Format code with black and isort
	$(PYTHON) -m black $(SRC_DIR) $(TEST_DIR)
	$(PYTHON) -m isort $(SRC_DIR) $(TEST_DIR)

format-check:  ## Check code formatting without changes
	$(PYTHON) -m black --check $(SRC_DIR) $(TEST_DIR)
	$(PYTHON) -m isort --check-only $(SRC_DIR) $(TEST_DIR)

smoke-test:  ## Headless smoke test (no camera display)
	$(PYTHON) -m handy_fingers.app --no-video & sleep 3 && pkill -f handy_fingers.app

clean:  ## Remove build artifacts and cache
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

recalibrate:  ## Force re-run calibration wizard
	$(PYTHON) -m handy_fingers.app --recalibrate
