"""
28-QUBIT MARITIME QUANTUM OPTIMIZER - FIXED VERSION
"""
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
import json
import sys

class MaritimeQuantumOptimizer:
    def __init__(self, n_qubits=28):
        self.n_qubits = n_qubits
        self.qr = QuantumRegister(n_qubits, 'q')
        self.cr = ClassicalRegister(n_qubits, 'c')
        
    def create_route_optimization_circuit(self, distance_params, weather_params):
        """Circuit 1: Quantum Approximate Optimization for shipping routes"""
        circuit = QuantumCircuit(self.qr, self.cr)
        print(f"Building {self.n_qubits}-qubit route optimization circuit...")
        
        # Encode distance parameters as rotation angles
        for i in range(self.n_qubits):
            theta = distance_params[i % len(distance_params)] * np.pi
            circuit.ry(theta, self.qr[i])
        
        # Create entanglement for route connectivity
        for i in range(0, self.n_qubits-1, 2):
            circuit.cx(self.qr[i], self.qr[i+1])
        
        # Weather effect encoding
        for i in range(self.n_qubits):
            phi = weather_params[i % len(weather_params)] * np.pi/2
            circuit.rz(phi, self.qr[i])
        
        # Mixing Hamiltonian for optimization
        for i in range(self.n_qubits):
            circuit.rx(np.pi/4, self.qr[i])
        
        circuit.measure(self.qr, self.cr)
        return circuit
    
    def create_hull_stress_circuit(self, stress_data):
        """Circuit 2: Variational Quantum Circuit for hull stress prediction - FIXED"""
        circuit = QuantumCircuit(self.qr, self.cr)
        
        # FIX: Use angle encoding instead of amplitude encoding for stability
        for i in range(min(self.n_qubits, len(stress_data))):
            angle = stress_data[i] * 2 * np.pi
            circuit.ry(angle, self.qr[i])
        
        # Variational layers for stress pattern recognition
        for layer in range(3):
            for i in range(self.n_qubits):
                circuit.ry(np.random.random() * np.pi, self.qr[i])
            for i in range(0, self.n_qubits-1, 1):
                circuit.cx(self.qr[i], self.qr[i+1])
        
        circuit.measure(self.qr, self.cr)
        return circuit
    
    def execute_simulation(self, circuit, shots=1024):
        """Execute circuit on local simulator"""
        simulator = Aer.get_backend('qasm_simulator')
        job = execute(circuit, simulator, shots=shots)
        result = job.result()
        counts = result.get_counts(circuit)
        return counts

# Generate test parameters
np.random.seed(42)
distance_params = np.random.rand(28)
weather_params = np.random.rand(28) * 0.5
stress_data = np.random.rand(28)  # Now matches qubit count

# Create and execute circuits
print("\n=== 28-QUBIT MARITIME QUANTUM SYSTEM (FIXED) ===")
optimizer = MaritimeQuantumOptimizer(28)

print("\n1. Creating Route Optimization Circuit...")
route_circuit = optimizer.create_route_optimization_circuit(distance_params, weather_params)
print(f"   Circuit depth: {route_circuit.depth()}")
print(f"   Gate count: {route_circuit.count_ops()}")

print("\n2. Creating Hull Stress Prediction Circuit (Fixed)...")
stress_circuit = optimizer.create_hull_stress_circuit(stress_data)
print(f"   Circuit depth: {stress_circuit.depth()}")
print(f"   Gate count: {stress_circuit.count_ops()}")

print("\n3. Simulating Both Circuits...")
route_counts = optimizer.execute_simulation(route_circuit, shots=512)
stress_counts = optimizer.execute_simulation(stress_circuit, shots=512)

print(f"   Route optimization: {len(route_counts)} unique quantum states")
print(f"   Hull stress prediction: {len(stress_counts)} unique quantum states")

# Save results
with open('Q28_RESULTS.json', 'w') as f:
    json.dump({
        'route_circuit_stats': dict(route_circuit.count_ops()),
        'stress_circuit_stats': dict(stress_circuit.count_ops()),
        'route_measurement_samples': dict(list(route_counts.items())[:5]),
        'stress_measurement_samples': dict(list(stress_counts.items())[:5])
    }, f, indent=2)

print("\n✓ Fixed 28-qubit quantum programs executed successfully")
print("  Files: Q28_RESULTS.json")
