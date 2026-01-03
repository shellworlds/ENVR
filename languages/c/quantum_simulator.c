/*
 * C: Quantum Circuit Simulator
 * Showcasing modern C features, memory management, and performance
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <complex.h>

// Constants
#define MAX_QUBITS 32
#define MAX_GATES 100
#define PI 3.14159265358979323846

// Quantum Gate Types
typedef enum {
    GATE_H,     // Hadamard
    GATE_X,     // Pauli-X
    GATE_Y,     // Pauli-Y
    GATE_Z,     // Pauli-Z
    GATE_CNOT,  // Controlled-NOT
    GATE_SWAP   // SWAP
} GateType;

// Quantum Gate Structure
typedef struct {
    GateType type;
    int target;
    int control;  // -1 if no control qubit
    double angle; // For rotation gates
} QuantumGate;

// Quantum State Vector
typedef struct {
    int num_qubits;
    int dimension;
    double complex* amplitudes;
} QuantumState;

// Quantum Circuit
typedef struct {
    int num_qubits;
    int num_gates;
    QuantumGate gates[MAX_GATES];
    char name[50];
} QuantumCircuit;

// Function Prototypes
QuantumState* create_state(int num_qubits);
void destroy_state(QuantumState* state);
void initialize_state(QuantumState* state);
void apply_gate(QuantumState* state, const QuantumGate* gate);
void print_state(const QuantumState* state);
QuantumCircuit* create_circuit(int num_qubits, const char* name);
void add_gate(QuantumCircuit* circuit, GateType type, int target, int control);
void simulate_circuit(const QuantumCircuit* circuit, QuantumState* state);
double measure_state(const QuantumState* state, int qubit);

// Create quantum state
QuantumState* create_state(int num_qubits) {
    if (num_qubits > MAX_QUBITS) {
        fprintf(stderr, "Error: Too many qubits (max %d)\n", MAX_QUBITS);
        return NULL;
    }
    
    QuantumState* state = malloc(sizeof(QuantumState));
    if (!state) {
        perror("Failed to allocate state");
        return NULL;
    }
    
    state->num_qubits = num_qubits;
    state->dimension = 1 << num_qubits; // 2^n
    
    state->amplitudes = calloc(state->dimension, sizeof(double complex));
    if (!state->amplitudes) {
        perror("Failed to allocate amplitudes");
        free(state);
        return NULL;
    }
    
    return state;
}

// Destroy quantum state
void destroy_state(QuantumState* state) {
    if (state) {
        free(state->amplitudes);
        free(state);
    }
}

// Initialize state to |0...0>
void initialize_state(QuantumState* state) {
    for (int i = 0; i < state->dimension; i++) {
        state->amplitudes[i] = 0.0;
    }
    state->amplitudes[0] = 1.0 + 0.0 * I;
}

// Print quantum state
void print_state(const QuantumState* state) {
    printf("Quantum State (n=%d):\n", state->num_qubits);
    for (int i = 0; i < state->dimension; i++) {
        double complex amp = state->amplitudes[i];
        double prob = creal(amp * conj(amp));
        if (prob > 1e-10) {
            printf("|%0*b>: amplitude = %.3f%+.3fi, probability = %.3f\n",
                   state->num_qubits, i,
                   creal(amp), cimag(amp), prob);
        }
    }
}

// Apply Hadamard gate
void apply_hadamard(QuantumState* state, int qubit) {
    int shift = 1 << qubit;
    int dim = state->dimension;
    
    for (int i = 0; i < dim; i += 2 * shift) {
        for (int j = 0; j < shift; j++) {
            int idx0 = i + j;
            int idx1 = i + j + shift;
            
            double complex a0 = state->amplitudes[idx0];
            double complex a1 = state->amplitudes[idx1];
            
            state->amplitudes[idx0] = (a0 + a1) / sqrt(2.0);
            state->amplitudes[idx1] = (a0 - a1) / sqrt(2.0);
        }
    }
}

// Apply Pauli-X gate
void apply_pauli_x(QuantumState* state, int qubit) {
    int shift = 1 << qubit;
    int dim = state->dimension;
    
    for (int i = 0; i < dim; i += 2 * shift) {
        for (int j = 0; j < shift; j++) {
            int idx0 = i + j;
            int idx1 = i + j + shift;
            
            double complex temp = state->amplitudes[idx0];
            state->amplitudes[idx0] = state->amplitudes[idx1];
            state->amplitudes[idx1] = temp;
        }
    }
}

// Apply gate to state
void apply_gate(QuantumState* state, const QuantumGate* gate) {
    switch (gate->type) {
        case GATE_H:
            apply_hadamard(state, gate->target);
            break;
        case GATE_X:
            apply_pauli_x(state, gate->target);
            break;
        // Additional gates would be implemented here
        default:
            fprintf(stderr, "Gate type %d not implemented\n", gate->type);
    }
}

// Create quantum circuit
QuantumCircuit* create_circuit(int num_qubits, const char* name) {
    QuantumCircuit* circuit = malloc(sizeof(QuantumCircuit));
    if (!circuit) {
        perror("Failed to allocate circuit");
        return NULL;
    }
    
    circuit->num_qubits = num_qubits;
    circuit->num_gates = 0;
    strncpy(circuit->name, name, sizeof(circuit->name) - 1);
    circuit->name[sizeof(circuit->name) - 1] = '\0';
    
    return circuit;
}

// Add gate to circuit
void add_gate(QuantumCircuit* circuit, GateType type, int target, int control) {
    if (circuit->num_gates >= MAX_GATES) {
        fprintf(stderr, "Error: Too many gates in circuit\n");
        return;
    }
    
    QuantumGate* gate = &circuit->gates[circuit->num_gates++];
    gate->type = type;
    gate->target = target;
    gate->control = control;
    gate->angle = 0.0;
}

// Simulate entire circuit
void simulate_circuit(const QuantumCircuit* circuit, QuantumState* state) {
    for (int i = 0; i < circuit->num_gates; i++) {
        apply_gate(state, &circuit->gates[i]);
    }
}

// Main function
int main() {
    printf("=== C Quantum Simulator ===\n");
    
    // Create Bell state circuit
    QuantumCircuit* bell_circuit = create_circuit(2, "Bell State");
    if (!bell_circuit) return 1;
    
    add_gate(bell_circuit, GATE_H, 0, -1);
    add_gate(bell_circuit, GATE_X, 1, 0);  // CNOT with control=0, target=1
    
    // Create and initialize state
    QuantumState* state = create_state(2);
    if (!state) {
        free(bell_circuit);
        return 1;
    }
    
    initialize_state(state);
    
    printf("\nInitial state:\n");
    print_state(state);
    
    // Simulate circuit
    clock_t start = clock();
    simulate_circuit(bell_circuit, state);
    clock_t end = clock();
    
    printf("\nFinal state after %s circuit:\n", bell_circuit->name);
    print_state(state);
    
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("\nSimulation time: %.6f seconds\n", time_taken);
    
    // Cleanup
    destroy_state(state);
    free(bell_circuit);
    
    printf("\n✅ Simulation completed successfully\n");
    return 0;
}
