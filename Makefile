CODE_DIR = .

flake8-check:
	poetry run flake8 $(CODE_DIR)

pre-commit-run:
	poetry run pre-commit run --all-files

check: flake8-check pre-commit-run

.PHONY: code-check
