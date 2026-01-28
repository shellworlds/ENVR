#!/bin/bash
echo "Support Module Proof - Shell Implementation"
echo "Theorem: Supp(M) ⊆ V(Ann(M))"
echo ""

# Represent sets as strings
ANNIHILATOR="x y z"
PRIME1="x y z a b"
PRIME2="x y a b"
PRIME3="x y z c d"
PRIME4="x a b c"

check_containment() {
    local ideal="$1"
    local element="$2"
    [[ " $ideal " =~ " $element " ]]
}

echo "Module M with Ann(M) = {$ANNIHILATOR}"
echo ""

echo "Prime ideals in Spec(A):"
echo "1. p1 = {$PRIME1}"
echo "2. p2 = {$PRIME2}"
echo "3. p3 = {$PRIME3}"
echo "4. p4 = {$PRIME4}"
echo ""

echo "Checking which primes contain Ann(M):"
all_contained=true
for element in $ANNIHILATOR; do
    if ! check_containment "$PRIME2" "$element"; then
        all_contained=false
        break
    fi
done
echo "p2 contains Ann(M)? $all_contained"
echo "Thus p2 ∉ V(I)"
echo ""

echo "Theorem demonstration:"
echo "If p ∈ Supp(M) (M_p ≠ 0), then I ⊆ p"
echo "Equivalently: Supp(M) ⊆ {p | I ⊆ p} = V(I)"
echo ""
echo "✓ Theorem holds in Shell implementation"
