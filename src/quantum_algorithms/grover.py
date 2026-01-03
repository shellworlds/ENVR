"""
Grover's Search Algorithm Implementation
"""
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

class GroverSearch:
    """Implementation of Grover's search algorithm"""
    
    def __init__(self, n_qubits=3, marked_state='101'):
        self.n_qubits = n_qubits
        self.marked_state = marked_state
        self.circuit = QuantumCircuit(n_qubits, n_qubits)
        
    def oracle(self):
        """Create oracle for marked state"""
        oracle_circuit = QuantumCircuit(self.n_qubits, name="Oracle")
        
        # Mark the specific state (example for |101>)
        if self.marked_state == '101':
            oracle_circuit.cz(0, 2)  # Control-Z on qubits 0 and 2
            oracle_circuit.cz(1, 2)  # To unmark |111>
            oracle_circuit.cz(0, 1)  # To unmark |011>
            
        return oracle_circuit
    
    def diffusion_operator(self):
        """Create diffusion operator"""
        diffusion_circuit = QuantumCircuit(self.n_qubits, name="Diffusion")
        
        # Apply H gates
        diffusion_circuit.h(range(self.n_qubits))
        
        # Apply X gates
        diffusion_circuit.x(range(self.n_qubits))
        
        # Apply multi-controlled Z gate
        diffusion_circuit.h(self.n_qubits - 1)
        diffusion_circuit.mcx(list(range(self.n_qubits - 1)), self.n_qubits - 1)
        diffusion_circuit.h(self.n_qubits - 1)
        
        # Apply X gates
        diffusion_circuit.x(range(self.n_qubits))
        
        # Apply H gates
        diffusion_circuit.h(range(self.n_qubits))
        
        return diffusion_circuit
    
    def build_circuit(self, iterations=1):
        """Build complete Grover circuit"""
        # Initialize superposition
        self.circuit.h(range(self.n_qubits))
        
        # Apply Grover iterations
        for _ in range(iterations):
            # Add oracle
            oracle = self.oracle()
            self.circuit.append(oracle, range(self.n_qubits))
            
            # Add diffusion operator
            diffusion = self.diffusion_operator()
            self.circuit.append(diffusion, range(self.n_qubits))
        
        # Measure
        self.circuit.measure(range(self.n_qubits), range(self.n_qubits))
        
        return self.circuit
    
    def run_simulation(self, shots=1024):
        """Run simulation and return results"""
        simulator = Aer.get_backend('qasm_simulator')
        compiled_circuit = transpile(self.circuit, simulator)
        job = simulator.run(compiled_circuit, shots=shots)
        result = job.result()
        counts = result.get_counts()
        
        return counts
    
    def visualize(self, counts):
        """Visualize results"""
        plot_histogram(counts)
        plt.title(f"Grover's Search Results - Marked: |{self.marked_state}>")
        plt.show()
        
    def get_circuit_info(self):
        """Get circuit information"""
        return {
            'qubits': self.n_qubits,
            'marked_state': self.marked_state,
            'depth': self.circuit.depth(),
            'size': self.circuit.size(),
            'operations': self.circuit.count_ops()
        }
