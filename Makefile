
# Exported variables for subshells, and their default values
export PYTHONPATH 	:= $(PWD)

# Loading .env if exists. This file can override the variables above.
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

#############################
# DOCKER COMMANDS           #
#############################

.PHONY: format
# Format code inside docker
format:
	@echo "Running Black..."
	@black .

.PHONY: test
# Run Tests inside docker.
test:
	@echo "Running Tests..."
	@pytest --ignore=migrations



.PHONY: bandit
# Run Bandit inside Docker.
bandit:
	@echo "Running Bandit..."
	@bandit -r .

.PHONY: pylint
# Run Pylint inside Docker.
pylint:
	@echo "Running PyLint..."
	@pylint core datasource_fgts

.PHONY: black
# Run Black inside Docker.
black:
	@echo "Running Black..."
	@black --check .

.PHONY: precommit
# Run Pre-Commit inside Docker.
pre-commit:
	@echo "Running Pre-Commit..."
	@pre-commit install -f
	@pre-commit run --all

.PHONY: lint
# Run Bandit, Lint, Unit Tests and Coverage inside docker.
lint: pre-commit coverage
	@echo "Finish Lint"



#############################
# VIRTUALENV COMMANDS       #
#############################

.PHONY: install
# Install or Reinstall Application
install:
	@poetry install
	@poetry run pre-commit install -f


.PHONY: shell
# Open a shell, with virtualenv and .env loaded
# Run 'dotenv list' to see all environment variables loaded in shell
shell:
	@poetry shell


.PHONY: vtest
# Run Tests
vtest:
	@poetry run python manage.py test
