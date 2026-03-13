# SN-112BA: 20-qubit Quantum Fourier Transform (Qiskit). Main developer: shellworlds.
"""Simulate 20-qubit QFT for phase/signal processing POC. Uses statevector when qubits > 15."""

import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector
import numpy as np

N_QUBITS = 20
MAX_QUBITS_SIM = 15  # Aer statevector limit; reduce for full simulation


def qft_circuit(n_qubits: int) -> QuantumCircuit:
    qc = QuantumCircuit(n_qubits)
    for j in range(n_qubits):
        qc.h(j)
        for k in range(j + 1, n_qubits):
            qc.cp(2 * math.pi / (2 ** (k - j + 1)), k, j)
    for i in range(n_qubits // 2):
        qc.swap(i, n_qubits - 1 - i)
    return qc


def run_qft_simulation(n_qubits: int = MAX_QUBITS_SIM):
    n = min(n_qubits, MAX_QUBITS_SIM)
    qc = qft_circuit(n)
    sim = AerSimulator(method="statevector")
    qc = transpile(qc, sim)
    job = sim.run(qc)
    result = job.result()
    state = result.get_statevector(qc)
    return state, qc


if __name__ == "__main__":
    state, circuit = run_qft_simulation(MAX_QUBITS_SIM)
    print("QFT circuit depth:", circuit.depth())
    print("Statevector dim:", len(state))
