#include <iostream>
#include <set>
#include <vector>
#include <string>

using namespace std;

class PrimeIdeal {
private:
    string name;
    set<string> elements;
    
public:
    PrimeIdeal(string n, vector<string> elems) : name(n) {
        for (const auto& e : elems) {
            elements.insert(e);
        }
    }
    
    bool contains(const set<string>& ideal) const {
        for (const auto& e : ideal) {
            if (elements.find(e) == elements.end()) {
                return false;
            }
        }
        return true;
    }
    
    string getName() const { return name; }
};

int main() {
    cout << "Support Module Proof - C++ Implementation" << endl;
    cout << "Theorem: Supp(M) ⊆ V(Ann(M))" << endl << endl;
    
    // Annihilator
    set<string> annihilator = {"x", "y", "z"};
    
    cout << "Ann(M) = {";
    for (const auto& e : annihilator) {
        cout << e << " ";
    }
    cout << "}" << endl << endl;
    
    // Prime ideals
    vector<PrimeIdeal> primes = {
        PrimeIdeal("p1", {"x", "y", "z", "a", "b"}),
        PrimeIdeal("p2", {"x", "y", "a", "b"}),
        PrimeIdeal("p3", {"x", "y", "z", "c", "d"}),
        PrimeIdeal("p4", {"x", "a", "b", "c"})
    };
    
    cout << "Checking containment:" << endl;
    for (const auto& p : primes) {
        if (p.contains(annihilator)) {
            cout << p.getName() << " ∈ V(I)" << endl;
        } else {
            cout << p.getName() << " ∉ V(I)" << endl;
        }
    }
    
    cout << endl << "Proof Summary:" << endl;
    cout << "For any p ∈ Supp(M):" << endl;
    cout << "1. M_p ≠ 0" << endl;
    cout << "2. If a ∈ I and a ∉ p, then a is unit in A_p" << endl;
    cout << "3. But aM = 0 ⇒ M_p = 0" << endl;
    cout << "4. Contradiction ⇒ I ⊆ p" << endl;
    cout << "5. Therefore p ∈ V(I)" << endl;
    
    cout << endl << "✓ C++ implementation complete" << endl;
    return 0;
}
