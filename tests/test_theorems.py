#!/usr/bin/env python3
"""
File: test_theorems.py
Purpose: Test cases for projective module theorems
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(file), '..', 'src'))

Import our implementation
from projective_module import Ring, ProjectiveModule, Module, ExactSequence

def test_theorem_1():
"""Test lifting property"""
print("Testing Theorem 1: Lifting Property")
ring = Ring("TestRing", False)
P = ProjectiveModule(ring, "P")

text
# Create test modules
M = Module(ring, "M")
N = Module(ring, "N")

# This should work since P is projective
try:
    mu = P.lifting_property(None, None)
    print("✓ Theorem 1 passed: Lifting property verified")
    return True
except Exception as e:
    print(f"✗ Theorem 1 failed: {e}")
    return False
def test_theorem_2():
"""Test splitting property"""
print("\nTesting Theorem 2: Splitting Property")
ring = Ring("TestRing", False)
P = ProjectiveModule(ring, "P")
L = Module(ring, "L")
M = Module(ring, "M")

text
seq = ExactSequence(L, M, P)
result = seq.splits()

if result:
    print("✓ Theorem 2 passed: Sequence splits for projective module")
    return True
else:
    print("✗ Theorem 2 failed: Sequence should split")
    return False
def test_theorem_3():
"""Test direct summand property"""
print("\nTesting Theorem 3: Direct Summand of Free")
ring = Ring("TestRing", False)
P = ProjectiveModule(ring, "P")

text
result = P.is_direct_summand_of_free()

if result:
    print("✓ Theorem 3 passed: Projective module is direct summand of free")
    return True
else:
    print("✗ Theorem 3 failed")
    return False
def test_theorem_4():
"""Test local ring theorem"""
print("\nTesting Theorem 4: Local Ring Theorem")

text
# Test with local ring
local_ring = Ring("LocalRing", True)
P_local = ProjectiveModule(local_ring, "P_local")
P_local.generators = ["g1", "g2"]  # Make it finitely generated

result = P_local.check_local_free()

if result and P_local.is_free:
    print("✓ Theorem 4 passed: Over local ring, f.g. projective is free")
    return True
else:
    print("✗ Theorem 4 failed")
    return False
def run_all_tests():
"""Run all theorem tests"""
print("=" * 60)
print("PROJECTIVE MODULE THEOREM TEST SUITE")
print("=" * 60)

text
results = []
results.append(test_theorem_1())
results.append(test_theorem_2())
results.append(test_theorem_3())
results.append(test_theorem_4())

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)

passed = sum(results)
total = len(results)

print(f"Tests passed: {passed}/{total}")
print(f"Success rate: {(passed/total)*100:.1f}%")

if passed == total:
    print("✓ ALL TESTS PASSED")
    return True
else:
    print("✗ SOME TESTS FAILED")
    return False
if name == "main":
success = run_all_tests()
sys.exit(0 if success else 1)
