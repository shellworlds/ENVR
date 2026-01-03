#!/usr/bin/env python3
"""
Quantum Computing Environment - Main Entry Point
Branch: ENVR1
"""
import sys
from src.quantum_algorithms.grover import GroverSearch
from src.quantum_algorithms.shor import ShorAlgorithm
import matplotlib.pyplot as plt

def main():
    """Main function to demonstrate quantum capabilities"""
    print("=" * 60)
    print("Quantum Computing Environment Showcase")
    print(f"Branch: ENVR1")
    print("=" * 60)
    
    # Example: Run Grover's algorithm
    print("\n1. Running Grover's Search Algorithm...")
    try:
        grover = GroverSearch(n_qubits=3, marked_state='101')
        circuit = grover.build_circuit(iterations=1)
        print(f"   Created circuit with {circuit.num_qubits} qubits")
        print(f"   Circuit depth: {circuit.depth()}")
    except ImportError:
        print("   Note: Grover module not fully implemented yet")
    
    # Example: Run Shor's algorithm placeholder
    print("\n2. Shor's Algorithm Setup...")
    try:
        shor = ShorAlgorithm(number=15)
        print(f"   Ready to factor number: {shor.number}")
    except ImportError:
        print("   Note: Shor module not fully implemented yet")
    
    print("\n3. Environment Check:")
    print(f"   Python version: {sys.version}")
    
    print("\n" + "=" * 60)
    print("Quantum Environment Ready!")
    print("=" * 60)

if __name__ == "__main__":
    main()
