# Multi-stage Dockerfile for full-stack quantum AI
FROM python:3.11-slim as base

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ nodejs npm openjdk-17-jdk golang-go \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Node.js dependencies
COPY package*.json ./
RUN npm ci --only=production

# Application
COPY . /app
WORKDIR /app

# Multi-service setup
EXPOSE 8000 3000 8080

CMD ["python", "orchestrator.py"]
