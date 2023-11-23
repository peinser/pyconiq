.PHONY: docs test examples

docs:
	poetry run mkdocs serve

lint:
	poetry run black --diff src/pyconiq
	poetry run ruff check src/pyconiq --fix
	poetry run mypy src/pyconiq

examples:
	poetry run black --diff examples
	poetry run ruff check examples --fix
	poetry run mypy examples

test:
	poetry run coverage run -m pytest --cov=src/pyconiq
