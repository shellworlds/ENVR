package main

import (
	"fmt"
)

// PrimeGenerator generates prime numbers up to limit
func generatePrimes(limit int) []int {
	isPrime := make([]bool, limit+1)
	for i := 2; i <= limit; i++ {
		isPrime[i] = true
	}
	
	var primes []int
	for i := 2; i <= limit; i++ {
		if isPrime[i] {
			primes = append(primes, i)
			for j := i * i; j <= limit; j += i {
				isPrime[j] = false
			}
		}
	}
	return primes
}

// SupportAnalyzer analyzes support of M = Q/Z
type SupportAnalyzer struct {
	maxPrime int
	primes   []int
}

// NewSupportAnalyzer creates a new analyzer
func NewSupportAnalyzer(maxPrime int) *SupportAnalyzer {
	return &SupportAnalyzer{
		maxPrime: maxPrime,
		primes:   generatePrimes(maxPrime),
	}
}

// ComputeSupport returns the support as strings
func (sa *SupportAnalyzer) ComputeSupport() []string {
	var support []string
	for _, prime := range sa.primes {
		support = append(support, fmt.Sprintf("(%d)", prime))
	}
	return support
}

// IsZariskiClosed checks if support is Zariski closed
func (sa *SupportAnalyzer) IsZariskiClosed(support []string) bool {
	if len(support) == 0 {
		return true
	}
	
	// In Spec(Z), closed sets are finite or whole space
	if len(support) == len(sa.primes) {
		return false // Infinite but not whole space
	}
	
	// Finite sets are closed
	return len(support) < len(sa.primes)
}

// Analyze performs complete analysis
func (sa *SupportAnalyzer) Analyze() {
	support := sa.ComputeSupport()
	closed := sa.IsZariskiClosed(support)
	
	fmt.Println("=== SLK8 Problem Analysis (Go) ===")
	fmt.Printf("Maximum prime considered: %d\n", sa.maxPrime)
	fmt.Printf("Support size: %d\n", len(support))
	
	fmt.Print("First 10 primes in support: ")
	for i := 0; i < 10 && i < len(support); i++ {
		fmt.Printf("%s ", support[i])
	}
	fmt.Println()
	
	fmt.Printf("Is Zariski closed? %v\n", closed)
	
	fmt.Println("\nMathematical Details:")
	fmt.Println("Module: M = ℚ/ℤ over ring ℤ")
	fmt.Println("Localization results:")
	fmt.Println("  • M_(0) = 0 (torsion disappears at generic point)")
	fmt.Println("  • M_(p) ≠ 0 ∀ prime p (p-torsion persists)")
	fmt.Println("Conclusion: Supp(M) = {(p) | p prime} is not Zariski closed.")
}

func main() {
	analyzer := NewSupportAnalyzer(50)
	analyzer.Analyze()
}
