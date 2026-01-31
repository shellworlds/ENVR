/*
Quantum JV Platform - Go Quantum API
REST API server for quantum operations in Go
*/

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
	"math/cmplx"
	"math/rand"
	"net/http"
	"strconv"
	"sync"
	"time"
)

// QuantumState represents a quantum state vector
type QuantumState struct {
	Qubits   int
	State    []complex128
	mu       sync.RWMutex
}

// QuantumCircuit represents a quantum circuit
type QuantumCircuit struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Qubits    int       `json:"qubits"`
	Gates     []Gate    `json:"gates"`
	CreatedAt time.Time `json:"created_at"`
}

// Gate represents a quantum gate
type Gate struct {
	Type     string    `json:"type"`
	Qubit    int       `json:"qubit"`
	Target   int       `json:"target,omitempty"`
	Angle    float64   `json:"angle,omitempty"`
}

// NewQuantumState creates a new quantum state
func NewQuantumState(qubits int) *QuantumState {
	dim := 1 << qubits
	state := make([]complex128, dim)
	state[0] = complex(1, 0) // Initialize to |0...0⟩
	
	return &QuantumState{
		Qubits: qubits,
		State:  state,
	}
}

// ApplyHadamard applies Hadamard gate to a qubit
func (qs *QuantumState) ApplyHadamard(qubit int) {
	qs.mu.Lock()
	defer qs.mu.Unlock()
	
	stride := 1 << qubit
	root2 := 1.0 / math.Sqrt(2.0)
	
	for i := 0; i < len(qs.State); i += 2 * stride {
		for j := 0; j < stride; j++ {
			idx0 := i + j
			idx1 := i + j + stride
			
			a := qs.State[idx0]
			b := qs.State[idx1]
			
			qs.State[idx0] = complex(root2, 0) * (a + b)
			qs.State[idx1] = complex(root2, 0) * (a - b)
		}
	}
}

// ApplyCNOT applies CNOT gate
func (qs *QuantumState) ApplyCNOT(control, target int) {
	qs.mu.Lock()
	defer qs.mu.Unlock()
	
	controlMask := 1 << control
	targetMask := 1 << target
	
	for i := 0; i < len(qs.State); i++ {
		if (i & controlMask) != 0 {
			if (i & targetMask) == 0 {
				j := i ^ targetMask
				qs.State[i], qs.State[j] = qs.State[j], qs.State[i]
			}
		}
	}
}

// Measure measures a qubit
func (qs *QuantumState) Measure(qubit int) int {
	qs.mu.Lock()
	defer qs.mu.Unlock()
	
	mask := 1 << qubit
	prob0 := 0.0
	
	// Calculate probability of |0⟩
	for i := 0; i < len(qs.State); i++ {
		if (i & mask) == 0 {
			prob0 += cmplx.Abs(qs.State[i]) * cmplx.Abs(qs.State[i])
		}
	}
	
	// Generate random number
	rand.Seed(time.Now().UnixNano())
	r := rand.Float64()
	
	if r < prob0 {
		// Collapse to |0⟩
		scale := 1.0 / math.Sqrt(prob0)
		for i := 0; i < len(qs.State); i++ {
			if (i & mask) == 0 {
				qs.State[i] *= complex(scale, 0)
			} else {
				qs.State[i] = complex(0, 0)
			}
		}
		return 0
	} else {
		// Collapse to |1⟩
		prob1 := 1.0 - prob0
		scale := 1.0 / math.Sqrt(prob1)
		for i := 0; i < len(qs.State); i++ {
			if (i & mask) != 0 {
				qs.State[i] *= complex(scale, 0)
			} else {
				qs.State[i] = complex(0, 0)
			}
		}
		return 1
	}
}

// GetProbabilities returns probability distribution
func (qs *QuantumState) GetProbabilities() []float64 {
	qs.mu.RLock()
	defer qs.mu.RUnlock()
	
	probs := make([]float64, len(qs.State))
	for i, amp := range qs.State {
		probs[i] = cmplx.Abs(amp) * cmplx.Abs(amp)
	}
	return probs
}

// CreateBellState creates a Bell state
func (qs *QuantumState) CreateBellState() {
	qs.ApplyHadamard(0)
	qs.ApplyCNOT(0, 1)
}

// HTTP Handlers
func healthHandler(w http.ResponseWriter, r *http.Request) {
	response := map[string]interface{}{
		"status":    "healthy",
		"service":   "Quantum Go API",
		"timestamp": time.Now().UTC(),
		"version":   "1.0.0",
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func bellStateHandler(w http.ResponseWriter, r *http.Request) {
	qs := NewQuantumState(2)
	qs.CreateBellState()
	
	response := map[string]interface{}{
		"state":        "Bell state created",
		"probabilities": qs.GetProbabilities(),
		"measurement_0": qs.Measure(0),
		"measurement_1": qs.Measure(1),
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func quantumSimHandler(w http.ResponseWriter, r *http.Request) {
	qubitsStr := r.URL.Query().Get("qubits")
	qubits, err := strconv.Atoi(qubitsStr)
	if err != nil || qubits < 1 || qubits > 5 {
		qubits = 2
	}
	
	qs := NewQuantumState(qubits)
	
	// Apply some gates based on query parameters
	gates := r.URL.Query().Get("gates")
	if gates != "" {
		// Simple gate application logic
		for i := 0; i < qubits; i++ {
			qs.ApplyHadamard(i)
		}
	}
	
	response := map[string]interface{}{
		"qubits":        qubits,
		"state_vector":  qs.State,
		"probabilities": qs.GetProbabilities(),
		"entanglement":  "simulated",
	}
	
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	// Register HTTP handlers
	http.HandleFunc("/api/quantum/health", healthHandler)
	http.HandleFunc("/api/quantum/bell", bellStateHandler)
	http.HandleFunc("/api/quantum/simulate", quantumSimHandler)
	
	// Serve static files
	fs := http.FileServer(http.Dir("./static"))
	http.Handle("/", fs)
	
	// Start server
	port := ":8080"
	fmt.Printf("Quantum Go API server starting on port %s\n", port)
	fmt.Printf("Endpoints:\n")
	fmt.Printf("  GET /api/quantum/health - Health check\n")
	fmt.Printf("  GET /api/quantum/bell - Create Bell state\n")
	fmt.Printf("  GET /api/quantum/simulate?qubits=N - Quantum simulation\n")
	
	log.Fatal(http.ListenAndServe(port, nil))
}
