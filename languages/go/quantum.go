/*
Go: Quantum Circuit Simulator
Showcasing Go's concurrency, interfaces, and modern features
*/
package main

import (
	"fmt"
	"math"
	"math/rand"
	"sync"
	"time"
)

// GateType represents quantum gate types
type GateType string

const (
	GateHadamard GateType = "H"
	GatePauliX   GateType = "X"
	GatePauliY   GateType = "Y"
	GatePauliZ   GateType = "Z"
	GateCNOT     GateType = "CX"
	GateSWAP     GateType = "SWAP"
)

// QuantumGate represents a quantum gate operation
type QuantumGate struct {
	Type    GateType
	Target  int
	Control *int // Pointer to allow nil
}

// String implements Stringer interface
func (g QuantumGate) String() string {
	if g.Control != nil {
		return fmt.Sprintf("%s(q%d, c%d)", g.Type, g.Target, *g.Control)
	}
	return fmt.Sprintf("%s(q%d)", g.Type, g.Target)
}

// QuantumCircuit represents a quantum circuit
type QuantumCircuit struct {
	Name     string
	Qubits   int
	Gates    []QuantumGate
	Results  map[string]int
	mu       sync.RWMutex // For thread-safe access
}

// NewQuantumCircuit creates a new quantum circuit
func NewQuantumCircuit(name string, qubits int) *QuantumCircuit {
	if qubits <= 0 {
		panic("qubits must be positive")
	}
	return &QuantumCircuit{
		Name:   name,
		Qubits: qubits,
		Gates:  make([]QuantumGate, 0),
		Results: make(map[string]int),
	}
}

// AddGate adds a gate to the circuit (method chaining)
func (qc *QuantumCircuit) AddGate(gate QuantumGate) *QuantumCircuit {
	if gate.Target >= qc.Qubits {
		panic(fmt.Sprintf("target qubit %d out of bounds", gate.Target))
	}
	if gate.Control != nil && *gate.Control >= qc.Qubits {
		panic(fmt.Sprintf("control qubit %d out of bounds", *gate.Control))
	}
	
	qc.mu.Lock()
	defer qc.mu.Unlock()
	qc.Gates = append(qc.Gates, gate)
	return qc
}

// Simulate runs quantum circuit simulation
func (qc *QuantumCircuit) Simulate(shots int) <-chan map[string]int {
	resultChan := make(chan map[string]int, 1)
	
	go func() {
		fmt.Printf("Simulating %s with %d shots...\n", qc.Name, shots)
		time.Sleep(100 * time.Millisecond) // Simulate computation
		
		qc.mu.Lock()
		defer qc.mu.Unlock()
		
		// Generate mock results
		qc.Results = qc.generateResults(shots)
		resultChan <- qc.Results
		close(resultChan)
	}()
	
	return resultChan
}

// generateResults creates mock simulation results
func (qc *QuantumCircuit) generateResults(shots int) map[string]int {
	results := make(map[string]int)
	numStates := 1 << qc.Qubits
	remaining := shots
	
	rand.Seed(time.Now().UnixNano())
	
	for i := 0; i < numStates-1; i++ {
		state := fmt.Sprintf("%0*b", qc.Qubits, i)
		count := rand.Intn(remaining / 2)
		results[state] = count
		remaining -= count
	}
	
	lastState := fmt.Sprintf("%0*b", qc.Qubits, numStates-1)
	results[lastState] = remaining
	
	return results
}

// CalculateEntropy calculates Shannon entropy of results
func (qc *QuantumCircuit) CalculateEntropy() float64 {
	qc.mu.RLock()
	defer qc.mu.RUnlock()
	
	if len(qc.Results) == 0 {
		return 0
	}
	
	total := 0
	for _, count := range qc.Results {
		total += count
	}
	
	entropy := 0.0
	for _, count := range qc.Results {
		probability := float64(count) / float64(total)
		if probability > 0 {
			entropy -= probability * math.Log2(probability)
		}
	}
	
	return entropy
}

// NewBellStateCircuit creates a Bell state circuit (factory function)
func NewBellStateCircuit() *QuantumCircuit {
	control := 0
	circuit := NewQuantumCircuit("Bell State", 2)
	circuit.AddGate(QuantumGate{Type: GateHadamard, Target: 0})
	circuit.AddGate(QuantumGate{Type: GateCNOT, Target: 1, Control: &control})
	return circuit
}

// String implements Stringer interface for circuit
func (qc *QuantumCircuit) String() string {
	qc.mu.RLock()
	defer qc.mu.RUnlock()
	
	return fmt.Sprintf("QuantumCircuit{Name: %s, Qubits: %d, Gates: %d}", 
		qc.Name, qc.Qubits, len(qc.Gates))
}

// CircuitStats holds circuit statistics
type CircuitStats struct {
	Depth     int
	GateCount int
	Width     int
}

// GetStats returns circuit statistics
func (qc *QuantumCircuit) GetStats() CircuitStats {
	qc.mu.RLock()
	defer qc.mu.RUnlock()
	
	return CircuitStats{
		Depth:     len(qc.Gates),
		GateCount: len(qc.Gates),
		Width:     qc.Qubits,
	}
}

// Worker pool for parallel simulation
func simulateMany(circuits []*QuantumCircuit, shots int) []map[string]int {
	var wg sync.WaitGroup
	results := make([]map[string]int, len(circuits))
	
	for i, circuit := range circuits {
		wg.Add(1)
		go func(idx int, c *QuantumCircuit) {
			defer wg.Done()
			results[idx] = <-c.Simulate(shots)
		}(i, circuit)
	}
	
	wg.Wait()
	return results
}

func main() {
	fmt.Println("=== Go Quantum Simulator ===\n")
	
	// Create Bell state circuit
	bellCircuit := NewBellStateCircuit()
	
	// Add additional gates
	bellCircuit.AddGate(QuantumGate{Type: GatePauliX, Target: 1})
	bellCircuit.AddGate(QuantumGate{Type: GatePauliZ, Target: 0})
	
	fmt.Println("Circuit:", bellCircuit)
	
	// Display gates
	fmt.Println("\nGates:")
	for _, gate := range bellCircuit.Gates {
		fmt.Println(" ", gate)
	}
	
	// Run simulation
	results := <-bellCircuit.Simulate(1000)
	
	fmt.Println("\nSimulation Results:")
	for state, count := range results {
		if count > 100 {
			fmt.Printf("  |%s⟩: %d counts\n", state, count)
		}
	}
	
	// Calculate entropy
	entropy := bellCircuit.CalculateEntropy()
	fmt.Printf("\nCircuit Entropy: %.3f bits\n", entropy)
	
	// Get circuit statistics
	stats := bellCircuit.GetStats()
	fmt.Printf("\nCircuit Statistics:\n")
	fmt.Printf("  Depth: %d\n", stats.Depth)
	fmt.Printf("  Gate Count: %d\n", stats.GateCount)
	fmt.Printf("  Width: %d\n", stats.Width)
	
	// Demonstrate concurrency with multiple circuits
	fmt.Println("\n--- Parallel Simulation Demo ---")
	
	circuits := []*QuantumCircuit{
		NewBellStateCircuit(),
		NewQuantumCircuit("Superposition", 1).AddGate(QuantumGate{Type: GateHadamard, Target: 0}),
		NewQuantumCircuit("Entangled 3", 3).
			AddGate(QuantumGate{Type: GateHadamard, Target: 0}).
			AddGate(QuantumGate{Type: GateCNOT, Target: 1, Control: &[]int{0}[0]}).
			AddGate(QuantumGate{Type: GateCNOT, Target: 2, Control: &[]int{1}[0]}),
	}
	
	parallelResults := simulateMany(circuits, 500)
	
	fmt.Println("\nParallel Simulation Results:")
	for i, result := range parallelResults {
		total := 0
		for _, count := range result {
			total += count
		}
		fmt.Printf("  Circuit %d: %d total shots\n", i+1, total)
	}
	
	fmt.Println("\n✅ Go quantum simulation completed!")
}
