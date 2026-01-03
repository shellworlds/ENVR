"""
Quantum Computing Demo Showcase
"""
import json
from datetime import datetime
from qiskit import QuantumCircuit, Aer, execute, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector
import numpy as np

class QuantumDemo:
    """Quantum computing demonstration class"""
    
    def __init__(self):
        self.results = {}
        self.timestamp = datetime.now().isoformat()
    
    def bell_state_demo(self):
        """Create and measure a Bell state"""
        print("Creating Bell state (EPR pair)...")
        
        # Create quantum circuit
        qc = QuantumCircuit(2, 2)
        qc.h(0)  # Hadamard gate on qubit 0
        qc.cx(0, 1)  # CNOT gate
        
        # Add measurements
        qc.measure([0, 1], [0, 1])
        
        # Execute on simulator
        simulator = Aer.get_backend('qasm_simulator')
        compiled_circuit = transpile(qc, simulator)
        job = execute(compiled_circuit, simulator, shots=1024)
        result = job.result()
        counts = result.get_counts(qc)
        
        self.results['bell_state'] = {
            'circuit': str(qc),
            'counts': counts,
            'entangled': True
        }
        
        print(f"Bell state results: {counts}")
        return counts
    
    def superposition_demo(self):
        """Demonstrate quantum superposition"""
        print("Demonstrating quantum superposition...")
        
        qc = QuantumCircuit(1, 1)
        qc.h(0)  # Create superposition
        qc.measure(0, 0)
        
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1024).result()
        counts = result.get_counts()
        
        self.results['superposition'] = {
            'circuit': str(qc),
            'counts': counts,
            'expected': {'0': '~50%', '1': '~50%'}
        }
        
        print(f"Superposition results: {counts}")
        return counts
    
    def quantum_teleportation_demo(self):
        """Simplified quantum teleportation demonstration"""
        print("Quantum teleportation demo (simplified)...")
        
        # Create circuit for quantum teleportation
        qc = QuantumCircuit(3, 3)
        
        # Step 1: Create entanglement
        qc.h(1)
        qc.cx(1, 2)
        
        # Step 2: Prepare state to teleport
        qc.x(0)  # |1> state
        
        # Step 3: Bell measurement
        qc.cx(0, 1)
        qc.h(0)
        
        # Step 4: Measure
        qc.measure([0, 1], [0, 1])
        
        # Step 5: Apply corrections (based on measurement)
        qc.cz(0, 2)
        qc.cx(1, 2)
        
        # Final measurement
        qc.measure(2, 2)
        
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1024).result()
        counts = result.get_counts()
        
        self.results['teleportation'] = {
            'circuit': str(qc),
            'counts': counts,
            'success_rate': counts.get('001', 0) / 1024 * 100
        }
        
        print(f"Teleportation results: {counts}")
        return counts
    
    def run_all_examples(self):
        """Run all quantum demos"""
        print("=" * 60)
        print("QUANTUM COMPUTING DEMONSTRATION")
        print("=" * 60)
        
        self.bell_state_demo()
        print("-" * 40)
        
        self.superposition_demo()
        print("-" * 40)
        
        self.quantum_teleportation_demo()
        print("-" * 40)
        
        # Save results to file
        self.save_results()
        
        print("All demonstrations completed!")
        return self.results
    
    def save_results(self, filename="quantum_results.json"):
        """Save results to JSON file"""
        output = {
            'timestamp': self.timestamp,
            'results': self.results,
            'metadata': {
                'qiskit_version': '1.0.0',
                'backend': 'qasm_simulator',
                'shots': 1024
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Results saved to {filename}")
        return filename

def main():
    """Main function to run quantum demos"""
    demo = QuantumDemo()
    results = demo.run_all_examples()
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for demo_name, data in results.items():
        print(f"\n{demo_name.upper().replace('_', ' ')}:")
        print(f"  Circuit operations: {len(data['circuit'].split('\\n'))}")
        print(f"  Measurement outcomes: {len(data['counts'])}")
        if 'success_rate' in data:
            print(f"  Success rate: {data['success_rate']:.1f}%")
    
    print(f"\nTotal demonstrations: {len(results)}")
    print(f"Timestamp: {demo.timestamp}")

if __name__ == "__main__":
    main()
