VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: all install run test clean

all: install test

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@echo "\n--- Environment Setup Complete ---"
	@echo "Try running: make run ARGS='translate --sport Football --role Captain'"

run:
	$(PYTHON) main.py $(ARGS)

test:
	$(PYTHON) -m pytest tests/

clean:
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/core/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache