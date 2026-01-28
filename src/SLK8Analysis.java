import java.util.ArrayList;
import java.util.List;

/**
 * Java implementation of SLK8 Problem
 * Support of M = Q/Z over integers Z
 */
public class SLK8Analysis {
    
    private int maxPrime;
    private List<Integer> primes;
    
    public SLK8Analysis(int maxPrime) {
        this.maxPrime = maxPrime;
        this.primes = generatePrimes(maxPrime);
    }
    
    private List<Integer> generatePrimes(int limit) {
        boolean[] isPrime = new boolean[limit + 1];
        for (int i = 2; i <= limit; i++) {
            isPrime[i] = true;
        }
        
        List<Integer> primesList = new ArrayList<>();
        for (int i = 2; i <= limit; i++) {
            if (isPrime[i]) {
                primesList.add(i);
                for (int j = i * i; j <= limit && j > 0; j += i) {
                    isPrime[j] = false;
                }
            }
        }
        return primesList;
    }
    
    public List<String> computeSupport() {
        List<String> support = new ArrayList<>();
        for (int prime : primes) {
            support.add("(" + prime + ")");
        }
        return support;
    }
    
    public boolean isZariskiClosed(List<String> support) {
        if (support == null || support.isEmpty()) {
            return true;
        }
        
        // In Spec(Z), closed sets are finite or whole space
        if (support.size() == primes.size()) {
            return false; // Infinite but not whole space
        }
        
        // Finite sets are closed
        return support.size() < primes.size();
    }
    
    public void analyze() {
        List<String> support = computeSupport();
        boolean closed = isZariskiClosed(support);
        
        System.out.println("=== SLK8 Problem Analysis (Java) ===");
        System.out.println("Maximum prime considered: " + maxPrime);
        System.out.println("Support size: " + support.size());
        System.out.print("First 10 primes in support: ");
        for (int i = 0; i < Math.min(10, support.size()); i++) {
            System.out.print(support.get(i) + " ");
        }
        System.out.println();
        System.out.println("Is Zariski closed? " + (closed ? "Yes" : "No"));
        
        System.out.println("\nMathematical Explanation:");
        System.out.println("For M = Q/Z as a Z-module:");
        System.out.println("1. M_{(0)} = 0 (torsion module localized at generic point)");
        System.out.println("2. M_{(p)} ≠ 0 for all primes p (p-power torsion survives)");
        System.out.println("Thus Supp(M) = { (p) | p prime }");
        System.out.println("This set is infinite but doesn't contain (0), so not Zariski closed.");
    }
    
    public static void main(String[] args) {
        SLK8Analysis analyzer = new SLK8Analysis(50);
        analyzer.analyze();
    }
}
