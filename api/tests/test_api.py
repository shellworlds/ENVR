"""
API Tests
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "ENVR Quantum Computing API" in data["message"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ENVR Quantum API" in data["service"]

def test_quantum_backends():
    """Test quantum backends endpoint"""
    response = client.get("/quantum/backends")
    assert response.status_code == 200
    data = response.json()
    assert "backends" in data
    assert "default" in data

def test_bell_state_demo():
    """Test Bell state demo"""
    response = client.get("/quantum/demo/bell-state")
    assert response.status_code == 200
    data = response.json()
    assert "circuit" in data
    assert "results" in data
    assert "entangled" in data
    assert data["entangled"] is True

def test_create_circuit():
    """Test circuit creation"""
    circuit_data = {
        "qubits": 2,
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "cx", "qubits": [0, 1]}
        ],
        "shots": 1024
    }
    response = client.post("/quantum/circuit/create", json=circuit_data)
    assert response.status_code == 200
    data = response.json()
    assert "circuit" in data
    assert "qubits" in data
    assert data["qubits"] == 2

def test_grover_search():
    """Test Grover search"""
    grover_data = {
        "database": ["00", "01", "10", "11"],
        "target": "10",
        "iterations": 1
    }
    response = client.post("/quantum/grover/search", json=grover_data)
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "target" in data
    assert data["target"] == "10"
