CODE_DIR = .

flake8-check:
	poetry run flake8 $(CODE_DIR)

black-check:
	poetry run black --check $(CODE_DIR)

pre-commit-run:
	poetry run pre-commit run --all-files

code-check: flake8-check black-check pre-commit-run

.PHONY: code-check
