# ENVR Quantum Computing API Documentation

## Overview
REST API for quantum computing operations built with FastAPI.

## Base URL

## Authentication
Most endpoints require JWT authentication.

### Get Access Token
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
POST /quantum/circuit/create
{
  "qubits": 2,
  "gates": [
    {"type": "h", "qubits": [0]},
    {"type": "cx", "qubits": [0, 1]}
  ],
  "shots": 1024
}

POST /quantum/grover/search
{
  "database": ["00", "01", "10", "11"],
  "target": "10",
  "iterations": 1
}
GET /quantum/backends
User Management
Get Users
bash
GET /users/
Get User Profile
bash
GET /users/{username}
Job Management
Submit Job
bash
POST /jobs/submit?circuit_name=bell_state&backend=qasm_simulator
Get Jobs
bash
GET /jobs/
Health Check
bash
GET /health
Running the API
bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
Testing
bash
cd api
pytest
