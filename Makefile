.PHONY: run clean test help lint

# Variables 
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip


run: $(VENV)/bin/activate
	$(PYTHON) -m flask run

test: $(VENV)/bin/activate
	source $(VENV)/bin/activate; ./run_tests.sh

lint: $(VENV)/bin/activate
	source $(VENV)/bin/activate; ./run_pylint.sh

help:
	@echo "Makefile commands:"
	@echo "  make run     - Run Flask app"
	@echo "  make test    - Run tests"
	@echo "  make clean   - Delete venv and cache"

venv/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	${PIP} install -r requirements.txt || true
	$(PIP) list --format=freeze | diff - requirements.txt || $(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)