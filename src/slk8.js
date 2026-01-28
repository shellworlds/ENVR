/**
 * JavaScript/Node.js implementation of SLK8 Problem
 * Support of M = Q/Z analysis
 */

const { performance } = require('perf_hooks');

class PrimeGenerator {
    static generatePrimes(limit) {
        const primes = [];
        const isPrime = new Array(limit + 1).fill(true);
        isPrime[0] = isPrime[1] = false;
        
        for (let i = 2; i <= limit; i++) {
            if (isPrime[i]) {
                primes.push(i);
                for (let j = i * i; j <= limit; j += i) {
                    isPrime[j] = false;
                }
            }
        }
        return primes;
    }
}

class SupportAnalyzer {
    constructor(maxPrime = 100) {
        this.maxPrime = maxPrime;
        this.primes = PrimeGenerator.generatePrimes(maxPrime);
    }
    
    computeSupport() {
        return this.primes.map(p => `(${p})`);
    }
    
    isZariskiClosed(support) {
        if (!support || support.length === 0) return true;
        
        // In Spec(Z), closed sets are finite or whole space
        if (support.length === this.primes.length) {
            return false; // Infinite but not whole space (missing (0))
        }
        
        // Finite sets are closed
        return support.length < this.primes.length;
    }
    
    analyze() {
        const support = this.computeSupport();
        const isClosed = this.isZariskiClosed(support);
        
        console.log('=== SLK8 Problem Analysis (JavaScript) ===');
        console.log(`Max prime considered: ${this.maxPrime}`);
        console.log(`Support size: ${support.length}`);
        console.log(`Support (first 10): ${support.slice(0, 10).join(', ')}`);
        console.log(`Is Zariski closed? ${isClosed ? 'Yes' : 'No'}`);
        console.log('\nExplanation:');
        console.log('Support(M) = { (p) | p prime }');
        console.log('This is an infinite set of nonzero primes.');
        console.log('In Spec(Z), closed sets are either:');
        console.log('1. Whole space Spec(Z) = {(0)} ∪ {(p)}');
        console.log('2. Finite sets of nonzero primes');
        console.log('Since Support(M) is infinite but not whole space, it is not closed.');
        
        return {
            support: support,
            isZariskiClosed: isClosed,
            totalPrimes: support.length
        };
    }
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SupportAnalyzer, PrimeGenerator };
}

// Run if executed directly
if (require.main === module) {
    const analyzer = new SupportAnalyzer(50);
    analyzer.analyze();
}
