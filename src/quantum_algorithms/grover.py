"""
Grover's Search Algorithm Implementation
"""
from qiskit import QuantumCircuit, Aer, execute
from qiskit.quantum_info import Statevector
import numpy as np

class GroverSearch:
    """Implementation of Grover's search algorithm"""
    
    def __init__(self, database):
        """
        Initialize Grover search
        
        Args:
            database: List of items to search through
        """
        self.database = database
        self.n = len(database)
        self.num_qubits = int(np.ceil(np.log2(self.n)))
        
    def create_oracle(self, target):
        """
        Create oracle for the target state
        
        Args:
            target: Target state to mark
            
        Returns:
            QuantumCircuit: Oracle circuit
        """
        qc = QuantumCircuit(self.num_qubits, name="Oracle")
        
        # Mark the target state (simplified version)
        # In real implementation, this would mark the target state
        if target in self.database:
            target_idx = self.database.index(target)
            # Apply X gates to create binary representation
            for i, bit in enumerate(format(target_idx, f'0{self.num_qubits}b')):
                if bit == '0':
                    qc.x(i)
            
            # Apply multi-controlled Z gate
            if self.num_qubits == 1:
                qc.z(0)
            elif self.num_qubits == 2:
                qc.cz(0, 1)
            
            # Uncompute X gates
            for i, bit in enumerate(format(target_idx, f'0{self.num_qubits}b')):
                if bit == '0':
                    qc.x(i)
        
        return qc
    
    def create_diffuser(self):
        """
        Create diffuser operator for amplitude amplification
        
        Returns:
            QuantumCircuit: Diffuser circuit
        """
        qc = QuantumCircuit(self.num_qubits, name="Diffuser")
        
        # Apply H gates to all qubits
        qc.h(range(self.num_qubits))
        
        # Apply X gates to all qubits
        qc.x(range(self.num_qubits))
        
        # Apply multi-controlled Z gate
        if self.num_qubits == 1:
            qc.z(0)
        elif self.num_qubits == 2:
            qc.h(1)
            qc.cx(0, 1)
            qc.h(1)
        
        # Apply X gates to all qubits
        qc.x(range(self.num_qubits))
        
        # Apply H gates to all qubits
        qc.h(range(self.num_qubits))
        
        return qc
    
    def search(self, target, iterations=1):
        """
        Perform Grover search for target
        
        Args:
            target: Item to search for
            iterations: Number of Grover iterations
            
        Returns:
            dict: Measurement results
        """
        if target not in self.database:
            return {"error": "Target not in database"}
        
        # Create quantum circuit
        qc = QuantumCircuit(self.num_qubits, self.num_qubits)
        
        # Initialize superposition
        qc.h(range(self.num_qubits))
        
        # Apply Grover iterations
        for _ in range(iterations):
            # Add oracle
            oracle = self.create_oracle(target)
            qc.append(oracle, range(self.num_qubits))
            
            # Add diffuser
            diffuser = self.create_diffuser()
            qc.append(diffuser, range(self.num_qubits))
        
        # Measure
        qc.measure(range(self.num_qubits), range(self.num_qubits))
        
        # Simulate
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1024).result()
        
        return result.get_counts(qc)
    
    def visualize_circuit(self, target):
        """
        Create and return circuit for visualization
        
        Args:
            target: Target to search for
            
        Returns:
            QuantumCircuit: Circuit for visualization
        """
        qc = QuantumCircuit(self.num_qubits, self.num_qubits)
        qc.h(range(self.num_qubits))
        oracle = self.create_oracle(target)
        qc.append(oracle, range(self.num_qubits))
        diffuser = self.create_diffuser()
        qc.append(diffuser, range(self.num_qubits))
        qc.measure(range(self.num_qubits), range(self.num_qubits))
        return qc

def demo_grover():
    """Demo function for Grover's algorithm"""
    print("=== Grover's Search Algorithm Demo ===")
    
    # Simple database
    database = ["00", "01", "10", "11"]
    target = "10"
    
    print(f"Database: {database}")
    print(f"Searching for: {target}")
    
    # Create Grover search instance
    grover = GroverSearch(database)
    
    # Perform search
    results = grover.search(target)
    
    print(f"\nSearch results:")
    for state, count in results.items():
        probability = count / 1024 * 100
        print(f"  State {state}: {count} shots ({probability:.1f}%)")
    
    # Get circuit for visualization
    circuit = grover.visualize_circuit(target)
    print(f"\nCircuit depth: {circuit.depth()}")
    print(f"Number of gates: {sum(circuit.count_ops().values())}")
    
    return results

if __name__ == "__main__":
    demo_grover()
