.PHONY: install format lint test test-unit test-integration run docs clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  install          Install dependencies"
	@echo "  format           Format code with ruff"
	@echo "  lint             Lint code with ruff and mypy"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  run              Run the development server"
	@echo "  docs             Generate documentation"
	@echo "  clean            Clean up temporary files"

install:
	uv pip install -e ".[dev]"

format:
	ruff format .
	ruff check --fix .

lint:
	ruff check .
	mypy src/

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

run:
	uvicorn pygridfight.main:app --reload --host 0.0.0.0 --port 8000

docs:
	@echo "Documentation generation not yet implemented"

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf dist/
	rm -rf build/