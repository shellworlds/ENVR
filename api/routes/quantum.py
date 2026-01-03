"""
Quantum Computing API Routes
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Dict, Any
import json

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import circuit_drawer
import numpy as np

router = APIRouter()

# Request/Response Models
class QuantumCircuitRequest(BaseModel):
    """Quantum circuit creation request"""
    qubits: int = 2
    gates: List[Dict[str, Any]] = []
    shots: int = 1024

class QuantumJobRequest(BaseModel):
    """Quantum job request"""
    circuit: QuantumCircuitRequest
    backend: str = "qasm_simulator"
    optimization_level: int = 1

class QuantumJobResponse(BaseModel):
    """Quantum job response"""
    job_id: str
    status: str
    results: Dict[str, int]
    circuit_depth: int
    execution_time: float

class GroverSearchRequest(BaseModel):
    """Grover search request"""
    database: List[str]
    target: str
    iterations: int = 1

# Quantum endpoints
@router.post("/circuit/create")
async def create_circuit(request: QuantumCircuitRequest):
    """Create a quantum circuit"""
    try:
        qc = QuantumCircuit(request.qubits, request.qubits)
        
        # Apply gates from request
        for gate in request.gates:
            gate_type = gate.get("type", "").lower()
            qubits = gate.get("qubits", [])
            
            if gate_type == "h":
                qc.h(qubits[0])
            elif gate_type == "x":
                qc.x(qubits[0])
            elif gate_type == "cx":
                qc.cx(qubits[0], qubits[1])
            elif gate_type == "cz":
                qc.cz(qubits[0], qubits[1])
        
        qc.measure_all()
        
        # Draw circuit as ASCII
        circuit_diagram = circuit_drawer(qc, output='text')
        
        return {
            "circuit": str(qc),
            "diagram": circuit_diagram,
            "qubits": request.qubits,
            "depth": qc.depth()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Circuit creation failed: {str(e)}"
        )

@router.post("/execute")
async def execute_circuit(request: QuantumJobRequest):
    """Execute quantum circuit"""
    try:
        # Create circuit from request
        qc = QuantumCircuit(request.circuit.qubits)
        
        # Apply gates
        for gate in request.circuit.gates:
            gate_type = gate.get("type", "").lower()
            qubits = gate.get("qubits", [])
            
            if gate_type == "h":
                qc.h(qubits[0])
            elif gate_type == "x":
                qc.x(qubits[0])
            elif gate_type == "cx":
                qc.cx(qubits[0], qubits[1])
        
        qc.measure_all()
        
        # Execute
        backend = Aer.get_backend(request.backend)
        job = execute(qc, backend, shots=request.circuit.shots)
        result = job.result()
        counts = result.get_counts()
        
        return QuantumJobResponse(
            job_id="job_" + str(hash(str(counts))),
            status="completed",
            results=counts,
            circuit_depth=qc.depth(),
            execution_time=0.1  # Simulated
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Execution failed: {str(e)}"
        )

@router.post("/grover/search")
async def grover_search(request: GroverSearchRequest):
    """Perform Grover search"""
    try:
        if request.target not in request.database:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Target not in database"
            )
        
        # Simplified Grover implementation
        n = len(request.database)
        num_qubits = int(np.ceil(np.log2(n)))
        
        qc = QuantumCircuit(num_qubits, num_qubits)
        qc.h(range(num_qubits))
        
        # Simplified oracle and diffuser
        for _ in range(request.iterations):
            # Mark target (simplified)
            target_idx = request.database.index(request.target)
            binary = format(target_idx, f'0{num_qubits}b')
            
            for i, bit in enumerate(binary):
                if bit == '0':
                    qc.x(i)
            
            if num_qubits == 1:
                qc.z(0)
            elif num_qubits >= 2:
                qc.cz(0, 1)
            
            for i, bit in enumerate(binary):
                if bit == '0':
                    qc.x(i)
            
            # Diffuser
            qc.h(range(num_qubits))
            qc.x(range(num_qubits))
            if num_qubits >= 2:
                qc.cz(0, 1)
            qc.x(range(num_qubits))
            qc.h(range(num_qubits))
        
        qc.measure(range(num_qubits), range(num_qubits))
        
        # Execute
        backend = Aer.get_backend('qasm_simulator')
        result = execute(qc, backend, shots=1024).result()
        counts = result.get_counts()
        
        return {
            "database": request.database,
            "target": request.target,
            "results": counts,
            "circuit_qubits": num_qubits,
            "iterations": request.iterations
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Grover search failed: {str(e)}"
        )

@router.get("/backends")
async def get_available_backends():
    """Get available quantum backends"""
    backends = Aer.backends()
    return {
        "backends": [str(backend) for backend in backends],
        "default": "qasm_simulator"
    }

@router.get("/demo/bell-state")
async def bell_state_demo():
    """Generate and measure Bell state"""
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=1024).result()
    counts = result.get_counts()
    
    return {
        "circuit": str(qc),
        "results": counts,
        "entangled": True,
        "description": "Bell state (EPR pair) demonstration"
    }
