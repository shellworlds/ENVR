/*
 * Rust implementation of SLK8 Problem
 * Support analysis with memory safety
 */

fn generate_primes(limit: usize) -> Vec<usize> {
    let mut is_prime = vec![true; limit + 1];
    if limit >= 2 {
        is_prime[0] = false;
        is_prime[1] = false;
    }
    
    let mut primes = Vec::new();
    for i in 2..=limit {
        if is_prime[i] {
            primes.push(i);
            let mut j = i * i;
            while j <= limit {
                is_prime[j] = false;
                j += i;
            }
        }
    }
    primes
}

struct SupportAnalyzerRust {
    max_prime: usize,
    primes: Vec<usize>,
}

impl SupportAnalyzerRust {
    fn new(max_prime: usize) -> Self {
        let primes = generate_primes(max_prime);
        SupportAnalyzerRust { max_prime, primes }
    }
    
    fn compute_support(&self) -> Vec<String> {
        self.primes.iter()
            .map(|&p| format!("({})", p))
            .collect()
    }
    
    fn is_zariski_closed(&self, support: &[String]) -> bool {
        if support.is_empty() {
            return true;
        }
        
        // In Spec(Z), closed sets are finite or whole space
        if support.len() == self.primes.len() {
            return false; // Infinite but not whole space
        }
        
        // Finite sets are closed
        support.len() < self.primes.len()
    }
    
    fn analyze(&self) {
        let support = self.compute_support();
        let closed = self.is_zariski_closed(&support);
        
        println!("=== SLK8 Problem Analysis (Rust) ===");
        println!("Maximum prime considered: {}", self.max_prime);
        println!("Support size: {}", support.len());
        
        print!("First 10 primes in support: ");
        for i in 0..std::cmp::min(10, support.len()) {
            print!("{} ", support[i]);
        }
        println!();
        
        println!("Is Zariski closed? {}", if closed { "Yes" } else { "No" });
        
        println!("\nMathematical Interpretation:");
        println!("Ring: ℤ (integers)");
        println!("Module: M = ℚ/ℤ");
        println!("Support: Supp(M) = {{ (p) | p ∈ ℙ }}");
        println!("Topology: Zariski topology on Spec(ℤ)");
        println!("Result: Support is not closed (infinite ≠ whole space)");
    }
}

fn main() {
    let analyzer = SupportAnalyzerRust::new(50);
    analyzer.analyze();
}
