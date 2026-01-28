package main

import "fmt"

type PrimeIdeal struct {
	name     string
	elements map[string]bool
}

func NewPrimeIdeal(name string, elements []string) *PrimeIdeal {
	p := &PrimeIdeal{
		name:     name,
		elements: make(map[string]bool),
	}
	for _, e := range elements {
		p.elements[e] = true
	}
	return p
}

func (p *PrimeIdeal) Contains(ideal map[string]bool) bool {
	for e := range ideal {
		if !p.elements[e] {
			return false
		}
	}
	return true
}

func main() {
	fmt.Println("Support Module Proof - Go Implementation")
	fmt.Println("Theorem: Supp(M) ⊆ V(Ann(M))\n")
	
	// Annihilator
	annihilator := map[string]bool{
		"x": true,
		"y": true,
		"z": true,
	}
	
	fmt.Print("Ann(M) = {")
	for e := range annihilator {
		fmt.Printf("%s ", e)
	}
	fmt.Println("}\n")
	
	// Prime ideals
	primes := []*PrimeIdeal{
		NewPrimeIdeal("p1", []string{"x", "y", "z", "a", "b"}),
		NewPrimeIdeal("p2", []string{"x", "y", "a", "b"}),
		NewPrimeIdeal("p3", []string{"x", "y", "z", "c", "d"}),
		NewPrimeIdeal("p4", []string{"x", "a", "b", "c"}),
	}
	
	fmt.Println("V(I) contains:")
	for _, p := range primes {
		if p.Contains(annihilator) {
			fmt.Printf("  %s\n", p.name)
		}
	}
	
	fmt.Println("\nMathematical reasoning:")
	fmt.Println("Let p ∈ Supp(M), so M_p ≠ 0.")
	fmt.Println("Assume ∃a ∈ I with a ∉ p.")
	fmt.Println("Then a is unit in A_p, but aM = 0.")
	fmt.Println("Thus M_p = 0, contradiction.")
	fmt.Println("So I ⊆ p, hence p ∈ V(I).")
	
	fmt.Println("\n✓ Go implementation complete")
}
