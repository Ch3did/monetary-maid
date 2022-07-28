
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

.PHONY: coverage
# Run Tests with Coverage inside Docker.
coverage:
	@echo "Running Tests with Coverage..."
	@pytest --cov=./datasource_fgts --ignore=migrations

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

.PHONY: update
# Update application dependencies
update:
	@poetry update --lock
	@echo "Update complete. Please rebuild DevContainer."

.PHONY: coverage_and_report
# Prepare and Send Coverage Report inside Docker
coverage_and_report: coverage
	@coverage xml

.PHONY: migrate
# Run database migration
migrate:
	@python manage.py migrate

.PHONY: migrations
# Create database migrations
migrations:
	@python manage.py makemigrations

#############################
# VIRTUALENV COMMANDS       #
#############################

.PHONY: install
# Install or Reinstall Application
install:
	@poetry install
	@poetry run pre-commit install -f

.PHONY: develop
# Run Application. Use SERVER_HOST and SERVER_PORT to define address
develop:
	@poetry run python manage.py runserver 0.0.0.0:8023

.PHONY: shell
# Open a shell, with virtualenv and .env loaded
# Run 'dotenv list' to see all environment variables loaded in shell
shell:
	@poetry shell

.PHONY: vformat
# Format code in virtualenv
vformat:
	@poetry run black .

.PHONY: vtest
# Run Tests
vtest:
	@poetry run python manage.py test

.PHONY: vlint
# Run Pre-Commit, Unit Tests and Coverage in virtualenv.
vlint:
	@echo "Running Pre-Commit..."
	@poetry run pre-commit run --all
	@echo "Running Django Tests with Coverage..."
	@poetry run pytest --cov=./ --ignore=migrations

.PHONY: vmigrate
# Run database migration
vmigrate:
	@poetry run python manage.py migrate

.PHONY: config_project
# Automate first install
config_project:
	@echo ">>> Removing Python 3.8 virtualenv if exists..."
	@poetry env remove 3.8 2>/dev/null || :
	@echo ">>> Install Dependencies ..."
	@poetry install
	@echo ">>> Running Git ..."
	@git init && git add . && git commit -m "chore(cookie): first commit"
	@echo ">>> Opening VSCode..."
	@cp env.credentials .env && code .
