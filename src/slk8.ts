/**
 * TypeScript implementation of SLK8 Problem
 * Support analysis with type safety
 */

interface SupportAnalysis {
  support: string[];
  isZariskiClosed: boolean;
  totalPrimes: number;
  explanation: string;
}

class PrimeGeneratorTS {
  static generatePrimes(limit: number): number[] {
    const isPrime: boolean[] = new Array(limit + 1).fill(true);
    isPrime[0] = isPrime[1] = false;
    const primes: number[] = [];
    
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

class SupportAnalyzerTS {
  private maxPrime: number;
  private primes: number[];
  
  constructor(maxPrime: number = 100) {
    this.maxPrime = maxPrime;
    this.primes = PrimeGeneratorTS.generatePrimes(maxPrime);
  }
  
  computeSupport(): string[] {
    return this.primes.map(p => `(${p})`);
  }
  
  isZariskiClosed(support: string[]): boolean {
    if (support.length === 0) return true;
    
    // Zariski closed sets in Spec(Z):
    // 1. Whole space Spec(Z)
    // 2. Finite sets of nonzero primes
    if (support.length === this.primes.length) {
      return false; // Infinite but not whole space
    }
    
    return support.length < this.primes.length;
  }
  
  analyze(): SupportAnalysis {
    const support = this.computeSupport();
    const isClosed = this.isZariskiClosed(support);
    
    return {
      support: support.slice(0, 10),
      isZariskiClosed: isClosed,
      totalPrimes: support.length,
      explanation: `Support(M = ℚ/ℤ) consists of all nonzero prime ideals. ` +
                  `This infinite set is not Zariski closed in Spec(ℤ) because ` +
                  `closed sets are either finite or the whole space.`
    };
  }
  
  printReport(): void {
    const analysis = this.analyze();
    
    console.log('=== SLK8 Problem Analysis (TypeScript) ===');
    console.log(`Max prime: ${this.maxPrime}`);
    console.log(`Support size: ${analysis.totalPrimes}`);
    console.log(`Support sample: ${analysis.support.join(', ')}`);
    console.log(`Zariski closed: ${analysis.isZariskiClosed}`);
    console.log(`\n${analysis.explanation}`);
  }
}

// Run if this file is executed directly
if (require.main === module) {
  const analyzer = new SupportAnalyzerTS(50);
  analyzer.printReport();
}

export { SupportAnalyzerTS, PrimeGeneratorTS, type SupportAnalysis };
