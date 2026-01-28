"""
Python implementation of SLK8 Problem:
Support of M = Q/Z and Zariski topology analysis.
"""

from sympy import isprime, primerange
import numpy as np

class SupportAnalyzer:
    """Analyze support of module M = Q/Z over integers Z."""
    
    def __init__(self, max_prime=100):
        self.max_prime = max_prime
        self.primes = list(primerange(2, max_prime + 1))
    
    def compute_support(self):
        """Compute Supp(M) = {(p) | p prime}."""
        return [(p,) for p in self.primes]
    
    def is_zariski_closed(self, support_set):
        """
        Check if support set is Zariski closed.
        In Spec(Z), closed sets are finite sets of nonzero primes or whole space.
        """
        if not support_set:
            return True
        
        # Check if it's the whole space (excluding generic point)
        if len(support_set) == len(self.primes):
            return False  # Not closed in Spec(Z)
        
        # Check if finite
        if len(support_set) < len(self.primes):
            return True   # Finite sets are closed
        
        return False
    
    def generate_report(self):
        """Generate analysis report."""
        support = self.compute_support()
        is_closed = self.is_zariski_closed(support)
        
        report = {
            "problem": "SLK8: Support of M = Q/Z",
            "support": [p[0] for p in support[:10]],  # First 10 primes
            "support_size": len(support),
            "is_zariski_closed": is_closed,
            "explanation": (
                "Support is infinite set of all nonzero prime ideals, "
                "which is not finite and not whole space, hence not Zariski closed."
            )
        }
        return report

def main():
    analyzer = SupportAnalyzer(max_prime=50)
    report = analyzer.generate_report()
    
    print("=== SLK8 Problem Solution ===")
    print(f"Problem: {report['problem']}")
    print(f"Support (first 10): {report['support']}")
    print(f"Total primes in support: {report['support_size']}")
    print(f"Is Zariski closed? {report['is_zariski_closed']}")
    print(f"Explanation: {report['explanation']}")

if __name__ == "__main__":
    main()
