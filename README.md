# Projective Module Theorem Implementation

## Overview
Multi-language implementation of projective module theorems from commutative algebra.

## Theorems Implemented
1. **Lifting Property**: P projective ⇔ Hom(P,–) exact
2. **Splitting Property**: P projective ⇔ every sequence 0→L→M→P→0 splits
3. **Direct Summand**: P projective ⇔ P is direct summand of free module
4. **Local Ring Theorem**: Over local ring, f.g. projective = free

## File Structure
- `src/` - Source code implementations
- `api/` - Web API and interface
- `scripts/` - Automation and deployment
- `docs/` - Documentation and web interface
- `config/` - Configuration files
- `docker/` - Containerization setup
- `tests/` - Test files

## Languages Used
1. Python - Main implementation
2. C++ - High-performance computation
3. Java - Object-oriented design
4. Go - Concurrent verification
5. JavaScript/Node.js - Web API
6. Shell Script - Automation
7. HTML/CSS - Web interface
8. Make - Build automation

## Quick Start
```bash
# Clone repository
git clone <repo-url>
cd ENVR_Project

# Install dependencies
./scripts/deploy.sh

# Run all verifications
make test

# Start web API
cd api && node module_api.js
# Using Docker
docker build -t projective-modules -f docker/Dockerfile .
docker run -p 3000:3000 projective-modules

# Manual deployment
./scripts/deploy.sh
API Endpoints
GET /api/modules - List modules

POST /api/modules - Create module

GET /api/modules/:id/theorems - Verify theorems

GET /health - Health check

System Requirements
Ubuntu 20.04+ / macOS / Windows WSL2

Python 3.8+

Node.js 16+

Java 11+

Go 1.16+

GCC/G++ 9+

Git

License
Educational and research purposes
