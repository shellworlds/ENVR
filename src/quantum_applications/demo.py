"""
Quantum Application Demo
Simple examples to showcase quantum capabilities
"""
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import numpy as np
import matplotlib.pyplot as plt

class QuantumDemo:
    """Collection of quantum computing demonstrations"""
    
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')
        self.statevector_backend = Aer.get_backend('statevector_simulator')
    
    def bell_state_demo(self):
        """Create and measure Bell states"""
        print("Demo 1: Creating Bell States")
        print("-" * 40)
        
        # Create Bell state (|00> + |11>)/√2
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        
        # Execute
        compiled = transpile(qc, self.backend)
        job = self.backend.run(compiled, shots=1024)
        result = job.result()
        counts = result.get_counts()
        
        print(f"Circuit depth: {qc.depth()}")
        print(f"Circuit size: {qc.size()}")
        print(f"Measurement results: {counts}")
        
        return qc, counts
    
    def superposition_demo(self):
        """Demonstrate quantum superposition"""
        print("\nDemo 2: Quantum Superposition")
        print("-" * 40)
        
        qc = QuantumCircuit(1, 1)
        qc.h(0)  # Create superposition
        qc.measure(0, 0)
        
        compiled = transpile(qc, self.backend)
        job = self.backend.run(compiled, shots=1024)
        result = job.result()
        counts = result.get_counts()
        
        print(f"Qubit in superposition |0> + |1>")
        print(f"Measurement distribution: {counts}")
        
        return qc, counts
    
    def entanglement_witness(self):
        """Demonstrate quantum entanglement"""
        print("\nDemo 3: Entanglement Witness")
        print("-" * 40)
        
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        
        # Get statevector
        qc_no_measure = QuantumCircuit(2, 2)
        qc_no_measure.h(0)
        qc_no_measure.cx(0, 1)
        
        statevector_job = self.statevector_backend.run(transpile(qc_no_measure, self.statevector_backend))
        statevector = statevector_job.result().get_statevector()
        
        print(f"Statevector: {statevector}")
        print("Entangled state: (|00> + |11>)/√2")
        
        return qc_no_measure, statevector
    
    def run_all_demos(self):
        """Run all demonstration circuits"""
        print("=" * 60)
        print("QUANTUM COMPUTING DEMONSTRATIONS")
        print("=" * 60)
        
        results = {}
        
        # Run demos
        bell_circuit, bell_counts = self.bell_state_demo()
        results['bell'] = {'circuit': bell_circuit, 'counts': bell_counts}
        
        super_circuit, super_counts = self.superposition_demo()
        results['superposition'] = {'circuit': super_circuit, 'counts': super_counts}
        
        ent_circuit, ent_state = self.entanglement_witness()
        results['entanglement'] = {'circuit': ent_circuit, 'state': ent_state}
        
        print("\n" + "=" * 60)
        print("All demonstrations completed successfully!")
        print("=" * 60)
        
        return results

# Quick test if run directly
if __name__ == "__main__":
    demo = QuantumDemo()
    demo.run_all_demos()
