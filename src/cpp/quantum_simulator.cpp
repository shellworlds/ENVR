/*
 * Quantum JV Platform - C++ Quantum Simulator
 * High-performance quantum circuit simulation
 */

#include <iostream>
#include <vector>
#include <complex>
#include <cmath>
#include <random>

using namespace std;
using Complex = complex<double>;

class QuantumSimulator {
private:
    int num_qubits;
    vector<Complex> state_vector;
    mt19937 rng;
    
public:
    QuantumSimulator(int n) : num_qubits(n), rng(random_device{}()) {
        // Initialize to |0...0⟩ state
        int dim = 1 << n;
        state_vector.resize(dim, Complex(0.0, 0.0));
        state_vector[0] = Complex(1.0, 0.0);
    }
    
    // Apply Hadamard gate to qubit q
    void applyH(int q) {
        int stride = 1 << q;
        int block_size = stride;
        
        for (int i = 0; i < (1 << num_qubits); i += 2 * stride) {
            for (int j = 0; j < block_size; ++j) {
                int idx0 = i + j;
                int idx1 = i + j + stride;
                
                Complex a = state_vector[idx0];
                Complex b = state_vector[idx1];
                
                state_vector[idx0] = (a + b) / sqrt(2.0);
                state_vector[idx1] = (a - b) / sqrt(2.0);
            }
        }
    }
    
    // Apply Pauli-X gate (NOT gate) to qubit q
    void applyX(int q) {
        int stride = 1 << q;
        
        for (int i = 0; i < (1 << num_qubits); i += 2 * stride) {
            for (int j = 0; j < stride; ++j) {
                swap(state_vector[i + j], state_vector[i + j + stride]);
            }
        }
    }
    
    // Apply CNOT gate (control c, target t)
    void applyCNOT(int c, int t) {
        int control_mask = 1 << c;
        int target_mask = 1 << t;
        
        for (int i = 0; i < (1 << num_qubits); ++i) {
            if (i & control_mask) {
                int target_bit = (i & target_mask) ? 1 : 0;
                if (target_bit == 0) {
                    int j = i ^ target_mask;
                    swap(state_vector[i], state_vector[j]);
                }
            }
        }
    }
    
    // Apply rotation Y gate
    void applyRY(int q, double theta) {
        int stride = 1 << q;
        double cos_theta = cos(theta / 2.0);
        double sin_theta = sin(theta / 2.0);
        
        for (int i = 0; i < (1 << num_qubits); i += 2 * stride) {
            for (int j = 0; j < stride; ++j) {
                int idx0 = i + j;
                int idx1 = i + j + stride;
                
                Complex a = state_vector[idx0];
                Complex b = state_vector[idx1];
                
                state_vector[idx0] = cos_theta * a - sin_theta * b;
                state_vector[idx1] = sin_theta * a + cos_theta * b;
            }
        }
    }
    
    // Measure qubit q
    int measure(int q) {
        double prob0 = 0.0;
        int mask = 1 << q;
        
        for (int i = 0; i < (1 << num_qubits); ++i) {
            if ((i & mask) == 0) {
                prob0 += norm(state_vector[i]);
            }
        }
        
        uniform_real_distribution<double> dist(0.0, 1.0);
        double r = dist(rng);
        
        if (r < prob0) {
            // Project onto |0⟩
            for (int i = 0; i < (1 << num_qubits); ++i) {
                if (i & mask) {
                    state_vector[i] = Complex(0.0, 0.0);
                } else {
                    state_vector[i] /= sqrt(prob0);
                }
            }
            return 0;
        } else {
            // Project onto |1⟩
            double prob1 = 1.0 - prob0;
            for (int i = 0; i < (1 << num_qubits); ++i) {
                if (i & mask) {
                    state_vector[i] /= sqrt(prob1);
                } else {
                    state_vector[i] = Complex(0.0, 0.0);
                }
            }
            return 1;
        }
    }
    
    // Create Bell state
    void createBellState() {
        applyH(0);
        applyCNOT(0, 1);
    }
    
    // Get probability distribution
    vector<double> getProbabilities() {
        vector<double> probs(1 << num_qubits);
        for (int i = 0; i < (1 << num_qubits); ++i) {
            probs[i] = norm(state_vector[i]);
        }
        return probs;
    }
    
    // Print state information
    void printState() {
        cout << "Quantum State (n=" << num_qubits << "):" << endl;
        for (int i = 0; i < (1 << num_qubits); ++i) {
            if (abs(state_vector[i]) > 1e-10) {
                cout << "|" << bitset<8>(i).to_string().substr(8 - num_qubits) 
                     << "⟩: " << state_vector[i] 
                     << " (prob: " << norm(state_vector[i]) << ")" << endl;
            }
        }
    }
};

int main() {
    cout << "=== C++ Quantum Simulator ===" << endl;
    
    // Create 2-qubit simulator
    QuantumSimulator sim(2);
    
    // Create Bell state
    cout << "\nCreating Bell state:" << endl;
    sim.createBellState();
    sim.printState();
    
    // Measure first qubit
    cout << "\nMeasuring first qubit:" << endl;
    int result = sim.measure(0);
    cout << "Result: " << result << endl;
    sim.printState();
    
    // Get probabilities
    cout << "\nProbability distribution:" << endl;
    vector<double> probs = sim.getProbabilities();
    for (int i = 0; i < probs.size(); ++i) {
        if (probs[i] > 1e-10) {
            cout << "P(|" << bitset<8>(i).to_string().substr(8 - 2) 
                 << "⟩) = " << probs[i] << endl;
        }
    }
    
    return 0;
}
