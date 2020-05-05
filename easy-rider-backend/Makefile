.PHONY: config install lint full-lint test build clean all ci
.DEFAULT_GOAL := all

all: install lint test build
ci: all

VIRTUAL_ENV = .venv
BIN = .venv/bin/
PYTHON = `python`
POETRY_VERSION = 1.0.3
PIP_VERSION = 20.0.2

TAG ?= latest
DEV ?= 1

config:
	poetry config virtualenvs.create `if [ "${DEV}" = "0" ]; then echo false; else echo true; fi`
	mkdir -p ~/.config/pypoetry/ | true

prepare:
	pip install pip==${PIP_VERSION}
	pip install poetry==${POETRY_VERSION}

install:
	make prepare
	make config
	poetry install -v `if [ "${DEV}" = "0" ]; then echo "--no-dev --no-interaction --no-ansi"; fi`

lint:
	poetry run isort --recursive config project
	poetry run flake8 --max-line-length=140 config project || true

full-lint:
	poetry run isort --recursive config project
	poetry run pylint config project || poetry run pylint-exit $$?

test:
	poetry run python manage.py test

build:
	poetry build

clean:
	rm -rf build dist

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

createsuperuser:
	poetry run python manage.py createsuperuser

run: install
	poetry run python manage.py runserver
