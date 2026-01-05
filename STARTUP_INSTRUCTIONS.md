# ENVR11 Travel Agent ML System - Startup Instructions

## Quick Start (All-in-One)

```bash
# 1. Clone and navigate to ENVR11
git clone -b ENVR11 https://github.com/shellworlds/ENVR.git ENVR11
cd ENVR11

# 2. Run complete installation
./scripts/install_all.sh

# 3. Start all services
./start_all.sh
Manual Startup (Individual Services)
Option A: Python ML Engine Only
bash
cd ENVR11
source envr11_env/bin/activate
python backend/travel_ml_engine.py
Option B: Node.js API Server Only
bash
cd ENVR11/backend
node server.js
Option C: Go Quantum Service Only
bash
cd ENVR11/backend
go build -o quantum_travel_service quantum_service.go
./quantum_travel_service
Option D: React Frontend Only
bash
cd ENVR11/frontend
npm install
npm run dev
Access Points After Startup
Service	URL	Port	Description
Frontend Dashboard	http://localhost:3000	3000	React travel dashboard
API Documentation	http://localhost:8000/docs	8000	FastAPI Swagger UI
Node.js API	http://localhost:8000/api/travel-data	8000	Travel data API
Go Quantum Service	http://localhost:8081/health	8081	Quantum optimization
System Health	http://localhost:8000/health	8000	System status check
Platform-Specific Instructions
Ubuntu/Linux
bash
# Complete installation
sudo apt-get update
sudo apt-get install python3 python3-pip nodejs npm golang openjdk-11-jdk g++
./scripts/deploy_envr11.sh
macOS
bash
# Install prerequisites via Homebrew
brew install python node go openjdk
./scripts/install_all.sh
Windows (WSL2)
bash
# Use Ubuntu WSL2 distribution
wsl --install -d Ubuntu
# Then follow Ubuntu instructions above
Docker Deployment
bash
# Build and run with Docker Compose
docker-compose up --build

# Or build individual containers
docker build -t envr11-ml-engine .
docker run -p 8000:8000 envr11-ml-engine
Testing the System
Test Quantum Optimization
bash
curl -X POST http://localhost:8000/api/quantum-optimize \
  -H "Content-Type: application/json" \
  -d '{"destinations": ["Paris", "London", "Rome"], "constraints": {"max_destinations": 2, "max_budget": 1000}}'
Test Price Prediction
bash
curl "http://localhost:8000/api/price-prediction?origin=NYC&destination=London&date=2024-06-15&passengers=2"
Test System Health
bash
curl http://localhost:8000/health
Configuration
Environment Variables
Create .env file:

bash
cp .env.example .env
# Edit .env with your API keys and configuration
API Keys (Required for Production)
Amadeus API: https://developers.amadeus.com

Skyscanner API: https://partners.skyscanner.net

Weather API: https://openweathermap.org/api

Troubleshooting
Common Issues
Port already in use

bash
# Find and kill process using port
sudo lsof -i :3000
sudo kill -9 <PID>
Python dependencies missing

bash
source envr11_env/bin/activate
pip install -r requirements_envr11.txt
Node.js modules missing

bash
cd frontend
rm -rf node_modules package-lock.json
npm install
Go compilation errors

bash
cd backend
go mod init envr11
go mod tidy
go build -o quantum_travel_service quantum_service.go
Monitoring
System Metrics
CPU/Memory: Use htop or glances

Quantum Jobs: Check quantum service logs

ML Predictions: Monitor prediction accuracy

API Performance: Use /api/system-metrics endpoint

Log Files
bash
# View all service logs
tail -f backend/server.log quantum_service.log frontend/logs/*
Maintenance
Regular Tasks
Daily: Check system health and error logs

Weekly: Retrain ML models, update dependencies

Monthly: Security updates, backup verification

Quarterly: Performance review, architecture assessment

Backup
bash
# Backup configuration and data
tar -czf envr11_backup_$(date +%Y%m%d).tar.gz \
  backend/ frontend/ scripts/ docs/ data/ .env
Support
Documentation: docs/ directory

Issue Tracking: GitHub repository issues

Email Support: support@envr11-travel.com

Emergency: 24/7 on-call rotation

Final Verification Checklist
All services start without errors

Dashboard loads at http://localhost:3000

API endpoints respond correctly

Quantum optimization returns valid results

ML predictions generate reasonable prices

System metrics show normal operation

Error logs are clean

ENVR11 System Ready for Production Deployment
Last Updated: $(date +"%Y-%m-%d")
