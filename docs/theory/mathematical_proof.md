# Mathematical Proof: Supp(M) ⊆ V(Ann(M))

## Statement
Let A be a commutative ring with unity, M an A-module, and I = Ann_A(M) its annihilator.
Then the support of M is contained in the variety of I:
\[
\operatorname{Supp}(M) \subseteq V(I)
\]

## Proof
Let p ∈ Supp(M). By definition, M_p ≠ 0.

**Step 1:** Assume for contradiction that I ⊈ p.
Then ∃ a ∈ I such that a ∉ p.

**Step 2:** Since a ∉ p, a becomes a unit in the localization A_p.
In A_p, a/1 is invertible.

**Step 3:** But a ∈ I = Ann(M), so a·m = 0 for all m ∈ M.
Localizing at p, we get (a/1)·(m/1) = 0 in M_p for all m ∈ M.

**Step 4:** Since a/1 is invertible in A_p, multiply by its inverse:
(m/1) = 0 in M_p for all m ∈ M.

**Step 5:** This implies M_p = 0, contradicting p ∈ Supp(M).

**Conclusion:** Therefore I ⊆ p, so p ∈ V(I).
Thus Supp(M) ⊆ V(I). ∎

## Corollaries
1. dim(Supp(M)) ≤ dim(A/I)
2. If M is finitely generated, Supp(M) = V(Ann(M))
3. For M ≠ 0, Ann(M) ≠ A, so V(I) ≠ ∅
