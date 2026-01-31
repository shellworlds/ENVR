# Getting Started with Quantum JV Platform

## Prerequisites
- Ubuntu 20.04+ / MacOS 12+ / Windows 10+ (WSL2)
- Python 3.10+
- Node.js 18+
- Git 2.30+
- 16GB RAM minimum

## Installation
\`\`\`bash
# Clone the repository
git clone https://github.com/shellworlds/ENVR.git
cd ENVR

# Run system verification
./scripts/verify_requirements.sh

# Setup environment
./scripts/setup_environment.sh

# Build all components
./scripts/build_all.sh
\`\`\`

## Quick Start
1. **Run Python quantum examples:**
   \`\`\`bash
   source venv/bin/activate
   python src/python/quantum_base.py
   \`\`\`

2. **Start Node.js server:**
   \`\`\`bash
   cd src/node
   npm start
   \`\`\`

3. **Run C++ simulator:**
   \`\`\`bash
   ./scripts/build_cpp.sh
   \`\`\`

## Client Integration
For client repository integration:
\`\`\`bash
# Setup client directories
./scripts/setup_clients.sh

# Sync platform files to clients
./scripts/sync_to_clients.sh

# Push to GitHub (requires permissions)
./scripts/push_to_github.sh
\`\`\`

## API Documentation
Base URL: \`http://localhost:8000\`

### Endpoints
- \`GET /api/quantum/health\` - Health check
- \`POST /api/quantum/circuit\` - Create quantum circuit
- \`GET /api/quantum/simulate/{id}\` - Run simulation
- \`POST /api/clients/register\` - Register new client

## Support
- Documentation: https://github.com/shellworlds/ENVR/wiki
- Issues: https://github.com/shellworlds/ENVR/issues
- Email: quantum-support@shellworlds.com
