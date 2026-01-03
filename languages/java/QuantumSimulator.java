/*
 * Java: Quantum Circuit Simulator
 * Showcasing OOP, interfaces, streams, and modern Java features
 */
import java.util.*;
import java.util.stream.*;
import java.util.concurrent.*;

public class QuantumSimulator {
    
    // Enum for gate types
    public enum GateType {
        HADAMARD("H"),
        PAULI_X("X"),
        PAULI_Y("Y"),
        PAULI_Z("Z"),
        CNOT("CX"),
        SWAP("SWAP");
        
        private final String symbol;
        
        GateType(String symbol) {
            this.symbol = symbol;
        }
        
        public String getSymbol() {
            return symbol;
        }
    }
    
    // Record for quantum gate (Java 14+)
    public record QuantumGate(GateType type, int target, Optional<Integer> control) {
        public QuantumGate {
            if (target < 0) {
                throw new IllegalArgumentException("Target qubit cannot be negative");
            }
            control.ifPresent(c -> {
                if (c < 0) throw new IllegalArgumentException("Control qubit cannot be negative");
            });
        }
        
        @Override
        public String toString() {
            return String.format("%s(q%d%s)", 
                type.getSymbol(), 
                target, 
                control.map(c -> ", c" + c).orElse(""));
        }
    }
    
    // Quantum circuit class
    public static class QuantumCircuit {
        private final String name;
        private final int numQubits;
        private final List<QuantumGate> gates;
        private Map<String, Integer> results;
        
        public QuantumCircuit(String name, int numQubits) {
            this.name = name;
            this.numQubits = numQubits;
            this.gates = new ArrayList<>();
            this.results = null;
            
            if (numQubits <= 0) {
                throw new IllegalArgumentException("Number of qubits must be positive");
            }
        }
        
        public QuantumCircuit addGate(QuantumGate gate) {
            if (gate.target() >= numQubits) {
                throw new IllegalArgumentException(
                    String.format("Gate target %d exceeds circuit width %d", 
                    gate.target(), numQubits));
            }
            gate.control().ifPresent(c -> {
                if (c >= numQubits) {
                    throw new IllegalArgumentException(
                        String.format("Control qubit %d exceeds circuit width %d", 
                        c, numQubits));
                }
            });
            
            gates.add(gate);
            return this;
        }
        
        public CompletableFuture<Map<String, Integer>> simulateAsync(int shots) {
            return CompletableFuture.supplyAsync(() -> {
                System.out.printf("Simulating %s with %d shots...%n", name, shots);
                
                try {
                    Thread.sleep(100); // Simulate computation
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException("Simulation interrupted", e);
                }
                
                // Generate mock results
                results = generateResults(shots);
                return results;
            });
        }
        
        private Map<String, Integer> generateResults(int shots) {
            Map<String, Integer> results = new HashMap<>();
            int numStates = 1 << numQubits;
            
            Random random = new Random();
            int remaining = shots;
            
            for (int i = 0; i < numStates - 1; i++) {
                String state = String.format("%" + numQubits + "s", 
                    Integer.toBinaryString(i)).replace(' ', '0');
                int count = random.nextInt(remaining / 2);
                results.put(state, count);
                remaining -= count;
            }
            
            String lastState = String.format("%" + numQubits + "s", 
                Integer.toBinaryString(numStates - 1)).replace(' ', '0');
            results.put(lastState, remaining);
            
            return results;
        }
        
        public double calculateEntropy() {
            if (results == null) {
                throw new IllegalStateException("No simulation results available");
            }
            
            int totalShots = results.values().stream()
                .mapToInt(Integer::intValue)
                .sum();
            
            return results.values().stream()
                .mapToDouble(count -> (double) count / totalShots)
                .filter(probability -> probability > 0)
                .map(probability -> -probability * (Math.log(probability) / Math.log(2)))
                .sum();
        }
        
        // Factory method for Bell state
        public static QuantumCircuit createBellState() {
            QuantumCircuit circuit = new QuantumCircuit("Bell State", 2);
            circuit.addGate(new QuantumGate(GateType.HADAMARD, 0, Optional.empty()))
                   .addGate(new QuantumGate(GateType.CNOT, 1, Optional.of(0)));
            return circuit;
        }
        
        // Getters
        public String getName() { return name; }
        public int getNumQubits() { return numQubits; }
        public List<QuantumGate> getGates() { return Collections.unmodifiableList(gates); }
        public Optional<Map<String, Integer>> getResults() { 
            return Optional.ofNullable(results); 
        }
        
        @Override
        public String toString() {
            return String.format("QuantumCircuit{name='%s', qubits=%d, gates=%d}", 
                name, numQubits, gates.size());
        }
    }
    
    // Main demonstration
    public static void main(String[] args) {
        System.out.println("=== Java Quantum Simulator ===\n");
        
        // Create Bell state circuit
        QuantumCircuit bellCircuit = QuantumCircuit.createBellState();
        
        // Add some gates
        bellCircuit.addGate(new QuantumGate(GateType.PAULI_X, 1, Optional.empty()))
                   .addGate(new QuantumGate(GateType.PAULI_Z, 0, Optional.empty()));
        
        System.out.println("Circuit: " + bellCircuit);
        
        // Use streams to display gates
        System.out.println("\nGates:");
        bellCircuit.getGates().stream()
            .map(QuantumGate::toString)
            .forEach(System.out::println);
        
        // Async simulation
        ExecutorService executor = Executors.newSingleThreadExecutor();
        try {
            CompletableFuture<Map<String, Integer>> simulation = bellCircuit.simulateAsync(1000);
            
            simulation.thenAccept(results -> {
                System.out.println("\nSimulation Results:");
                
                // Use streams to process results
                results.entrySet().stream()
                    .filter(entry -> entry.getValue() > 100)
                    .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                    .forEach(entry -> 
                        System.out.printf("  |%s⟩: %d counts%n", entry.getKey(), entry.getValue()));
                
                // Calculate entropy
                double entropy = bellCircuit.calculateEntropy();
                System.out.printf("%nCircuit Entropy: %.3f bits%n", entropy);
                
                // Additional analysis using streams
                double avgCount = results.values().stream()
                    .mapToInt(Integer::intValue)
                    .average()
                    .orElse(0.0);
                System.out.printf("Average count per state: %.1f%n", avgCount);
                
            }).get(); // Wait for completion
            
        } catch (Exception e) {
            System.err.println("Error during simulation: " + e.getMessage());
            e.printStackTrace();
        } finally {
            executor.shutdown();
        }
        
        // Pattern matching (Java 17+ preview)
        System.out.println("\nCircuit Analysis:");
        analyzeCircuit(bellCircuit);
        
        System.out.println("\n✅ Java quantum simulation completed!");
    }
    
    // Pattern matching demonstration
    private static void analyzeCircuit(QuantumCircuit circuit) {
        // Switch expression
        String complexity = switch (circuit.getNumQubits()) {
            case 1 -> "Trivial";
            case 2 -> "Simple";
            case 3, 4 -> "Medium";
            default -> "Complex";
        };
        
        System.out.printf("Circuit complexity: %s%n", complexity);
        System.out.printf("Number of gates: %d%n", circuit.getGates().size());
        
        // Record pattern matching (Java 19+ preview)
        long cnotGates = circuit.getGates().stream()
            .filter(gate -> gate.type() == GateType.CNOT)
            .count();
        System.out.printf("CNOT gates: %d%n", cnotGates);
    }
}
