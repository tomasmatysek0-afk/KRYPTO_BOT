.PHONY: install install-dev test lint help no-secrets

PYTHON ?= python

install:
	# [LOCAL_VENV]
	$(PYTHON) -m pip install --upgrade pip
	# [LOCAL_VENV]
	$(PYTHON) -m pip install -e .

install-dev:
	# [LOCAL_VENV]
	$(PYTHON) -m pip install -e ".[dev]"

test:
	# [LOCAL_VENV]
	$(PYTHON) -m pytest

lint:
	# [LOCAL_VENV]
	ruff check .

help:
	# [LOCAL_VENV]
	$(PYTHON) -m coinbase_freqtrade_guarded_bot --help

no-secrets:
	# [HOST_POWERSHELL]
	powershell -ExecutionPolicy Bypass -File scripts/dev.ps1 no-secrets
