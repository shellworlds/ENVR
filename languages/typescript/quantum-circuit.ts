/**
 * TypeScript: Quantum Circuit with Strong Typing
 * Interfaces, generics, decorators, and modern TypeScript features
 */

// Enums for type safety
enum GateType {
    Hadamard = 'H',
    PauliX = 'X',
    PauliY = 'Y',
    PauliZ = 'Z',
    CNOT = 'CX',
    SWAP = 'SWAP'
}

// Interface definitions
interface IQuantumGate {
    type: GateType;
    target: number;
    control?: number;
    angle?: number;
}

interface ISimulationResult {
    [state: string]: number;
    entropy?: number;
    executionTime?: number;
}

interface ICircuitStats {
    depth: number;
    gateCount: number;
    width: number;
}

// Generic type for measurement results
type MeasurementResult<T extends string> = Record<T, number>;

// Decorator for logging
function logExecution(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = function(...args: any[]) {
        console.log(`Executing ${propertyKey} with args:`, args);
        const start = performance.now();
        const result = originalMethod.apply(this, args);
        const end = performance.now();
        console.log(`${propertyKey} executed in ${(end - start).toFixed(2)}ms`);
        return result;
    };
    
    return descriptor;
}

// Abstract base class
abstract class QuantumComponent {
    abstract name: string;
    
    describe(): string {
        return `Quantum Component: ${this.name}`;
    }
}

// Quantum Gate class with generics
class QuantumGate<T extends GateType> implements IQuantumGate {
    constructor(
        public type: T,
        public target: number,
        public control?: number,
        public angle?: number
    ) {
        if (target < 0) {
            throw new Error('Target qubit must be non-negative');
        }
        if (control !== undefined && control < 0) {
            throw new Error('Control qubit must be non-negative');
        }
    }
    
    toString(): string {
        const controlStr = this.control !== undefined ? `, control=${this.control}` : '';
        const angleStr = this.angle !== undefined ? `, angle=${this.angle}` : '';
        return `${this.type}(target=${this.target}${controlStr}${angleStr})`;
    }
    
    // Generic method
    static createGate<T extends GateType>(type: T, target: number, control?: number): QuantumGate<T> {
        return new QuantumGate(type, target, control);
    }
}

// Quantum Circuit with inheritance
class QuantumCircuit extends QuantumComponent {
    private gates: QuantumGate<GateType>[] = [];
    private results: ISimulationResult | null = null;
    
    constructor(
        public name: string,
        private numQubits: number
    ) {
        super();
        if (numQubits <= 0) {
            throw new Error('Number of qubits must be positive');
        }
    }
    
    // Method overloads
    addGate(gate: QuantumGate<GateType>): this;
    addGate(type: GateType, target: number, control?: number): this;
    addGate(param1: GateType | QuantumGate<GateType>, target?: number, control?: number): this {
        if (param1 instanceof QuantumGate) {
            this.validateGate(param1);
            this.gates.push(param1);
        } else if (typeof param1 === 'string' && target !== undefined) {
            const gate = new QuantumGate(param1 as GateType, target, control);
            this.validateGate(gate);
            this.gates.push(gate);
        }
        return this;
    }
    
    private validateGate(gate: QuantumGate<GateType>): void {
        if (gate.target >= this.numQubits) {
            throw new Error(`Gate target ${gate.target} exceeds circuit width ${this.numQubits}`);
        }
        if (gate.control !== undefined && gate.control >= this.numQubits) {
            throw new Error(`Control qubit ${gate.control} exceeds circuit width ${this.numQubits}`);
        }
    }
    
    @logExecution
    async simulate(shots: number = 1024): Promise<ISimulationResult> {
        console.log(`Simulating ${this.name} with ${shots} shots...`);
        
        // Simulate with delay
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Generate mock results
        this.results = this.generateResults(shots);
        this.results.entropy = this.calculateEntropy();
        this.results.executionTime = Math.random() * 100;
        
        return this.results;
    }
    
    private generateResults(shots: number): ISimulationResult {
        const results: ISimulationResult = {};
        const numStates = 1 << this.numQubits;
        
        // Generate random distribution
        let remaining = shots;
        const states = Array.from({length: numStates}, (_, i) => 
            i.toString(2).padStart(this.numQubits, '0')
        );
        
        for (let i = 0; i < states.length - 1; i++) {
            const count = Math.floor(Math.random() * remaining / 2);
            results[states[i]] = count;
            remaining -= count;
        }
        
        results[states[states.length - 1]] = remaining;
        return results;
    }
    
    calculateEntropy(): number {
        if (!this.results) {
            throw new Error('No simulation results available');
        }
        
        const total = Object.values(this.results)
            .filter(v => typeof v === 'number')
            .reduce((sum, count) => sum + count, 0);
        
        let entropy = 0;
        
        for (const [state, count] of Object.entries(this.results)) {
            if (typeof count === 'number' && state !== 'entropy' && state !== 'executionTime') {
                const probability = count / total;
                if (probability > 0) {
                    entropy -= probability * Math.log2(probability);
                }
            }
        }
        
        return entropy;
    }
    
    getStats(): ICircuitStats {
        return {
            depth: this.gates.length,
            gateCount: this.gates.length,
            width: this.numQubits
        };
    }
    
    // Factory method using generic constraints
    static createBellState(): QuantumCircuit {
        const circuit = new QuantumCircuit('Bell State Circuit', 2);
        circuit.addGate(GateType.Hadamard, 0)
               .addGate(GateType.CNOT, 1, 0);
        return circuit;
    }
    
    // Iterator implementation
    *[Symbol.iterator](): IterableIterator<QuantumGate<GateType>> {
        for (const gate of this.gates) {
            yield gate;
        }
    }
}

// Demonstration function
async function demonstrateTypeScriptFeatures(): Promise<void> {
    console.log('=== TypeScript Quantum Features Demo ===\n');
    
    // 1. Create circuit using factory method
    const bellCircuit = QuantumCircuit.createBellState();
    
    // 2. Use tuple type
    const additionalGates: [GateType, number, number?][] = [
        [GateType.PauliX, 1],
        [GateType.PauliZ, 0]
    ];
    
    // 3. Add gates using tuple destructuring
    for (const [type, target, control] of additionalGates) {
        bellCircuit.addGate(type, target, control);
    }
    
    // 4. Display circuit info using template literal types
    console.log(`Circuit: ${bellCircuit.describe()}`);
    
    // 5. Get statistics using interface
    const stats = bellCircuit.getStats();
    console.log(`Circuit Stats:`, stats);
    
    // 6. Run simulation
    try {
        const results = await bellCircuit.simulate(1000);
        
        // 7. Type guard
        const isCompleteResult = (result: any): result is ISimulationResult => {
            return result && typeof result === 'object' && 'entropy' in result;
        };
        
        if (isCompleteResult(results)) {
            console.log(`\nSimulation Results:`);
            console.log(`Entropy: ${results.entropy!.toFixed(3)} bits`);
            console.log(`Execution Time: ${results.executionTime!.toFixed(2)} ms`);
            
            // 8. Filter and map with type safety
            const significantResults = Object.entries(results)
                .filter(([key, value]) => 
                    !['entropy', 'executionTime'].includes(key) && 
                    typeof value === 'number' && 
                    value > 100
                )
                .map(([state, count]) => ({ state, count: count as number }));
            
            console.log('\nSignificant Results (>100 counts):');
            significantResults.forEach(({ state, count }) => {
                console.log(`  |${state}⟩: ${count} counts`);
            });
        }
        
        // 9. Use iterator
        console.log('\nCircuit Gates:');
        for (const gate of bellCircuit) {
            console.log(`  ${gate.toString()}`);
        }
        
        // 10. Generic method demonstration
        const hadamardGate = QuantumGate.createGate(GateType.Hadamard, 0);
        console.log(`\nCreated gate: ${hadamardGate.toString()}`);
        
    } catch (error) {
        if (error instanceof Error) {
            console.error(`Error: ${error.message}`);
        }
    }
}

// Export for module system
export {
    GateType,
    QuantumGate,
    QuantumCircuit,
    demonstrateTypeScriptFeatures
};

// Run demo if executed directly
if (require.main === module) {
    demonstrateTypeScriptFeatures();
}
