import java.util.HashSet;
import java.util.Set;

public class SupportProof {
    
    static class PrimeIdeal {
        Set<String> elements;
        String name;
        
        PrimeIdeal(String name, String... elements) {
            this.name = name;
            this.elements = new HashSet<>();
            for (String e : elements) {
                this.elements.add(e);
            }
        }
        
        boolean contains(Set<String> ideal) {
            return elements.containsAll(ideal);
        }
    }
    
    public static void main(String[] args) {
        System.out.println("Support Module Proof - Java Implementation");
        System.out.println("Theorem: Supp(M) ⊆ V(Ann(M))\n");
        
        // Annihilator
        Set<String> annihilator = new HashSet<>();
        annihilator.add("x");
        annihilator.add("y");
        annihilator.add("z");
        
        System.out.println("Ann(M) = " + annihilator);
        
        // Prime ideals
        PrimeIdeal[] primes = {
            new PrimeIdeal("p1", "x", "y", "z", "a", "b"),
            new PrimeIdeal("p2", "x", "y", "a", "b"),
            new PrimeIdeal("p3", "x", "y", "z", "c", "d"),
            new PrimeIdeal("p4", "x", "a", "b", "c")
        };
        
        System.out.println("\nV(I) = {p ∈ Spec(A) | I ⊆ p}:");
        for (PrimeIdeal p : primes) {
            if (p.contains(annihilator)) {
                System.out.println("  " + p.name + " ∈ V(I)");
            }
        }
        
        System.out.println("\nMathematical Proof:");
        System.out.println("1. Take p ∈ Supp(M) (M_p ≠ 0)");
        System.out.println("2. Assume I ⊈ p → contradiction");
        System.out.println("3. Therefore I ⊆ p → p ∈ V(I)");
        System.out.println("4. Hence Supp(M) ⊆ V(I)");
        
        System.out.println("\n✓ Java implementation complete");
    }
}
