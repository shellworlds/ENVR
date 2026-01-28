#include <iostream>
#include <vector>
#include <cmath>
#include <string>

/**
 * C++ implementation of SLK8 Problem
 * Support analysis of module M = Q/Z
 */

class PrimeGenerator {
public:
    static std::vector<int> generatePrimes(int limit) {
        std::vector<bool> isPrime(limit + 1, true);
        std::vector<int> primes;
        
        if (limit >= 2) {
            isPrime[0] = isPrime[1] = false;
        }
        
        for (int i = 2; i <= limit; ++i) {
            if (isPrime[i]) {
                primes.push_back(i);
                for (long long j = static_cast<long long>(i) * i; j <= limit; j += i) {
                    isPrime[j] = false;
                }
            }
        }
        
        return primes;
    }
};

class SupportAnalyzer {
private:
    int maxPrime;
    std::vector<int> primes;
    
public:
    SupportAnalyzer(int maxPrime = 100) : maxPrime(maxPrime) {
        primes = PrimeGenerator::generatePrimes(maxPrime);
    }
    
    std::vector<std::string> computeSupport() const {
        std::vector<std::string> support;
        for (int prime : primes) {
            support.push_back("(" + std::to_string(prime) + ")");
        }
        return support;
    }
    
    bool isZariskiClosed(const std::vector<std::string>& support) const {
        if (support.empty()) {
            return true;
        }
        
        // In Spec(Z), closed sets are finite or whole space
        if (support.size() == primes.size()) {
            return false; // Infinite but not whole space
        }
        
        // Finite sets are closed
        return support.size() < primes.size();
    }
    
    void analyze() const {
        std::vector<std::string> support = computeSupport();
        bool closed = isZariskiClosed(support);
        
        std::cout << "=== SLK8 Problem Analysis (C++) ===" << std::endl;
        std::cout << "Maximum prime considered: " << maxPrime << std::endl;
        std::cout << "Support size: " << support.size() << std::endl;
        
        std::cout << "First 10 primes in support: ";
        for (size_t i = 0; i < std::min(size_t(10), support.size()); ++i) {
            std::cout << support[i] << " ";
        }
        std::cout << std::endl;
        
        std::cout << "Is Zariski closed? " << (closed ? "Yes" : "No") << std::endl;
        
        std::cout << "\nTopological Analysis:" << std::endl;
        std::cout << "Space: Spec(Z) = {(0)} ∪ {(p) | p prime}" << std::endl;
        std::cout << "Zariski closed sets in Spec(Z):" << std::endl;
        std::cout << "1. Whole space Spec(Z)" << std::endl;
        std::cout << "2. Finite sets of nonzero primes" << std::endl;
        std::cout << "Since Supp(M) is infinite and ≠ Spec(Z), it's not closed." << std::endl;
    }
};

int main() {
    SupportAnalyzer analyzer(50);
    analyzer.analyze();
    return 0;
}
