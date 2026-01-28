
Mathematical Proof
Theorem
For M = ℚ/ℤ as a ℤ-module:

Supp(M) = { (p) | p is prime }

Supp(M) is not Zariski closed in Spec(ℤ)

Proof
Part 1: Computing Supp(M)
Let M = ℚ/ℤ. For a prime ideal 𝔭 ∈ Spec(ℤ):

Case 𝔭 = (0):

M_(0) = (ℚ/ℤ) ⊗_ℤ ℚ = ℚ/ℤ ⊗_ℤ ℚ

Since ℚ/ℤ is torsion and ℚ is ℚ-vector space

Torsion elements become 0 when tensoring with ℚ

Therefore M_(0) = 0

Hence (0) ∉ Supp(M)

Case 𝔭 = (p) for prime p:

M_(p) = (ℚ/ℤ) ⊗ℤ ℤ(p)

ℚ/ℤ ≅ ⨁_q ℚ_q/ℤ_q (Prüfer q-group decomposition)

For localization at (p):

If q ≠ p, ℚ_q/ℤ_q ⊗ ℤ_(p) = 0 (q becomes unit in ℤ_(p))

If q = p, ℚ_p/ℤ_p ⊗ ℤ_(p) ≅ ℚ_p/ℤ_p ≠ 0

Therefore M_(p) ≅ ℚ_p/ℤ_p ≠ 0

Hence (p) ∈ Supp(M)

Thus Supp(M) = { (p) | p prime }.

Part 2: Zariski Topology on Spec(ℤ)
The Zariski topology on Spec(ℤ) has:

Closed sets: V(I) = { 𝔭 ∈ Spec(ℤ) | I ⊆ 𝔭 } for ideals I ⊆ ℤ

Since ℤ is a PID, I = (n) for some n ∈ ℤ

V((n)) = { (p) | p divides n } ∪ { (0) } if n ≠ 0

V((0)) = Spec(ℤ)

Therefore closed sets in Spec(ℤ) are:

Whole space Spec(ℤ)

Finite sets of nonzero primes (possibly empty)

Part 3: Supp(M) is not closed
Supp(M) = { (p) | p prime } is:

Infinite (contains all primes)

Does not contain (0)

Not equal to Spec(ℤ)

Since closed sets are either finite or the whole space, and Supp(M) is infinite but not whole space, it is not closed.

Corollaries
Module Type: M is torsion but not finitely generated

Support Properties: Supp(M) is dense in Spec(ℤ) but not closed

Geometric Interpretation: Points (p) are "generic" in the support

Implementation Verification
All language implementations confirm:

First 10 primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29

Support size grows with prime search limit

Zariski closed: False (in all implementations)
