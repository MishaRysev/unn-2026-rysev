.PHONY: test format format-check lint lint-fix typecheck check build

test:
	uv run python -m unittest discover -s tests -v

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

typecheck:
	uv run mypy bot/ main.py

check: lint format-check typecheck test

build:
	docker build -t echo-bot .