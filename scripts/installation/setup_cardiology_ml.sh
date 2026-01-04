#!/bin/bash

# Cardiology ML System Setup Script
# Comprehensive installation for Ubuntu/Linux systems

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_warning "This script requires root privileges for some operations."
        log_warning "Please run with sudo or as root."
        read -p "Continue with current user? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Detect OS and package manager
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        log_info "Detected OS: $OS $VER"
        
        case $ID in
            ubuntu|debian)
                PKG_MANAGER="apt-get"
                INSTALL_CMD="sudo $PKG_MANAGER install -y"
                UPDATE_CMD="sudo $PKG_MANAGER update"
                ;;
            fedora|centos|rhel)
                PKG_MANAGER="yum"
                INSTALL_CMD="sudo $PKG_MANAGER install -y"
                UPDATE_CMD="sudo $PKG_MANAGER update"
                ;;
            arch)
                PKG_MANAGER="pacman"
                INSTALL_CMD="sudo $PKG_MANAGER -S --noconfirm"
                UPDATE_CMD="sudo $PKG_MANAGER -Syu --noconfirm"
                ;;
            *)
                log_error "Unsupported OS: $ID"
                exit 1
                ;;
        esac
    else
        log_error "Cannot detect OS"
        exit 1
    fi
}

# Check system requirements
check_system_requirements() {
    log_info "Checking system requirements..."
    
    # Check RAM
    RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    RAM_GB=$((RAM_KB / 1024 / 1024))
    if [ $RAM_GB -lt 16 ]; then
        log_warning "Recommended RAM: 32GB, Detected: ${RAM_GB}GB"
    else
        log_success "RAM: ${RAM_GB}GB ✓"
    fi
    
    # Check storage
    STORAGE_GB=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ $STORAGE_GB -lt 100 ]; then
        log_warning "Low storage space: ${STORAGE_GB}GB free"
    else
        log_success "Storage: ${STORAGE_GB}GB free ✓"
    fi
    
    # Check CPU cores
    CPU_CORES=$(nproc)
    if [ $CPU_CORES -lt 4 ]; then
        log_warning "Limited CPU cores: $CPU_CORES"
    else
        log_success "CPU cores: $CPU_CORES ✓"
    fi
}

# Update system packages
update_system() {
    log_info "Updating system packages..."
    $UPDATE_CMD
    log_success "System updated"
}

# Install Python and dependencies
install_python() {
    log_info "Installing Python and scientific computing packages..."
    
    # Install Python 3.13
    $INSTALL_CMD python3.13 python3.13-dev python3.13-venv python3-pip
    
    # Create virtual environment
    python3.13 -m venv ~/cardiology_ml_venv
    source ~/cardiology_ml_venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    # Install core Python packages
    pip install numpy==1.26.0
    pip install pandas==2.1.3
    pip install scipy==1.11.3
    pip install matplotlib==3.8.0
    pip install scikit-learn==1.3.2
    pip install tensorflow==2.15.0
    pip install torch==2.1.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    pip install biosppy==0.6.1
    pip install neurokit2==0.2.4
    pip install wfdb==4.1.0
    pip install pyedflib==0.1.29
    pip install flask==3.0.0
    pip install fastapi==0.104.1
    pip install uvicorn==0.24.0
    pip install pydantic==2.5.0
    pip install sqlalchemy==2.0.23
    pip install redis==5.0.1
    pip install celery==5.3.4
    pip install plotly==5.18.0
    pip install dash==2.14.2
    pip install streamlit==1.28.0
    pip install jupyter==1.0.0
    pip install jupyterlab==4.0.10
    pip install black==23.11.0
    pip install flake8==6.1.0
    pip install pytest==7.4.3
    pip install pytest-cov==4.1.0
    
    log_success "Python environment setup complete"
}

# Install Node.js and dependencies
install_nodejs() {
    log_info "Installing Node.js and React dependencies..."
    
    # Install Node.js 20.x
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    $INSTALL_CMD nodejs
    
    # Install npm packages globally
    npm install -g npm@latest
    npm install -g create-react-app
    npm install -g vite
    npm install -g next@latest
    npm install -g typescript
    npm install -g eslint
    npm install -g prettier
    npm install -g nodemon
    npm install -g pm2
    
    # Install project-specific npm packages
    cd ~/cardiology_ml_app/ENVR
    npm init -y
    
    # Frontend dependencies
    npm install react@latest react-dom@latest
    npm install @types/react @types/react-dom
    npm install d3@latest
    npm install chart.js@latest
    npm install recharts@latest
    npm install victory@latest
    npm install @mui/material @emotion/react @emotion/styled
    npm install @mui/x-charts
    npm install axios
    npm install websocket
    npm install react-query
    npm install zustand
    npm install react-router-dom
    npm install react-hook-form
    
    # Backend dependencies
    npm install express
    npm install cors
    npm install body-parser
    npm install multer
    npm install jsonwebtoken
    npm install bcryptjs
    npm install mongoose
    npm install socket.io
    npm install ws
    npm install moment
    npm install uuid
    
    log_success "Node.js environment setup complete"
}

# Install C++ build tools
install_cpp_tools() {
    log_info "Installing C++ development tools..."
    
    $INSTALL_CMD build-essential
    $INSTALL_CMD gcc-13 g++-13
    $INSTALL_CMD cmake
    $INSTALL_CMD make
    $INSTALL_CMD libboost-all-dev
    $INSTALL_CMD libeigen3-dev
    $INSTALL_CMD libfftw3-dev
    $INSTALL_CMD libopenblas-dev
    $INSTALL_CMD liblapack-dev
    $INSTALL_CMD libarmadillo-dev
    $INSTALL_CMD libhdf5-dev
    $INSTALL_CMD libmatio-dev
    $INSTALL_CMD openmpi-bin libopenmpi-dev
    
    log_success "C++ development tools installed"
}

# Install Go language
install_go() {
    log_info "Installing Go language..."
    
    # Download and install Go
    GO_VERSION="1.21.3"
    ARCH=$(uname -m)
    
    if [ "$ARCH" = "x86_64" ]; then
        ARCH="amd64"
    elif [ "$ARCH" = "aarch64" ]; then
        ARCH="arm64"
    fi
    
    wget https://go.dev/dl/go${GO_VERSION}.linux-${ARCH}.tar.gz
    sudo tar -C /usr/local -xzf go${GO_VERSION}.linux-${ARCH}.tar.gz
    rm go${GO_VERSION}.linux-${ARCH}.tar.gz
    
    # Add Go to PATH
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    echo 'export GOPATH=$HOME/go' >> ~/.bashrc
    echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc
    source ~/.bashrc
    
    # Install Go packages
    go install github.com/gorilla/websocket@latest
    go install github.com/lib/pq@latest
    go install github.com/jinzhu/gorm@latest
    go install github.com/gin-gonic/gin@latest
    go install github.com/spf13/viper@latest
    go install github.com/sirupsen/logrus@latest
    go install github.com/stretchr/testify@latest
    
    log_success "Go language installed"
}

# Install database systems
install_databases() {
    log_info "Installing database systems..."
    
    # Install PostgreSQL
    $INSTALL_CMD postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    
    # Install Redis
    $INSTALL_CMD redis-server
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    
    # Install MongoDB
    wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
    $UPDATE_CMD
    $INSTALL_CMD mongodb-org
    sudo systemctl start mongod
    sudo systemctl enable mongod
    
    log_success "Database systems installed"
}

# Install additional tools
install_additional_tools() {
    log_info "Installing additional development tools..."
    
    # Install Git
    $INSTALL_CMD git git-lfs
    
    # Install Docker
    $INSTALL_CMD docker.io docker-compose
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    
    # Install VS Code (optional)
    read -p "Install Visual Studio Code? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
        sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
        sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
        rm -f packages.microsoft.gpg
        $UPDATE_CMD
        $INSTALL_CMD code
    fi
    
    # Install Jupyter Lab
    $INSTALL_CMD jupyter-lab
    
    # Install system monitoring tools
    $INSTALL_CMD htop glances screen tmux
    
    log_success "Additional tools installed"
}

# Install ECG-specific libraries
install_ecg_libraries() {
    log_info "Installing ECG-specific libraries and tools..."
    
    # Install WFDB (Waveform Database) toolkit
    $INSTALL_CMD libwfdb-dev wfdb
    
    # Install BioSig toolkit
    $INSTALL_CMD biosig-tools
    
    # Install EDFlib for EDF/BDF file support
    $INSTALL_CMD libedflib-dev
    
    # Install additional scientific libraries
    $INSTALL_CMD libatlas-base-dev libsuitesparse-dev
    
    # Install OpenCV for image processing (for ECG image analysis)
    $INSTALL_CMD libopencv-dev python3-opencv
    
    log_success "ECG-specific libraries installed"
}

# Configure system settings
configure_system() {
    log_info "Configuring system settings for optimal performance..."
    
    # Increase file watcher limit (for Node.js development)
    echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
    sudo sysctl -p
    
    # Increase max memory for Node.js
    NODE_OPTIONS="--max-old-space-size=8192"
    echo "export NODE_OPTIONS=\"$NODE_OPTIONS\"" >> ~/.bashrc
    
    # Configure swap if needed
    SWAP_SIZE="8G"
    if [ $(free | grep -i swap | awk '{print $2}') -eq 0 ]; then
        log_info "Creating swap file..."
        sudo fallocate -l $SWAP_SIZE /swapfile
        sudo chmod 600 /swapfile
        sudo mkswap /swapfile
        sudo swapon /swapfile
        echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    fi
    
    # Configure kernel parameters for better performance
    echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
    echo "vm.vfs_cache_pressure=50" | sudo tee -a /etc/sysctl.conf
    sudo sysctl -p
    
    log_success "System configuration optimized"
}

# Set up project structure
setup_project() {
    log_info "Setting up project structure..."
    
    # Create project directories
    mkdir -p ~/cardiology_ml_app/{data,models,notebooks,reports,exports}
    mkdir -p ~/cardiology_ml_app/data/{ecg,patients,annotations}
    mkdir -p ~/cardiology_ml_app/models/{ecg_analysis,risk_prediction,anomaly_detection}
    mkdir -p ~/cardiology_ml_app/notebooks/{exploratory,analysis,prototyping}
    mkdir -p ~/cardiology_ml_app/reports/{daily,weekly,clinical}
    mkdir -p ~/cardiology_ml_app/exports/{csv,images,pdf}
    
    # Create configuration files
    cat > ~/cardiology_ml_app/config.yaml << 'CONFIG'
# Cardiology ML System Configuration
system:
  name: "Cardiology ML Assessment Platform"
  version: "1.0.0"
  environment: "development"

database:
  postgres:
    host: "localhost"
    port: 5432
    name: "cardiology_ml"
    user: "cardio_user"
    password: "secure_password"
  redis:
    host: "localhost"
    port: 6379
  mongodb:
    uri: "mongodb://localhost:27017/cardiology_ml"

api:
  port: 8000
  host: "0.0.0.0"
  cors_origins: ["http://localhost:3000", "http://localhost:5173"]
  rate_limit: 1000

ecg_processing:
  default_sampling_rate: 500
  industry_standard: "AHA/ACC"
  qrs_detection_algorithm: "Pan-Tompkins"
  metrics_calculation: true

ml_models:
  ecg_classification:
    framework: "TensorFlow/PyTorch"
    input_shape: [5000, 12]
    output_classes: 5
  risk_prediction:
    framework: "Scikit-learn"
    features: ["age", "hr", "qtc", "st_elevation"]
    target: "risk_score"

logging:
  level: "INFO"
  file: "logs/cardiology_ml.log"
  rotation: "daily"
  retention: "30 days"

monitoring:
  prometheus_enabled: true
  grafana_enabled: true
  health_check_interval: 30

security:
  jwt_secret: "change_this_in_production"
  encryption_key: "32_byte_key_here"
  ssl_enabled: false
CONFIG

    # Create environment file
    cat > ~/cardiology_ml_app/.env << 'ENV'
# Environment Variables for Cardiology ML System
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://cardio_user:secure_password@localhost:5432/cardiology_ml
REDIS_URL=redis://localhost:6379
MONGODB_URI=mongodb://localhost:27017/cardiology_ml
JWT_SECRET=your_jwt_secret_key_here
API_KEY=your_api_key_here
ENV

    # Create README
    cat > ~/cardiology_ml_app/README.md << 'README'
# Cardiology ML Assessment System

## Overview
Advanced machine learning system for cardiology assessment with ECG analysis, visualization, and industry-standard indicators.

## System Architecture
- **Backend**: Python FastAPI, Node.js Express, Go
- **Frontend**: React, Next.js, D3.js
- **Database**: PostgreSQL, MongoDB, Redis
- **ML**: TensorFlow, PyTorch, Scikit-learn
- **Processing**: C++ for high-performance ECG analysis

## Prerequisites
- Ubuntu 20.04/22.04 or compatible
- 32GB RAM recommended
- 1TB SSD storage
- Python 3.13, Node.js 20+, Go 1.21+

## Installation
1. Clone the repository
2. Run setup script: `./scripts/installation/setup_cardiology_ml.sh`
3. Configure environment variables
4. Start services: `./scripts/deployment/start_services.sh`

## Features
- Real-time ECG signal processing
- Multi-lead ECG visualization
- Arrhythmia detection
- ST-segment analysis
- QT interval measurement
- Industry standard compliance checking
- Patient risk assessment
- Clinical report generation

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Monitoring
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001
- Health checks: http://localhost:8000/health

## Development
```bash
# Activate virtual environment
source ~/cardiology_ml_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
npm install

# Run development servers
python src/python/api_server.py
npm run dev
License
Proprietary - Cardiology ML System
README

text
log_success "Project structure created"
}

Create startup scripts
create_startup_scripts() {
log_info "Creating startup and management scripts..."

text
# Create service management script
cat > ~/cardiology_ml_app/scripts/deployment/start_services.sh << 'STARTUP'
#!/bin/bash

Cardiology ML Services Management Script
set -e

SERVICES_DIR="$HOME/cardiology_ml_app"
VENV_PATH="$HOME/cardiology_ml_venv"
LOG_DIR="$SERVICES_DIR/logs"

Create log directory
mkdir -p $LOG_DIR

Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

Log function
log() {
echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
echo -e "${RED}[ERROR]${NC} $1"
}

warning() {
echo -e "${YELLOW}[WARNING]${NC} $1"
}

Check if services are running
check_service() {
local service_name=$1
local pid_file=$2

text
if [ -f "$pid_file" ]; then
    local pid=$(cat "$pid_file")
    if ps -p $pid > /dev/null 2>&1; then
        return 0
    else
        rm -f "$pid_file"
        return 1
    fi
fi
return 1
}

Start PostgreSQL
start_postgresql() {
log "Starting PostgreSQL..."
sudo systemctl start postgresql
sleep 2
if sudo systemctl is-active --quiet postgresql; then
log "PostgreSQL started successfully"
else
error "Failed to start PostgreSQL"
exit 1
fi
}

Start Redis
start_redis() {
log "Starting Redis..."
sudo systemctl start redis-server
sleep 1
if sudo systemctl is-active --quiet redis-server; then
log "Redis started successfully"
else
error "Failed to start Redis"
exit 1
fi
}

Start MongoDB
start_mongodb() {
log "Starting MongoDB..."
sudo systemctl start mongod
sleep 2
if sudo systemctl is-active --quiet mongod; then
log "MongoDB started successfully"
else
warning "MongoDB failed to start (may not be installed)"
fi
}

Start Python API server
start_python_api() {
log "Starting Python FastAPI server..."
cd $SERVICES_DIR
source $VENV_PATH/bin/activate

text
# Kill existing process if any
if check_service "python_api" "$SERVICES_DIR/pids/python_api.pid"; then
    warning "Python API is already running"
    return
fi

nohup uvicorn src.python.api_server:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info \
    > $LOG_DIR/python_api.log 2>&1 &

echo $! > $SERVICES_DIR/pids/python_api.pid
sleep 3
log "Python API server started on port 8000"
}

Start Node.js server
start_node_server() {
log "Starting Node.js server..."
cd $SERVICES_DIR

text
if check_service "node_server" "$SERVICES_DIR/pids/node_server.pid"; then
    warning "Node.js server is already running"
    return
fi

nohup node src/node/ecg_api_server.js \
    > $LOG_DIR/node_server.log 2>&1 &

echo $! > $SERVICES_DIR/pids/node_server.pid
sleep 3
log "Node.js server started on port 3000"
}

Start Go service
start_go_service() {
log "Starting Go streaming service..."
cd $SERVICES_DIR/src/go

text
if check_service "go_service" "$SERVICES_DIR/pids/go_service.pid"; then
    warning "Go service is already running"
    return
fi

nohup go run ecg_stream_service.go \
    > $LOG_DIR/go_service.log 2>&1 &

echo $! > $SERVICES_DIR/pids/go_service.pid
sleep 2
log "Go service started on port 8080"
}

Start React development server
start_react_dev() {
log "Starting React development server..."
cd $SERVICES_DIR/src/react

text
if check_service "react_dev" "$SERVICES_DIR/pids/react_dev.pid"; then
    warning "React dev server is already running"
    return
fi

nohup npm start \
    > $LOG_DIR/react_dev.log 2>&1 &

echo $! > $SERVICES_DIR/pids/react_dev.pid
sleep 5
log "React dev server started on port 5173"
}

Start Jupyter Lab
start_jupyter() {
log "Starting Jupyter Lab..."
cd $SERVICES_DIR
source $VENV_PATH/bin/activate

text
if check_service "jupyter" "$SERVICES_DIR/pids/jupyter.pid"; then
    warning "Jupyter Lab is already running"
    return
fi

nohup jupyter lab \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --notebook-dir=$SERVICES_DIR/notebooks \
    > $LOG_DIR/jupyter.log 2>&1 &

echo $! > $SERVICES_DIR/pids/jupyter.pid
sleep 3
log "Jupyter Lab started on port 8888"
}

Start monitoring services
start_monitoring() {
log "Starting monitoring services..."

text
# Start Prometheus if installed
if command -v prometheus &> /dev/null; then
    nohup prometheus \
        --config.file=$SERVICES_DIR/monitoring/prometheus.yml \
        --storage.tsdb.path=$SERVICES_DIR/monitoring/data \
        > $LOG_DIR/prometheus.log 2>&1 &
    echo $! > $SERVICES_DIR/pids/prometheus.pid
    log "Prometheus started on port 9090"
fi

# Start Grafana if installed
if command -v grafana-server &> /dev/null; then
    nohup grafana-server \
        --homepath /usr/share/grafana \
        > $LOG_DIR/grafana.log 2>&1 &
    echo $! > $SERVICES_DIR/pids/grafana.pid
    log "Grafana started on port 3001"
fi
}

Display service status
display_status() {
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║ Cardiology ML Services Status ║"
echo "╠══════════════════════════════════════════════════════════╣"

text
services=(
    "PostgreSQL:5432"
    "Redis:6379"
    "MongoDB:27017"
    "Python API:8000"
    "Node.js API:3000"
    "Go Service:8080"
    "React Dev:5173"
    "Jupyter Lab:8888"
)

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    if nc -z localhost $port 2>/dev/null; then
        echo "║  ✓ $name (localhost:$port)                    "
    else
        echo "║  ✗ $name (localhost:$port)                    "
    fi
done

echo "╠══════════════════════════════════════════════════════════╣"
echo "║     Access URLs:                                        ║"
echo "║     • Python API Docs: http://localhost:8000/docs       ║"
echo "║     • React App: http://localhost:5173                  ║"
echo "║     • Jupyter Lab: http://localhost:8888                ║"
echo "║     • Node.js API: http://localhost:3000                ║"
echo "║     • Go Service: http://localhost:8080                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
}

Main execution
main() {
log "Starting Cardiology ML Services..."

text
# Create PID directory
mkdir -p $SERVICES_DIR/pids

# Start database services
start_postgresql
start_redis
start_mongodb

# Start application services
start_python_api
start_node_server
start_go_service
start_react_dev
start_jupyter

# Start monitoring
start_monitoring

# Display status
display_status

log "All services started successfully!"
log "Logs are available in: $LOG_DIR"
}

Handle command line arguments
case "$1" in
start)
main
;;
stop)
# Stop all services
log "Stopping all services..."
for pid_file in $SERVICES_DIR/pids/*.pid; do
if [ -f "$pid_file" ]; then
pid=$(cat "$pid_file")
kill $pid 2>/dev/null && rm -f "$pid_file"
fi
done
log "All services stopped"
;;
restart)
$0 stop
sleep 2
$0 start
;;
status)
display_status
;;
*)
echo "Usage: $0 {start|stop|restart|status}"
exit 1
;;
esac
STARTUP

text
chmod +x ~/cardiology_ml_app/scripts/deployment/start_services.sh

# Create monitoring script
cat > ~/cardiology_ml_app/scripts/deployment/monitor_services.sh << 'MONITOR'
#!/bin/bash

Cardiology ML Services Monitoring Script
set -e

SERVICES_DIR="$HOME/cardiology_ml_app"
LOG_DIR="$SERVICES_DIR/logs"

Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

Function to check port
check_port() {
local port=$1
nc -z localhost $port 2>/dev/null
return $?
}

Function to get service status
get_service_status() {
local service_name=$1
local port=$2
local pid_file="$SERVICES_DIR/pids/${service_name}.pid"

text
if [ -f "$pid_file" ]; then
    local pid=$(cat "$pid_file")
    if ps -p $pid > /dev/null 2>&1; then
        if check_port $port; then
            echo -e "${GREEN}RUNNING${NC}"
        else
            echo -e "${YELLOW}PID_EXISTS${NC}"
        fi
    else
        echo -e "${RED}DEAD${NC}"
    fi
else
    if check_port $port; then
        echo -e "${GREEN}RUNNING${NC}"
    else
        echo -e "${RED}STOPPED${NC}"
    fi
fi
}

Function to check resource usage
check_resources() {
echo ""
echo "System Resources:"
echo "-----------------"

text
# CPU usage
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
echo "CPU Usage: ${cpu_usage}%"

# Memory usage
mem_total=$(free -h | grep Mem | awk '{print $2}')
mem_used=$(free -h | grep Mem | awk '{print $3}')
mem_percent=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
echo "Memory: ${mem_used}/${mem_total} (${mem_percent%.*}%)"

# Disk usage
disk_usage=$(df -h / | awk 'NR==2 {print $5}')
echo "Disk Usage: $disk_usage"

# Network connections
connections=$(netstat -an | grep ESTABLISHED | wc -l)
echo "Active Connections: $connections"
}

Function to check service health
check_service_health() {
local service_name=$1
local port=$2
local health_endpoint=$3

text
if check_port $port; then
    if [ -n "$health_endpoint" ]; then
        if curl -s "http://localhost:$port$health_endpoint" > /dev/null; then
            echo -e "${GREEN}HEALTHY${NC}"
        else
            echo -e "${YELLOW}UNHEALTHY${NC}"
        fi
    else
        echo -e "${GREEN}UP${NC}"
    fi
else
    echo -e "${RED}DOWN${NC}"
fi
}

Main monitoring function
monitor_services() {
clear
echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║ CARDIOLOGY ML SERVICES MONITOR ║"
echo "╠══════════════════════════════════════════════════════════════════════╣"
echo "║ Service Port Status Health PID ║"
echo "╠══════════════════════════════════════════════════════════════════════╣"

text
# Define services to monitor
services=(
    "PostgreSQL:5432::"
    "Redis:6379::"
    "MongoDB:27017::"
    "Python API:8000:/health"
    "Node.js API:3000:/api/health"
    "Go Service:8080:/"
    "React Dev:5173::"
    "Jupyter Lab:8888::"
)

for service_info in "${services[@]}"; do
    name=$(echo $service_info | cut -d: -f1)
    port=$(echo $service_info | cut -d: -f2)
    health_endpoint=$(echo $service_info | cut -d: -f3)
    
    # Get PID if exists
    pid_file="$SERVICES_DIR/pids/${name,,}.pid"
    pid="N/A"
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ! ps -p $pid > /dev/null 2>&1; then
            pid="DEAD"
        fi
    fi
    
    status=$(get_service_status ${name,,} $port)
    health=$(check_service_health "$name" "$port" "$health_endpoint")
    
    printf "║ %-17s %-6s %-14s %-12s %-12s \n" "$name" "$port" "$status" "$health" "$pid"
done

echo "╠══════════════════════════════════════════════════════════════════════╣"

# Display recent logs
echo "║ Recent Errors (last 10):                                           ║"
echo "╠══════════════════════════════════════════════════════════════════════╣"

error_count=0
for log_file in $LOG_DIR/*.log; do
    if [ -f "$log_file" ]; then
        errors=$(grep -i "error\|fail\|exception" "$log_file" | tail -5)
        if [ -n "$errors" ]; then
            echo "║ $(basename $log_file):"
            while IFS= read -r line; do
                if [ ${#line} -gt 70 ]; then
                    line="${line:0:67}..."
                fi
                echo "║   $line"
                ((error_count++))
                if [ $error_count -ge 10 ]; then
                    break 2
                fi
            done <<< "$errors"
        fi
    fi
done

if [ $error_count -eq 0 ]; then
    echo "║ No errors found in recent logs.                                   ║"
fi

echo "╠══════════════════════════════════════════════════════════════════════╣"

# Check resources
check_resources | while read -r line; do
    echo "║ $line"
done

echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Last Updated: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Press Ctrl+C to exit"
}

Continuous monitoring
if [ "$1" = "continuous" ]; then
while true; do
monitor_services
sleep 5
done
else
monitor_services
fi
MONITOR

text
chmod +x ~/cardiology_ml_app/scripts/deployment/monitor_services.sh

# Create backup script
cat > ~/cardiology_ml_app/scripts/deployment/backup_system.sh << 'BACKUP'
#!/bin/bash

Cardiology ML System Backup Script
set -e

BACKUP_DIR="$HOME/cardiology_ml_backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/backup_$DATE"

Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log() {
echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
echo -e "${RED}[ERROR]${NC} $1"
}

Create backup directory
mkdir -p $BACKUP_PATH

log "Starting Cardiology ML System Backup..."

Backup PostgreSQL databases
log "Backing up PostgreSQL databases..."
sudo -u postgres pg_dumpall > $BACKUP_PATH/postgres_backup.sql 2>/dev/null || {
error "Failed to backup PostgreSQL"
}

Backup MongoDB
log "Backing up MongoDB..."
mongodump --out $BACKUP_PATH/mongodb_backup 2>/dev/null || {
error "Failed to backup MongoDB (may not be installed)"
}

Backup Redis
log "Backing up Redis..."
redis-cli SAVE > /dev/null 2>&1
cp /var/lib/redis/dump.rdb $BACKUP_PATH/redis_backup.rdb 2>/dev/null || {
error "Failed to backup Redis"
}

Backup application data
log "Backing up application data..."
cp -r ~/cardiology_ml_app/data $BACKUP_PATH/
cp -r ~/cardiology_ml_app/models $BACKUP_PATH/
cp -r ~/cardiology_ml_app/reports $BACKUP_PATH/

Backup configuration
log "Backing up configuration..."
cp ~/cardiology_ml_app/config.yaml $BACKUP_PATH/
cp ~/cardiology_ml_app/.env $BACKUP_PATH/

Backup source code (excluding large files)
log "Backing up source code..."
find ~/cardiology_ml_app -type f 
−
n
a
m
e
"
∗
.
p
y
"
−
o
−
n
a
m
e
"
∗
.
j
s
"
−
o
−
n
a
m
e
"
∗
.
j
s
x
"
−
o
−
n
a
m
e
"
∗
.
t
s
"
−
o
−
n
a
m
e
"
∗
.
t
s
x
"
−
o
−
n
a
m
e
"
∗
.
c
p
p
"
−
o
−
n
a
m
e
"
∗
.
g
o
"
−
o
−
n
a
m
e
"
∗
.
s
h
"
−
o
−
n
a
m
e
"
∗
.
m
d
"
−
o
−
n
a
m
e
"
∗
.
y
a
m
l
"
−
o
−
n
a
m
e
"
∗
.
y
m
l
"
−
o
−
n
a
m
e
"
∗
.
j
s
o
n
"
−name"∗.py"−o−name"∗.js"−o−name"∗.jsx"−o−name"∗.ts"−o−name"∗.tsx"−o−name"∗.cpp"−o−name"∗.go"−o−name"∗.sh"−o−name"∗.md"−o−name"∗.yaml"−o−name"∗.yml"−o−name"∗.json" -exec cp --parents {} $BACKUP_PATH/ ; 2>/dev/null

Create backup manifest
log "Creating backup manifest..."
cat > $BACKUP_PATH/manifest.txt << MANIFEST
Cardiology ML System Backup
Date: $(date)
Backup ID: $DATE

Contents:

PostgreSQL database dump

MongoDB backup

Redis RDB file

Application data

Trained models

Reports

Configuration files

Source code

Total size: $(du -sh $BACKUP_PATH | cut -f1)

Restore Instructions:

Stop all services

Restore PostgreSQL: psql -f postgres_backup.sql

Restore MongoDB: mongorestore --dir mongodb_backup/

Restore Redis: cp redis_backup.rdb /var/lib/redis/dump.rdb

Restore application data: cp -r data/ models/ reports/ ~/cardiology_ml_app/

Restore configuration: cp config.yaml .env ~/cardiology_ml_app/

Start services

MANIFEST

Compress backup
log "Compressing backup..."
tar -czf $BACKUP_PATH.tar.gz -C $BACKUP_DIR backup_$DATE
rm -rf $BACKUP_PATH

Remove old backups (keep last 7 days)
log "Cleaning up old backups..."
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete

log "Backup completed successfully: $BACKUP_PATH.tar.gz"
log "Backup size: $(du -h $BACKUP_PATH.tar.gz | cut -f1)"

Create restore script
cat > $BACKUP_DIR/restore_backup.sh << 'RESTORE'
#!/bin/bash

Cardiology ML System Restore Script
set -e

BACKUP_DIR="$HOME/cardiology_ml_backups"

if [ -z "$1" ]; then
echo "Usage: $0 <backup_file.tar.gz>"
echo "Available backups:"
ls -lh $BACKUP_DIR/backup_*.tar.gz 2>/dev/null || echo "No backups found"
exit 1
fi

BACKUP_FILE="$1"
RESTORE_DIR="/tmp/restore_$(date +%s)"

if [ ! -f "$BACKUP_FILE" ]; then
echo "Backup file not found: $BACKUP_FILE"
exit 1
fi

echo "Starting restore from: $BACKUP_FILE"
echo "WARNING: This will overwrite existing data!"
read -p "Are you sure? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
exit 1
fi

Extract backup
mkdir -p $RESTORE_DIR
tar -xzf "$BACKUP_FILE" -C $RESTORE_DIR

Stop services
echo "Stopping services..."
sudo systemctl stop postgresql
sudo systemctl stop redis-server
sudo systemctl stop mongod

Restore PostgreSQL
echo "Restoring PostgreSQL..."
sudo -u postgres psql -f $RESTORE_DIR/backup_*/postgres_backup.sql

Restore MongoDB
if [ -d "$RESTORE_DIR/backup_/mongodb_backup" ]; then
echo "Restoring MongoDB..."
mongorestore --dir $RESTORE_DIR/backup_/mongodb_backup/
fi

Restore Redis
echo "Restoring Redis..."
sudo cp $RESTORE_DIR/backup_*/redis_backup.rdb /var/lib/redis/dump.rdb
sudo chown redis:redis /var/lib/redis/dump.rdb

Restore application data
echo "Restoring application data..."
cp -r $RESTORE_DIR/backup_/data ~/cardiology_ml_app/
cp -r $RESTORE_DIR/backup_/models ~/cardiology_ml_app/
cp -r $RESTORE_DIR/backup_*/reports ~/cardiology_ml_app/

Restore configuration
echo "Restoring configuration..."
cp $RESTORE_DIR/backup_/config.yaml ~/cardiology_ml_app/
cp $RESTORE_DIR/backup_/.env ~/cardiology_ml_app/

Start services
echo "Starting services..."
sudo systemctl start postgresql
sudo systemctl start redis-server
sudo systemctl start mongod

Cleanup
rm -rf $RESTORE_DIR

echo "Restore completed successfully!"
echo "Please restart application services manually."
RESTORE

chmod +x $BACKUP_DIR/restore_backup.sh

log "Restore script created: $BACKUP_DIR/restore_backup.sh"
BACKUP

text
chmod +x ~/cardiology_ml_app/scripts/deployment/backup_system.sh

log_success "Startup and management scripts created"
}

Test installations
test_installations() {
log_info "Testing installations..."

text
# Test Python
python3.13 --version
if [ $? -eq 0 ]; then
    log_success "Python 3.13 installed successfully"
else
    log_error "Python installation failed"
fi

# Test Node.js
node --version
if [ $? -eq 0 ]; then
    log_success "Node.js installed successfully"
else
    log_error "Node.js installation failed"
fi

# Test Go
go version
if [ $? -eq 0 ]; then
    log_success "Go installed successfully"
else
    log_error "Go installation failed"
fi

# Test C++ compiler
g++-13 --version
if [ $? -eq 0 ]; then
    log_success "C++ compiler installed successfully"
else
    log_error "C++ compiler installation failed"
fi

# Test PostgreSQL
sudo systemctl status postgresql --no-pager | grep -q "active"
if [ $? -eq 0 ]; then
    log_success "PostgreSQL installed and running"
else
    log_error "PostgreSQL installation failed"
fi

# Test Redis
sudo systemctl status redis-server --no-pager | grep -q "active"
if [ $? -eq 0 ]; then
    log_success "Redis installed and running"
else
    log_error "Redis installation failed"
fi
}

Main installation function
main_installation() {
log_info "Starting Cardiology ML System Installation..."
echo ""

text
# Check system
check_root
detect_os
check_system_requirements

# Update system
update_system

# Install components
install_python
install_nodejs
install_cpp_tools
install_go
install_databases
install_additional_tools
install_ecg_libraries

# Configure system
configure_system

# Setup project
setup_project
create_startup_scripts

# Test installations
test_installations

echo ""
log_success "╔══════════════════════════════════════════════════════════╗"
log_success "║     Cardiology ML System Installation Complete!         ║"
log_success "╠══════════════════════════════════════════════════════════╣"
log_success "║                                                          ║"
log_success "║  Next Steps:                                            ║"
log_success "║  1. Activate virtual environment:                       ║"
log_success "║     source ~/cardiology_ml_venv/bin/activate            ║"
log_success "║  2. Navigate to project:                                ║"
log_success "║     cd ~/cardiology_ml_app                              ║"
log_success "║  3. Start all services:                                 ║"
log_success "║     ./scripts/deployment/start_services.sh start        ║"
log_success "║  4. Monitor services:                                   ║"
log_success "║     ./scripts/deployment/monitor_services.sh            ║"
log_success "║                                                          ║"
log_success "║  Access Points:                                         ║"
log_success "║  • API Documentation: http://localhost:8000/docs        ║"
log_success "║  • React Application: http://localhost:5173             ║"
log_success "║  • Jupyter Lab: http://localhost:8888                   ║"
log_success "║                                                          ║"
log_success "║  Backup System:                                         ║"
log_success "║  ./scripts/deployment/backup_system.sh                  ║"
log_success "╚══════════════════════════════════════════════════════════╝"
echo ""

# Display system information
log_info "System Information:"
echo "OS: $OS $VER"
echo "CPU: $(nproc) cores"
echo "RAM: $(free -h | grep Mem | awk '{print $2}')"
echo "Storage: $(df -h / | awk 'NR==2 {print $4}') free"
echo "Installation Date: $(date)"
echo "Installation Log: ~/cardiology_ml_install.log"
}

Execute main installation
main_installation 2>&1 | tee ~/cardiology_ml_install.log
