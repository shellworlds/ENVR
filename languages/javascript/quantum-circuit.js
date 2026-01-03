/**
 * JavaScript: Quantum Circuit Simulator
 * ES6+ features, async/await, classes, modules
 */

class QuantumGate {
    constructor(type, target, control = null) {
        this.type = type;
        this.target = target;
        this.control = control;
    }

    apply(circuit) {
        switch (this.type.toLowerCase()) {
            case 'h':
                circuit.h(this.target);
                break;
            case 'x':
                circuit.x(this.target);
                break;
            case 'cx':
                if (this.control !== null) {
                    circuit.cx(this.control, this.target);
                }
                break;
            default:
                throw new Error(`Unknown gate type: ${this.type}`);
        }
    }

    toString() {
        return `${this.type}(${this.target}${this.control !== null ? `, ${this.control}` : ''})`;
    }
}

class QuantumCircuit {
    constructor(numQubits, name = 'Untitled Circuit') {
        this.numQubits = numQubits;
        this.name = name;
        this.gates = [];
        this.results = null;
    }

    addGate(gate) {
        if (gate.target >= this.numQubits) {
            throw new Error(`Gate target qubit ${gate.target} out of bounds`);
        }
        if (gate.control !== null && gate.control >= this.numQubits) {
            throw new Error(`Control qubit ${gate.control} out of bounds`);
        }
        this.gates.push(gate);
        return this;
    }

    async simulate(shots = 1024) {
        console.log(`Simulating ${this.name} with ${shots} shots...`);
        
        // Simulate quantum computation
        return new Promise((resolve) => {
            setTimeout(() => {
                // Mock simulation results
                this.results = this.generateMockResults(shots);
                console.log('Simulation completed:', this.results);
                resolve(this.results);
            }, 100);
        });
    }

    generateMockResults(shots) {
        const results = {};
        const numStates = 1 << this.numQubits; // 2^n
        
        // Generate probabilistic distribution
        let remainingShots = shots;
        for (let i = 0; i < numStates - 1; i++) {
            const state = i.toString(2).padStart(this.numQubits, '0');
            const count = Math.floor(Math.random() * remainingShots / 2);
            results[state] = count;
            remainingShots -= count;
        }
        
        // Remaining shots go to last state
        const lastState = (numStates - 1).toString(2).padStart(this.numQubits, '0');
        results[lastState] = remainingShots;
        
        return results;
    }

    calculateEntropy() {
        if (!this.results) {
            throw new Error('Run simulation first');
        }

        const totalShots = Object.values(this.results).reduce((a, b) => a + b, 0);
        let entropy = 0;

        for (const count of Object.values(this.results)) {
            const probability = count / totalShots;
            if (probability > 0) {
                entropy -= probability * Math.log2(probability);
            }
        }

        return entropy;
    }

    static createBellState() {
        const circuit = new QuantumCircuit(2, 'Bell State');
        circuit.addGate(new QuantumGate('h', 0))
               .addGate(new QuantumGate('cx', 1, 0));
        return circuit;
    }

    // Generator function for circuit steps
    *stepThrough() {
        yield `Starting circuit: ${this.name}`;
        for (const [index, gate] of this.gates.entries()) {
            yield `Step ${index + 1}: Applying ${gate.toString()}`;
        }
        yield 'Circuit complete';
    }

    // Async iteration example
    async *asyncStepThrough(delay = 500) {
        for await (const step of this.stepThrough()) {
            await new Promise(resolve => setTimeout(resolve, delay));
            yield step;
        }
    }
}

// Modern JavaScript features demonstration
const quantumFeaturesDemo = async () => {
    console.log('=== JavaScript Quantum Features Demo ===\n');

    // 1. Create Bell state using factory method
    const bellCircuit = QuantumCircuit.createBellState();
    
    // 2. Array destructuring and spread operator
    const gates = [new QuantumGate('h', 0), new QuantumGate('x', 1)];
    bellCircuit.gates = [...bellCircuit.gates, ...gates];
    
    // 3. Optional chaining and nullish coalescing
    const gateCount = bellCircuit.gates?.length ?? 0;
    console.log(`Circuit has ${gateCount} gates`);
    
    // 4. Template literals
    console.log(`Circuit name: ${bellCircuit.name}`);
    console.log(`Qubits: ${bellCircuit.numQubits}\n`);
    
    // 5. Async/await simulation
    try {
        await bellCircuit.simulate(1000);
        
        // 6. Object destructuring
        const { results } = bellCircuit;
        
        // 7. Map and filter operations
        const states = Object.entries(results)
            .map(([state, count]) => ({ state, probability: count / 1000 }))
            .filter(({ probability }) => probability > 0.1);
        
        console.log('States with probability > 0.1:');
        states.forEach(({ state, probability }) => {
            console.log(`  |${state}⟩: ${(probability * 100).toFixed(1)}%`);
        });
        
        // 8. Calculate entropy
        const entropy = bellCircuit.calculateEntropy();
        console.log(`\nCircuit entropy: ${entropy.toFixed(3)} bits`);
        
        // 9. Generator demonstration
        console.log('\nCircuit steps:');
        for (const step of bellCircuit.stepThrough()) {
            console.log(`  ${step}`);
        }
        
        // 10. Async generator demonstration
        console.log('\nAsync circuit execution:');
        for await (const step of bellCircuit.asyncStepThrough(200)) {
            console.log(`  ${step}`);
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        QuantumGate,
        QuantumCircuit,
        quantumFeaturesDemo
    };
}

// Run demo if executed directly
if (typeof window === 'undefined' && require.main === module) {
    quantumFeaturesDemo();
}
