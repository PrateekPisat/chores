.PHONY: install format bump lint test

install:
	uv sync

format:
	uv run ruff check --fix src tests
	uv run ruff format src tests

bump:
	uv version --bump patch

lint:
	uv run ruff check src tests || exit 1
	uv run mypy src tests || exit 1
	uv run ruff format --check --diff src tests || exit 1

test:
	uv run coverage run -m pytest src tests
	uv run coverage report
