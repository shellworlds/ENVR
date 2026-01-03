"""
Python: Quantum Calculator
Python 3.11 showcase with modern features
"""
import asyncio
import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class GateType(Enum):
    """Quantum gate types"""
    HADAMARD = "h"
    PAULI_X = "x"
    PAULI_Y = "y"
    PAULI_Z = "z"
    CNOT = "cx"

@dataclass
class QuantumGate:
    """Quantum gate representation"""
    type: GateType
    target_qubit: int
    control_qubit: Optional[int] = None
    
    def __str__(self) -> str:
        if self.control_qubit is not None:
            return f"{self.type.value}({self.target_qubit}, control={self.control_qubit})"
        return f"{self.type.value}({self.target_qubit})"

class QuantumCalculator:
    """Quantum calculator using modern Python"""
    def __init__(self, qubits: int = 2):
        self.qubits = qubits
        self.gates: List[QuantumGate] = []
        self.results: Optional[Dict[str, int]] = None
    
    def add_gate(self, gate: QuantumGate) -> 'QuantumCalculator':
        """Add gate with method chaining"""
        self.gates.append(gate)
        return self
    
    async def simulate(self, shots: int = 1024) -> Dict[str, int]:
        """Simulate quantum circuit asynchronously"""
        print(f"Simulating {len(self.gates)} gates with {shots} shots...")
        
        await asyncio.sleep(0.1)  # Simulate computation
        
        # Generate mock results
        self.results = self._generate_results(shots)
        return self.results
    
    def _generate_results(self, shots: int) -> Dict[str, int]:
        """Generate mock quantum results"""
        import random
        results = {}
        num_states = 1 << self.qubits
        remaining = shots
        
        for i in range(num_states - 1):
            state = format(i, f'0{self.qubits}b')
            count = random.randint(0, remaining // 2)
            results[state] = count
            remaining -= count
        
        last_state = format(num_states - 1, f'0{self.qubits}b')
        results[last_state] = remaining
        
        return results
    
    def calculate_entropy(self) -> float:
        """Calculate Shannon entropy of results"""
        if not self.results:
            return 0.0
        
        total = sum(self.results.values())
        entropy = 0.0
        
        for count in self.results.values():
            probability = count / total
            if probability > 0:
                entropy -= probability * np.log2(probability)
        
        return entropy
    
    @classmethod
    def create_bell_state(cls) -> 'QuantumCalculator':
        """Factory method for Bell state circuit"""
        calculator = cls(qubits=2)
        calculator.add_gate(QuantumGate(GateType.HADAMARD, 0))
        calculator.add_gate(QuantumGate(GateType.CNOT, 1, 0))
        return calculator

async def main():
    """Main async function"""
    print("🚀 Python Quantum Calculator")
    print("=" * 40)
    
    # Create Bell state calculator
    bell_calc = QuantumCalculator.create_bell_state()
    
    # Add more gates
    bell_calc.add_gate(QuantumGate(GateType.PAULI_X, 1))
    
    print(f"Circuit: {bell_calc.qubits} qubits, {len(bell_calc.gates)} gates")
    print("\nGates:")
    for gate in bell_calc.gates:
        print(f"  {gate}")
    
    # Execute circuit
    results = await bell_calc.simulate(shots=1000)
    
    print("\nResults (counts > 100):")
    for state, count in results.items():
        if count > 100:
            probability = count / 1000 * 100
            print(f"  |{state}⟩: {count} shots ({probability:.1f}%)")
    
    # Calculate entropy
    entropy = bell_calc.calculate_entropy()
    print(f"\nCircuit Entropy: {entropy:.3f} bits")
    
    # Demonstrate Python features
    print("\n" + "=" * 40)
    print("Python Features Demonstrated:")
    print("  • Async/await for simulations")
    print("  • Type hints and dataclasses")
    print("  • Enum for gate types")
    print("  • Method chaining pattern")
    print("  • Factory method pattern")
    print("  • List comprehensions")
    print("  • f-strings and formatting")

if __name__ == "__main__":
    asyncio.run(main())
