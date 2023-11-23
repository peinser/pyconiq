.PHONY: docs test

docs:
	poetry run mkdocs serve

lint:
	poetry run black --diff src/pyconiq
	poetry run ruff check src/pyconiq --fix
	poetry run mypy src/pyconiq

test:
	poetry run coverage run -m pytest --cov=src/pyconiq
