import React, { useState, useEffect } from 'react';
import './SupportVisualizer.css';

const SupportVisualizer = ({ maxPrime = 50 }) => {
  const [primes, setPrimes] = useState([]);
  const [isClosed, setIsClosed] = useState(false);
  
  // Generate primes up to maxPrime
  const generatePrimes = (limit) => {
    const sieve = new Array(limit + 1).fill(true);
    sieve[0] = sieve[1] = false;
    const primesList = [];
    
    for (let i = 2; i <= limit; i++) {
      if (sieve[i]) {
        primesList.push(i);
        for (let j = i * i; j <= limit; j += i) {
          sieve[j] = false;
        }
      }
    }
    return primesList;
  };
  
  useEffect(() => {
    const primesList = generatePrimes(maxPrime);
    setPrimes(primesList);
    // Support is not Zariski closed if it contains all primes (infinite concept)
    setIsClosed(primesList.length < maxPrime / 2); // Simplified logic
  }, [maxPrime]);
  
  return (
    <div className="support-visualizer">
      <h2>SLK8: Support of M = ℚ/ℤ</h2>
      
      <div className="mathematical-result">
        <h3>Mathematical Result</h3>
        <div className="result-card">
          <p><strong>Support(M)</strong> = {"{"} (p) | p is prime {"}"}</p>
          <p><strong>Zariski Closed:</strong> {isClosed ? 'Yes' : 'No'}</p>
          <p className="explanation">
            The support consists of all nonzero prime ideals. 
            This infinite set is not closed in the Zariski topology on Spec(ℤ).
          </p>
        </div>
      </div>
      
      <div className="primes-list">
        <h3>Prime Ideals in Support (first {Math.min(20, primes.length)})</h3>
        <div className="primes-grid">
          {primes.slice(0, 20).map(prime => (
            <div key={prime} className="prime-item">
              ({prime})
            </div>
          ))}
        </div>
        <p className="count">Total primes ≤ {maxPrime}: {primes.length}</p>
      </div>
      
      <div className="topology-info">
        <h3>Zariski Topology on Spec(ℤ)</h3>
        <ul>
          <li>Closed sets: Whole space or finite sets of nonzero primes</li>
          <li>Generic point: (0) corresponding to zero ideal</li>
          <li>Support(M) excludes (0) but includes all primes</li>
          <li>Thus Support(M) is infinite but not whole space → not closed</li>
        </ul>
      </div>
    </div>
  );
};

export default SupportVisualizer;
