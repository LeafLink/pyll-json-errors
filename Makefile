# Script constants
.DEFAULT_GOAL := help
LOCALHOST=0.0.0.0
PDOCS_PORT=5001


docs-server:
	@echo "Running PDocs development server on port $(PDOCS_PORT)"
	DJANGO_SETTINGS_MODULE=drivers.django_rest_framework.myapi.myapi.settings \
	poetry run pdoc pyll_json_errors --html --template-dir docs/pdoc_templates --http $(LOCALHOST):$(PDOCS_PORT)

format:
	@echo "Linting and fixing code..."
	poetry run autoflake ./pyll_json_errors --in-place --remove-all-unused-import --ignore-init-module-imports -r
	poetry run isort ./pyll_json_errors
	poetry run black . --config=./pyproject.toml

lint:
	@echo "Linting code..."
	poetry run autoflake ./pyll_json_errors --remove-all-unused-import --ignore-init-module-imports -r
	poetry run isort ./pyll_json_errors -c
	poetry run black . --config=./pyproject.toml --check

test:
	@echo "Testing code..."
	poetry run pytest -c ./setup.cfg --cov-report term-missing

test-ci:
	@echo "Testing code..."
	poetry run pytest -c ./setup.cfg \
		--cov-report=xml:./test-results/coverage.xml \
		--junitxml=./test-results/pytest/results.xml \


# Help Docs
help:
	@echo "  LeafLink Mail Service Commands"
	@echo "  |"
	@echo "  |_ help (default)          - Show this message."
	@echo "  |_ docs-server             - Start a PDocs development server."
	@echo "  |_ format                  - Lint code and fix any errors."
	@echo "  |_ lint                    - Lint code, does not fix any errors."
	@echo "  |_ test                    - Run unit tests."
	@echo "  |_ test-ci                 - Run unit tests and generate coverage reports."
	@echo "  |____________________________________________________________________"
	@echo " "

.PHONY:
	docs-server
	format
	lint
	test
	test-ci
