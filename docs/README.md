# ENVR9 Building Survey System

## Overview
Complete multi-language system for building surveying with 16 tools and 5 processes.

## Quick Start

### 1. System Check
cd system_check
./system_check.sh

### 2. Install Dependencies
cd ../backend
pip install -r requirements_envr9.txt
npm install

### 3. Start Services
# Python FastAPI (port 8000)
python fastapi_server.py &

# Node.js (port 3000)
node server.js &

# Go (port 8081)
go run survey_service.go &

### 4. Access Dashboard
Open ../frontend/dashboard.html in browser.

## 16 Tools
1. Python 3.13+
2. Node.js 20.19+
3. FastAPI
4. Go 1.21+
5. C++17
6. Docker
7. PostgreSQL
8. Redis
9. OpenCV
10. Git
11. NPM
12. CMake
13. Pip
14. Shell Script
15. HTML5/CSS3/JS
16. Grafana

## 5 Processes
1. System Verification
2. Data Collection
3. 3D Modeling
4. Report Generation
5. Quality Assurance
