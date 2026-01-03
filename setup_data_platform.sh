#!/bin/bash
# Shell: B2B Data Platform Setup Script
# Multi-platform installation for Lenovo, Mac, Windows (WSL)

set -euo pipefail

# Platform detection
detect_platform() {
    case "$(uname -s)" in
        Linux*)     
            if [[ -f /etc/os-release ]]; then
                . /etc/os-release
                OS="$NAME"
                VER="$VERSION_ID"
                
                # Check for WSL
                if grep -q Microsoft /proc/version 2>/dev/null; then
                    echo "windows-wsl"
                else
                    echo "linux"
                fi
            else
                echo "linux"
            fi
            ;;
        Darwin*)    
            echo "macos"
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            echo "windows"
            ;;
        *)          
            echo "unknown"
            ;;
    esac
}

PLATFORM=$(detect_platform)

echo "🚀 B2B Data Platform Setup"
echo "Platform detected: $PLATFORM"
echo "========================================="

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Installation functions
install_python_deps() {
    echo -e "${BLUE}Installing Python dependencies...${NC}"
    
    # Create virtual environment
    python3 -m venv venv
    
    # Activate based on platform
    case "$PLATFORM" in
        "windows"|"windows-wsl")
            source venv/Scripts/activate
            ;;
        *)
            source venv/bin/activate
            ;;
    esac
    
    # Install packages
    pip install --upgrade pip
    
    cat > requirements.txt << REQ
# B2B Data Platform Dependencies
pandas>=2.0.0
numpy>=1.24.0
pydantic>=2.0.0
pyyaml>=6.0
asyncio
aiohttp>=3.8.0
sqlalchemy>=2.0.0
apache-airflow>=2.7.0
prefect>=2.0.0
dbt-core>=1.5.0
pyspark>=3.4.0
boto3>=1.28.0  # AWS
google-cloud-storage>=2.0.0  # GCP
azure-storage-blob>=12.0.0  # Azure
snowflake-connector-python>=3.0.0
great-expectations>=0.16.0
dagster>=1.3.0
jupyter>=1.0.0
REQ
    
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
}

install_docker() {
    echo -e "${BLUE}Installing Docker...${NC}"
    
    case "$PLATFORM" in
        "linux")
            # Ubuntu/Debian
            sudo apt-get update
            sudo apt-get install -y docker.io docker-compose
            sudo systemctl enable docker
            sudo systemctl start docker
            sudo usermod -aG docker $USER
            ;;
        "macos")
            # macOS with Homebrew
            if ! command -v brew &> /dev/null; then
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install docker docker-compose
            ;;
        "windows-wsl")
            echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
            echo "Then enable WSL2 integration in Docker Desktop settings"
            read -p "Press Enter after Docker Desktop is installed..."
            ;;
        "windows")
            echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}✅ Docker installed${NC}"
}

install_data_tools() {
    echo -e "${BLUE}Installing data tools...${NC}"
    
    case "$PLATFORM" in
        "linux"|"windows-wsl")
            # Install Java for Spark
            sudo apt-get install -y openjdk-11-jdk
            
            # Install other tools
            sudo apt-get install -y \
                postgresql \
                redis-server \
                kafkacat \
                jq \
                curl \
                wget
            ;;
        "macos")
            brew install openjdk@11 postgresql redis kafka jq curl wget
            ;;
    esac
    
    echo -e "${GREEN}✅ Data tools installed${NC}"
}

setup_airflow() {
    echo -e "${BLUE}Setting up Apache Airflow...${NC}"
    
    # Initialize Airflow
    export AIRFLOW_HOME=$(pwd)/airflow
    mkdir -p $AIRFLOW_HOME
    
    # Create airflow.cfg
    cat > $AIRFLOW_HOME/airflow.cfg << AIRFLOWCFG
[core]
dags_folder = $(pwd)/data_pipeline/dags
load_examples = False
executor = LocalExecutor
sql_alchemy_conn = sqlite:///$AIRFLOW_HOME/airflow.db

[scheduler]
min_file_process_interval = 30
catchup_by_default = False

[webserver]
web_server_port = 8080
AIRFLOWCFG
    
    # Initialize database
    airflow db init
    
    # Create admin user
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com \
        --password admin
    
    echo -e "${GREEN}✅ Airflow setup complete${NC}"
    echo "Start Airflow: airflow webserver --port 8080 & airflow scheduler"
}

setup_datalake_structure() {
    echo -e "${BLUE}Setting up datalake structure...${NC}"
    
    # Create S3/minio local structure
    mkdir -p datalake/{raw,processed,curated}/landing_zone/{daily,hourly,monthly}
    mkdir -p datalake/{bronze,silver,gold}/zone/{client_data,reference_data}
    
    # Create sample data
    cat > datalake/bronze/zone/client_data/sample_data.json << SAMPLE
{
    "client_id": "enterprise_corp",
    "data_type": "transactions",
    "ingestion_time": "$(date -Iseconds)",
    "records": 1000,
    "format": "parquet"
}
SAMPLE
    
    echo -e "${GREEN}✅ Datalake structure created${NC}"
}

create_sample_pipelines() {
    echo -e "${BLUE}Creating sample data pipelines...${NC}"
    
    # Create DAG for Airflow
    mkdir -p data_pipeline/dags
    
    cat > data_pipeline/dags/b2b_data_pipeline.py << DAG
"""
B2B Data Pipeline DAG for Airflow
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd

def extract_data(**kwargs):
    """Extract data from B2B source"""
    print("Extracting B2B data...")
    # Simulate data extraction
    data = pd.DataFrame({
        'transaction_id': range(1000),
        'amount': [x * 1.5 for x in range(1000)],
        'client': ['enterprise_corp'] * 1000
    })
    return data.to_dict()

def transform_data(**kwargs):
    """Transform B2B data"""
    print("Transforming B2B data...")
    ti = kwargs['ti']
    data_dict = ti.xcom_pull(task_ids='extract_data')
    data = pd.DataFrame.from_dict(data_dict)
    
    # Apply transformations
    data['amount_usd'] = data['amount'] * 1.0
    data['processed_at'] = datetime.now()
    
    return data.to_dict()

def load_to_datalake(**kwargs):
    """Load to datalake"""
    print("Loading to datalake...")
    ti = kwargs['ti']
    data_dict = ti.xcom_pull(task_ids='transform_data')
    data = pd.DataFrame.from_dict(data_dict)
    
    # Save to local datalake (simulated)
    path = f"datalake/bronze/zone/client_data/{datetime.now().strftime('%Y%m%d')}.parquet"
    data.to_parquet(path, compression='snappy')
    print(f"Data saved to: {path}")

# Define DAG
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'b2b_data_pipeline',
    default_args=default_args,
    description='B2B Data Pipeline with Datalake and Warehouse',
    schedule_interval='0 * * * *',  # Hourly
    catchup=False
)

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_to_datalake',
    python_callable=load_to_datalake,
    dag=dag
)

# Set task dependencies
extract_task >> transform_task >> load_task
DAG
    
    echo -e "${GREEN}✅ Sample pipelines created${NC}"
}

create_one_click_script() {
    echo -e "${BLUE}Creating one-click startup script...${NC}"
    
    cat > start_platform.sh << STARTUP
#!/bin/bash
# One-click B2B Data Platform Startup

echo "🚀 Starting B2B Data Platform..."

# Start services based on platform
case "\$(uname -s)" in
    Linux*|Darwin*)
        # Start Airflow
        echo "Starting Airflow..."
        export AIRFLOW_HOME=\$(pwd)/airflow
        airflow webserver --port 8080 --daemon
        airflow scheduler --daemon
        
        # Start local services
        echo "Starting local services..."
        docker-compose up -d
        
        echo "✅ Platform started!"
        echo "📊 Airflow UI: http://localhost:8080"
        echo "🔗 Admin: admin / admin"
        ;;
    *)
        echo "Platform not fully supported for auto-start"
        ;;
esac
STARTUP
    
    chmod +x start_platform.sh
    
    cat > stop_platform.sh << SHUTDOWN
#!/bin/bash
# Shutdown B2B Data Platform

echo "🛑 Stopping B2B Data Platform..."

# Stop services
pkill -f "airflow"
docker-compose down

echo "✅ Platform stopped"
SHUTDOWN
    
    chmod +x stop_platform.sh
    
    echo -e "${GREEN}✅ Startup scripts created${NC}"
}

show_instructions() {
    echo -e "\n${GREEN}✅ B2B Data Platform Setup Complete!${NC}"
    echo -e "\n${BLUE}📋 NEXT STEPS:${NC}"
    
    case "$PLATFORM" in
        "linux"|"macos")
            echo "1. Activate virtual environment:"
            echo "   source venv/bin/activate"
            echo ""
            echo "2. Start the platform:"
            echo "   ./start_platform.sh"
            echo ""
            echo "3. Access services:"
            echo "   Airflow UI: http://localhost:8080"
            echo "   Jupyter: jupyter lab"
            ;;
        "windows-wsl")
            echo "1. Activate virtual environment:"
            echo "   source venv/Scripts/activate"
            echo ""
            echo "2. Start Docker Desktop (GUI application)"
            echo ""
            echo "3. Start the platform:"
            echo "   ./start_platform.sh"
            echo ""
            echo "4. Access services:"
            echo "   Airflow UI: http://localhost:8080"
            ;;
        "windows")
            echo "1. Open PowerShell as Administrator"
            echo "2. Install WSL2: wsl --install"
            echo "3. Install Ubuntu from Microsoft Store"
            echo "4. Run this script in WSL2"
            ;;
    esac
    
    echo -e "\n${YELLOW}🔧 Available Tools:${NC}"
    echo "   • Airflow (Orchestration)"
    echo "   • Spark (Processing)"
    echo "   • DBT (Transformation)"
    echo "   • Datalake Structure"
    echo "   • Sample Pipelines"
    
    echo -e "\n${BLUE}📚 Documentation:${NC}"
    echo "   View README.md for detailed usage"
}

# Main installation flow
main() {
    echo -e "${BLUE}Starting B2B Data Platform installation...${NC}"
    
    install_python_deps
    install_docker
    install_data_tools
    setup_airflow
    setup_datalake_structure
    create_sample_pipelines
    create_one_click_script
    show_instructions
}

# Run main function
main
