.PHONY: requirements run dev env

ENV=.env
PYTHON_VERSION=3
PYTHON=python${PYTHON_VERSION}
IN_ENV=. ${ENV}/bin/activate;
PACKAGE_VERSION=$(shell cat VERSION)

default: env requirements

env:
	@echo "Creating Python environment..." >&2
	@${PYTHON} -m venv ${ENV}
	@echo "Updating pip..." >&2
	@${IN_ENV} ${PYTHON} -m pip install -U pip setuptools

requirements: env
	@${IN_ENV} ${PYTHON} -m pip install -r requirements.txt


run: env requirements
	@${IN_ENV} ${PYTHON} -m pip install -e ./
	@${IN_ENV} gunicorn -w 1 capytcha_server.app:create_app --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker


dev: env requirements
	@${IN_ENV} ${PYTHON} -m pip install -e ./
	@${IN_ENV} gunicorn -w 1 capytcha_server.app:create_app --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker --reload --access-logfile - --log-level debug