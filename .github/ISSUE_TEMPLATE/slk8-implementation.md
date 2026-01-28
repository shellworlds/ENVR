---
name: SLK8 Implementation Issue
about: Report issues with SLK8 problem implementation
title: '[SLK8] '
labels: ['mathematics', 'implementation', 'bug']
assignees: ''
---

## SLK8 Implementation Issue

### Repository: [Repository Name]
### Branch: [Branch Name]

### Problem Description
[Describe the issue with the SLK8 implementation]

### Mathematical Context
- Module: M = ℚ/ℤ
- Ring: ℤ (integers)
- Expected Support: Supp(M) = { (p) | p is prime }
- Expected Topology: Not Zariski closed in Spec(ℤ)

### Affected Language Implementation
- [ ] Python
- [ ] JavaScript/Node.js
- [ ] Java
- [ ] C++
- [ ] Go
- [ ] Rust
- [ ] TypeScript
- [ ] Other: _____

### Steps to Reproduce
1. Clone repository and checkout branch
2. Run implementation: `./scripts/run_all.sh`
3. Observe issue: [Describe what happens]

### Expected Behavior
All implementations should confirm:
- Support contains primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
- Support size: Infinite (all primes)
- Zariski closed: False

### Actual Behavior
[Describe actual output]

### Environment
- OS: [e.g., Ubuntu 24.04]
- Language Version: [e.g., Python 3.11]
- Repository Branch: [e.g., DENVR48]

### Additional Context
[Add any other context about the problem]
