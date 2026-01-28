import unittest
import sys
sys.path.insert(0, '../src')
from slk8_math import SupportAnalyzer

class TestSupportAnalysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = SupportAnalyzer(max_prime=50)
    
    def test_support_not_empty(self):
        support = self.analyzer.compute_support()
        self.assertGreater(len(support), 0)
    
    def test_support_contains_primes(self):
        support = self.analyzer.compute_support()
        # Check first few primes are present
        first_primes = [2, 3, 5, 7, 11]
        for prime in first_primes:
            self.assertIn((prime,), support)
    
    def test_not_zariski_closed(self):
        support = self.analyzer.compute_support()
        is_closed = self.analyzer.is_zariski_closed(support)
        self.assertFalse(is_closed, 
            "Support should not be Zariski closed (infinite set of primes)")
    
    def test_finite_set_is_closed(self):
        # Test that a finite subset would be closed
        finite_support = [(2,), (3,), (5,)]
        is_closed = self.analyzer.is_zariski_closed(finite_support)
        self.assertTrue(is_closed, 
            "Finite sets should be Zariski closed in Spec(Z)")

if __name__ == '__main__':
    unittest.main()
