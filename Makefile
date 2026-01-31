.PHONY: help setup install test clean deploy

# Variables
PYTHON=python3
NODE=node
NPM=npm
PIP=pip
VENV=venv
REQUIREMENTS=requirements.txt

help:
	@echo "Quantum JV Platform - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  setup     - Setup development environment"
	@echo "  install   - Install all dependencies"
	@echo "  python    - Install Python dependencies"
	@echo "  node      - Install Node.js dependencies"
	@echo "  test      - Run tests"
	@echo "  clean     - Clean build artifacts"
	@echo "  run       - Run development server"
	@echo "  deploy    - Deploy to production"
	@echo "  docs      - Generate documentation"
	@echo "  lint      - Run linting"

setup:
	@echo "Setting up development environment..."
	chmod +x scripts/setup_environment.sh
	./scripts/setup_environment.sh

install: python node
	@echo "All dependencies installed"

python:
	@echo "Installing Python dependencies..."
	if [ ! -d "$(VENV)" ]; then $(PYTHON) -m venv $(VENV); fi
	. $(VENV)/bin/activate && $(PIP) install -r $(REQUIREMENTS)

node:
	@echo "Installing Node.js dependencies..."
	cd src/react && $(NPM) install
	cd src/node && $(NPM) install

test:
	@echo "Running tests..."
	. $(VENV)/bin/activate && python -m pytest tests/ -v
	cd src/node && $(NPM) test

run:
	@echo "Starting development servers..."
	@echo "1. Python API: http://localhost:8000"
	@echo "2. React App: http://localhost:3000"
	@echo "3. Documentation: http://localhost:8080"
	. $(VENV)/bin/activate && python src/python/api_server.py &
	cd src/react && $(NPM) start &
	cd docs && python -m http.server 8080 &

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.so" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf node_modules/ .next/ out/ dist/

deploy:
	@echo "Deploying to production..."
	git push origin main
	@echo "Deployment triggered"

docs:
	@echo "Generating documentation..."
	. $(VENV)/bin/activate && pdoc --html src/python --output-dir docs/api
	@echo "Documentation generated in docs/api/"

lint:
	@echo "Running linting..."
	. $(VENV)/bin/activate && black src/python/
	. $(VENV)/bin/activate && flake8 src/python/
	cd src/react && $(NPM) run lint
	cd src/node && $(NPM) run lint

# Client-specific targets
client-setup:
	@echo "Setting up client repositories..."
	@echo "Run: ./scripts/setup_clients.sh"

client-push:
	@echo "Pushing to client repositories..."
	@echo "Run: ./scripts/push_to_clients.sh"

.PHONY: quantum-simulate
quantum-simulate:
	@echo "Running quantum simulation..."
	. $(VENV)/bin/activate && python src/python/quantum_base.py
