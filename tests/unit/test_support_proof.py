import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/python'))

import unittest
from support_proof import Module, PrimeIdeal, support_is_in_v

class TestSupportProof(unittest.TestCase):
    
    def setUp(self):
        self.ring = "TestRing"
        self.module = Module("TestModule", self.ring)
        self.module.annihilator = {"a", "b", "c"}
    
    def test_prime_contains_annihilator(self):
        """Test if prime ideal contains annihilator"""
        prime = PrimeIdeal(["a", "b", "c", "d"])
        self.assertTrue(prime.contains(self.module.annihilator))
    
    def test_prime_does_not_contain_annihilator(self):
        """Test if prime ideal doesn't contain annihilator"""
        prime = PrimeIdeal(["a", "d", "e"])
        self.assertFalse(prime.contains(self.module.annihilator))
    
    def test_support_inclusion(self):
        """Test the main theorem"""
        primes = [
            PrimeIdeal(["a", "b", "c", "d"]),
            PrimeIdeal(["a", "b", "d"]),
            PrimeIdeal(["a", "b", "c", "e"]),
        ]
        
        result = support_is_in_v(self.module, primes)
        self.assertTrue(result["proof_holds"])
    
    def test_module_initialization(self):
        """Test module creation"""
        self.assertEqual(self.module.name, "TestModule")
        self.assertEqual(self.module.ring, self.ring)

if __name__ == '__main__':
    unittest.main()
