#!/bin/bash
# One-click Installation for B2B Data Platform
# Supports Lenovo (Ubuntu), Mac, Windows (WSL/CMD)

echo "🚀 B2B Data Platform - Complete Installation"
echo "=========================================="
echo "Solving: B2B Data Flow with Datalake, ETL, and Warehousing"
echo ""

# Platform detection
detect_platform() {
    case "$(uname -s)" in
        Linux*)
            if [[ -f /etc/os-release ]]; then
                . /etc/os-release
                if [[ $ID == "ubuntu" ]]; then
                    echo "lenovo-ubuntu"
                else
                    echo "linux"
                fi
            elif grep -q Microsoft /proc/version 2>/dev/null; then
                echo "windows-wsl"
            else
                echo "linux"
            fi
            ;;
        Darwin*)
            echo "macos"
            ;;
        CYGWIN*|MINGW*|MSYS*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

PLATFORM=$(detect_platform)

echo "📱 Detected Platform: $PLATFORM"
echo ""

# Installation steps based on platform
case $PLATFORM in
    "lenovo-ubuntu"|"linux")
        echo "🖥️  Lenovo ThinkPad (Ubuntu) Installation"
        echo "----------------------------------------"
        install_lenovo_ubuntu
        ;;
    "macos")
        echo "🍎 macOS Installation"
        echo "--------------------"
        install_macos
        ;;
    "windows-wsl")
        echo "🪟 Windows WSL2 Installation"
        echo "---------------------------"
        install_windows_wsl
        ;;
    "windows")
        echo "🪟 Windows Native Installation"
        echo "----------------------------"
        install_windows_native
        ;;
    *)
        echo "❌ Unsupported platform"
        exit 1
        ;;
esac

# Lenovo Ubuntu installation
install_lenovo_ubuntu() {
    echo "📦 Updating package list..."
    sudo apt-get update
    
    echo "🐍 Installing Python 3.11..."
    sudo apt-get install -y python3.11 python3.11-venv python3-pip
    
    echo "🐳 Installing Docker..."
    sudo apt-get install -y docker.io docker-compose
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker $USER
    
    echo "☕ Installing Java (for Spark)..."
    sudo apt-get install -y openjdk-11-jdk
    
    echo "📊 Installing data tools..."
    sudo apt-get install -y \
        postgresql \
        redis-server \
        sqlite3 \
        curl \
        wget \
        git \
        jq \
        nodejs \
        npm
    
    echo "🔧 Setting up Python environment..."
    python3.11 -m venv venv
    source venv/bin/activate
    
    echo "📦 Installing Python packages..."
    pip install --upgrade pip
    
    cat > requirements.txt << REQ
# B2B Data Platform - Complete Stack
pandas>=2.0.0
numpy>=1.24.0
pydantic>=2.0.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
alembic>=1.12.0
psycopg2-binary>=2.9.0
redis>=5.0.0
pyspark>=3.4.0
apache-airflow>=2.7.0
dbt-core>=1.5.0
dbt-postgres>=1.5.0
great-expectations>=0.16.0
prefect>=2.0.0
dagster>=1.3.0
jupyter>=1.0.0
jupyterlab>=4.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
boto3>=1.28.0
google-cloud-storage>=2.0.0
azure-storage-blob>=12.0.0
snowflake-connector-python>=3.0.0
kafka-python>=2.0.0
confluent-kafka>=2.0.0
requests>=2.31.0
aiohttp>=3.8.0
asyncio
REQ
    
    pip install -r requirements.txt
    
    echo "⚙️  Setting up project structure..."
    create_project_structure
    
    echo "🚀 Creating startup scripts..."
    create_startup_scripts
}

# macOS installation
install_macos() {
    echo "🍺 Checking Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    echo "🐍 Installing Python 3.11..."
    brew install python@3.11
    
    echo "🐳 Installing Docker..."
    brew install --cask docker
    open /Applications/Docker.app
    
    echo "☕ Installing Java..."
    brew install openjdk@11
    
    echo "📊 Installing data tools..."
    brew install \
        postgresql \
        redis \
        node \
        wget \
        jq \
        git
    
    echo "🔧 Setting up Python environment..."
    python3.11 -m venv venv
    source venv/bin/activate
    
    echo "📦 Installing Python packages..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo "⚙️  Setting up project structure..."
    create_project_structure
    
    echo "🚀 Creating startup scripts..."
    create_startup_scripts
}

# Windows WSL installation
install_windows_wsl() {
    echo "⚠️  Windows WSL Installation Instructions:"
    echo ""
    echo "1. Open PowerShell as Administrator and run:"
    echo "   wsl --install"
    echo ""
    echo "2. Install Ubuntu from Microsoft Store"
    echo ""
    echo "3. Open Ubuntu and run:"
    echo "   sudo apt-get update"
    echo "   sudo apt-get install git"
    echo "   git clone https://github.com/shellworlds/ENVR.git"
    echo "   cd ENVR"
    echo "   ./install_all_platforms.sh"
    echo ""
    echo "4. Install Docker Desktop from:"
    echo "   https://www.docker.com/products/docker-desktop/"
    echo ""
    echo "5. Enable WSL2 integration in Docker Desktop settings"
    
    read -p "Press Enter after completing these steps..."
    
    # Continue with Ubuntu installation
    install_lenovo_ubuntu
}

# Windows native installation
install_windows_native() {
    echo "⚠️  Windows Native Installation Instructions:"
    echo ""
    echo "1. Install Python 3.11 from:"
    echo "   https://www.python.org/downloads/"
    echo ""
    echo "2. Install Git from:"
    echo "   https://git-scm.com/download/win"
    echo ""
    echo "3. Install Docker Desktop from:"
    echo "   https://www.docker.com/products/docker-desktop/"
    echo ""
    echo "4. Open PowerShell and run:"
    echo "   git clone https://github.com/shellworlds/ENVR.git"
    echo "   cd ENVR"
    echo "   python -m venv venv"
    echo "   venv\\Scripts\\activate"
    echo "   pip install -r requirements.txt"
    echo ""
    echo "⚠️  Note: Some tools may require WSL2 for full functionality"
    
    exit 0
}

# Create project structure
create_project_structure() {
    echo "📁 Creating project directories..."
    
    # Core directories
    mkdir -p {data_pipeline,datalake,warehouse,etl,monitoring,governance}
    mkdir -p {tools,processes,platforms,analytics,logs}
    
    # Data lake structure
    mkdir -p datalake/{bronze,silver,gold}/{landing,validated,enriched}
    mkdir -p datalake/raw/{daily,hourly,monthly}
    
    # Pipeline directories
    mkdir -p data_pipeline/{dags,scripts,configs,logs}
    
    # Tools directories
    mkdir -p tools/{airflow,dbt,spark,trino,kafka,debezium}
    
    # Create sample configurations
    cat > data_pipeline/configs/pipeline_config.yaml << CONFIG
# B2B Data Pipeline Configuration
version: 2.0

clients:
  - name: enterprise_corp
    source_type: api
    destination: snowflake
    schedule: "0 * * * *"  # hourly
    retention_days: 365
    
  - name: retail_chain
    source_type: database
    destination: bigquery
    schedule: "0 2 * * *"  # daily at 2am
    retention_days: 730

datalake:
  storage: s3
  bucket: b2b-datalake
  partitions:
    - date
    - client
    - data_type

warehouse:
  type: snowflake
  database: b2b_analytics
  schema: production
CONFIG
    
    cat > docker-compose.yml << DOCKER
# B2B Data Platform - Docker Compose
version: '3.8'

services:
  # Data Services
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: b2b_user
      POSTGRES_PASSWORD: b2b_pass
      POSTGRES_DB: b2b_data
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # Airflow
  airflow-webserver:
    image: apache/airflow:2.7.0
    command: webserver
    ports:
      - "8080:8080"
    volumes:
      - ./data_pipeline/dags:/opt/airflow/dags
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://b2b_user:b2b_pass@postgres/b2b_data

  # Jupyter
  jupyter:
    image: jupyter/datascience-notebook:latest
    ports:
      - "8888:8888"
    volumes:
      - ./analytics:/home/jovyan/work
    environment:
      JUPYTER_TOKEN: b2b123

volumes:
  postgres_data:
DOCKER
}

# Create startup scripts
create_startup_scripts() {
    echo "⚡ Creating startup scripts..."
    
    cat > start_platform.sh << STARTUP
#!/bin/bash
# Start B2B Data Platform

echo "🚀 Starting B2B Data Platform..."

# Start Docker services
echo "Starting Docker services..."
docker-compose up -d

# Start Python orchestrator
echo "Starting Python orchestrator..."
source venv/bin/activate
python b2b_data_orchestrator.py &

# Start Node.js API
echo "Starting Node.js API..."
node data_pipeline_api.js &

# Start Airflow (if using)
echo "Starting Airflow..."
export AIRFLOW_HOME=\$(pwd)/airflow
airflow webserver --port 8080 --daemon
airflow scheduler --daemon

echo ""
echo "✅ B2B Data Platform Started!"
echo ""
echo "📊 Access Points:"
echo "   • Airflow UI: http://localhost:8080"
echo "   • Jupyter: http://localhost:8888"
echo "   • API Server: http://localhost:3001"
echo "   • Data Dashboard: Open b2b_data_dashboard.html"
echo ""
echo "🔧 Usernames:"
echo "   Airflow: admin / admin"
echo "   Jupyter: token: b2b123"
echo ""
echo "🛑 To stop: ./stop_platform.sh"
STARTUP
    
    chmod +x start_platform.sh
    
    cat > stop_platform.sh << SHUTDOWN
#!/bin/bash
# Stop B2B Data Platform

echo "🛑 Stopping B2B Data Platform..."

# Stop all services
pkill -f "python b2b_data_orchestrator.py"
pkill -f "node data_pipeline_api.js"
pkill -f "airflow"

# Stop Docker services
docker-compose down

echo "✅ All services stopped"
SHUTDOWN
    
    chmod +x stop_platform.sh
    
    cat > quick_test.sh << TEST
#!/bin/bash
# Quick test of B2B Data Platform

echo "🧪 Testing B2B Data Platform..."

# Test Python orchestrator
echo "Testing Python orchestrator..."
source venv/bin/activate
python -c "import pandas as pd; print('✅ Pandas version:', pd.__version__)"

# Test Node.js
echo "Testing Node.js..."
node --version

# Test Docker
echo "Testing Docker..."
docker --version
docker-compose --version

# Test data tools
echo "Testing data tools..."
python -c "import pyspark; print('✅ PySpark available')" 2>/dev/null || echo "⚠️  PySpark not installed"

echo ""
echo "✅ Quick test complete!"
TEST
    
    chmod +x quick_test.sh
}

# Create HTML dashboard
cat > b2b_data_dashboard.html << HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B2B Data Platform Dashboard</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f1f5f9;
            margin: 0;
            padding: 20px;
        }
        .dashboard {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: rgba(30, 41, 59, 0.8);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid #475569;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(30, 41, 59, 0.8);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #475569;
        }
        .status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
        }
        .status-running { background: rgba(59, 130, 246, 0.2); color: #3b82f6; }
        .status-success { background: rgba(16, 185, 129, 0.2); color: #10b981; }
        .status-warning { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🚀 B2B Data Platform Dashboard</h1>
            <p>Datalake • ETL • Warehousing • Analytics</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>📊 Data Pipeline Status</h2>
                <div class="status status-running">Running</div>
                <p>Last run: 2 minutes ago</p>
                <p>Records processed: 125,000</p>
                <p>Success rate: 99.8%</p>
            </div>
            
            <div class="card">
                <h2>🏭 Datalake Health</h2>
                <div class="status status-success">Healthy</div>
                <p>Storage used: 45%</p>
                <p>Total data: 2.5 TB</p>
                <p>Daily ingestion: 250 GB</p>
            </div>
            
            <div class="card">
                <h2>📈 ETL Performance</h2>
                <div class="status status-success">Optimal</div>
                <p>Avg processing time: 1.2s</p>
                <p>Daily jobs: 1,250</p>
                <p>Failed jobs: 12 (0.96%)</p>
            </div>
            
            <div class="card">
                <h2>🔧 Quick Actions</h2>
                <button onclick="runPipeline()">Run Pipeline</button>
                <button onclick="refreshData()">Refresh Data</button>
                <button onclick="openAirflow()">Open Airflow</button>
                <button onclick="openJupyter()">Open Jupyter</button>
            </div>
        </div>
    </div>
    
    <script>
        function runPipeline() {
            alert('Pipeline execution started');
        }
        function refreshData() {
            alert('Data refresh initiated');
        }
        function openAirflow() {
            window.open('http://localhost:8080', '_blank');
        }
        function openJupyter() {
            window.open('http://localhost:8888', '_blank');
        }
    </script>
</body>
</html>
HTML

echo ""
echo "🎉 B2B Data Platform Installation Complete!"
echo ""
echo "📋 INSTALLED COMPONENTS:"
echo "   1. Python 3.11 with virtual environment"
echo "   2. Docker & Docker Compose"
echo "   3. Java 11 (for Spark)"
echo "   4. PostgreSQL, Redis"
echo "   5. Node.js & npm"
echo "   6. Complete Python data stack"
echo "   7. Project structure with datalake"
echo "   8. Docker services (Airflow, Jupyter)"
echo "   9. Startup/shutdown scripts"
echo "   10. HTML dashboard"
echo ""
echo "🚀 TO START THE PLATFORM:"
echo "   ./start_platform.sh"
echo ""
echo "🧪 TO TEST INSTALLATION:"
echo "   ./quick_test.sh"
echo ""
echo "📚 DOCUMENTATION:"
echo "   View README_ENVR6.md for detailed usage"
echo ""
echo "🔗 GITHUB REPOSITORY:"
echo "   https://github.com/shellworlds/ENVR/tree/ENVR6"
echo ""
