#!/bin/bash

echo "=== Docker Setup for Quantum JV Platform ==="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing..."
    
    # Ubuntu/Debian
    if [ -f /etc/debian_version ]; then
        sudo apt update
        sudo apt install -y docker.io docker-compose
        sudo systemctl start docker
        sudo systemctl enable docker
        
    # MacOS (assuming Homebrew)
    elif [ "$(uname)" == "Darwin" ]; then
        brew install docker docker-compose
        open /Applications/Docker.app
        
    else
        echo "Please install Docker manually from: https://docs.docker.com/get-docker/"
        exit 1
    fi
fi

# Create Dockerfile for quantum platform
cat > Dockerfile << 'DOCKERFILE'
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    nodejs \
    npm \
    openjdk-17-jdk \
    golang-go \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
COPY src/node/package*.json ./src/node/
RUN cd src/node && npm install --production

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 quantumuser && chown -R quantumuser:quantumuser /app
USER quantumuser

# Expose ports
EXPOSE 8000 3000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/quantum/health || exit 1

# Start application
CMD ["bash", "scripts/start_all.sh"]
DOCKERFILE

# Create docker-compose.yml
cat > docker-compose.yml << 'COMPOSE'
version: '3.8'

services:
  quantum-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
      - PYTHONPATH=/app/src/python
      - QUANTUM_BACKEND=simulator
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    command: python src/python/api_server.py
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/quantum/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - quantum-network

  quantum-frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:3000"
    depends_on:
      - quantum-api
    environment:
      - REACT_APP_API_URL=http://quantum-api:8000
    networks:
      - quantum-network

  quantum-database:
    image: postgres:15
    environment:
      - POSTGRES_DB=quantumdb
      - POSTGRES_USER=quantumuser
      - POSTGRES_PASSWORD=quantumpass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - quantum-network

  redis-cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - quantum-network

  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - quantum-api
      - quantum-frontend
    networks:
      - quantum-network

volumes:
  postgres_data:
  redis_data:

networks:
  quantum-network:
    driver: bridge
COMPOSE

# Create frontend Dockerfile
cat > Dockerfile.frontend << 'FRONTEND'
FROM node:20-alpine

WORKDIR /app

COPY src/react/package*.json ./
RUN npm install --production

COPY src/react/ ./

RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
FRONTEND

echo ""
echo "Docker setup complete!"
echo "Files created:"
echo "1. Dockerfile"
echo "2. docker-compose.yml"
echo "3. Dockerfile.frontend"
echo ""
echo "To build and run:"
echo "  docker-compose build"
echo "  docker-compose up -d"
echo ""
echo "To stop:"
echo "  docker-compose down"
