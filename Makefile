.PHONY: check install-backend install-frontend build run

check:
	./scripts/system_check.sh

install-backend:
	pip install fastapi uvicorn qcodes numpy

install-frontend:
	npm install

build:
	cargo build --manifest-path src/backend/Cargo.toml 2>/dev/null || echo "Rust build skipped"
	npm run build

run-backend:
	uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	npm run dev
