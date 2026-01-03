# ENVR Quantum Computing API

FastAPI-based REST API for quantum computing operations.

## Features
- Quantum circuit creation and execution
- Grover's algorithm implementation
- User authentication (JWT)
- Job management system
- Docker containerization
- Comprehensive testing

## Quick Start

### Local Development
```bash
cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
cd api
docker-compose up
cd api
pytest
API Documentation
Once running, visit:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Endpoints
/quantum/ - Quantum operations

/auth/ - Authentication

/users/ - User management

/jobs/ - Job management

/health - Health check

Environment Variables
Create .env file:

env
DATABASE_URL=postgresql://user:password@localhost/quantum_db
SECRET_KEY=your-secret-key
DEBUG=True
