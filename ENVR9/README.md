# ENVR9 - Building Survey System

## GitHub Branch: ENVR9
Repository: https://github.com/shellworlds/ENVR/tree/ENVR9

## Installation
Clone repository
git clone -b ENVR9 https://github.com/shellworlds/ENVR.git
cd ENVR/ENVR9

Run system check
cd system_check && ./system_check.sh

Install and run
cd ../backend
pip install -r requirements_envr9.txt
npm install

Start services
python fastapi_server.py &
node server.js &

## API Endpoints
FastAPI: http://localhost:8000/docs
Node.js: http://localhost:3000
Go: http://localhost:8081

## Dashboard
Open frontend/dashboard.html in browser.
