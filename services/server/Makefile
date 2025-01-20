.PHONY: install format bump lint test

install:
	poetry install

format:
	ruff check --fix src tests
	ruff format src tests

bump:
	poetry version patch

lint:
	ruff check src tests || exit 1
	mypy src tests || exit 1
	ruff format --check --diff src tests || exit 1

test:
	coverage run -m pytest src tests
	coverage report
