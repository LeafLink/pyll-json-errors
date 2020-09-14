# Script constants
PWD=`pwd`
DJANGO_SETTINGS_MODULE=drivers.django_rest_framework.myapi.myapi.settings
SDOCS_DIST_DIR=$(PWD)/sdocs/dist
SDOCS_SERVE_DIR=$(PWD)/sdocs/serve
SDOCS_SOURCE_DIR=$(PWD)/sdocs/src
SDOCS_PORT=5001

.DEFAULT_GOAL := help

docs-build:
	@echo "Build HTML documentation via sphinx..."
	mkdir -p $(SDOCS_DIST_DIR)
	make _sphinx-build-html target="$(SDOCS_DIST_DIR)"

docs-serve:
	@echo "Serving HTML documentation on port $(SDOCS_PORT)..."
	mkdir -p $(SDOCS_SERVE_DIR)
	make _sphinx-serve-html target="$(SDOCS_SERVE_DIR)"

_sphinx-build-html:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) \
		poetry run sphinx-build -b html $(SDOCS_SOURCE_DIR) $(target)/html

_sphinx-serve-html:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) \
		poetry run sphinx-autobuild $(SDOCS_SOURCE_DIR) $(target)/html --port $(SDOCS_PORT)

docs-build-docker:
	@echo "Cleaning up old ./dist directory..."
	rm -r $(SDOCS_DIST_DIR) || true
	@echo "Building container image..."
	docker build -t pyll-json-errors .
	@echo "Generating sphinx docs and outputting to $(SDOCS_DIST_DIR)..."
	docker run --rm -v $(SDOCS_DIST_DIR)/:/usr/src/app/sdocs/dist/ --entrypoint make pyll-json-errors:latest docs-build

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
	@echo "  Make Commands Help Menu"
	@echo "  |"
	@echo "  |_ help (default)          - Show this message."
	@echo "  |_ docs-build              - Build package documentation HTML."
	@echo "  |_ docs-build-docker       - Build package documentation HTML in Docker. Outputs to ./dist."
	@echo "  |_ docs-serve              - Start a PDocs development server."
	@echo "  |_ format                  - Lint code and fix any errors."
	@echo "  |_ lint                    - Lint code, does not fix any errors."
	@echo "  |_ test                    - Run unit tests."
	@echo "  |_ test-ci                 - Run unit tests and generate coverage reports."
	@echo "  |____________________________________________________________________"
	@echo " "

.PHONY:
	docs-build
	docs-build-docker
	docs-serve
	format
	lint
	test
	test-ci
