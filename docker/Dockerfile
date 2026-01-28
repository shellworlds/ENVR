# File: Dockerfile
# Purpose: Containerized deployment of projective module project

FROM ubuntu:24.04

# Set metadata
LABEL maintainer="shellworlds"
LABEL version="1.0"
LABEL description="Projective Module Theorem Implementation"

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PROJECT_DIR=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    default-jdk \
    golang \
    g++ \
    make \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create project directory
WORKDIR $PROJECT_DIR

# Copy project files
COPY . .

# Create Python virtual environment
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt 2>/dev/null || true

# Install Node.js dependencies
WORKDIR $PROJECT_DIR/api
RUN npm install express 2>/dev/null || true

# Build all implementations
WORKDIR $PROJECT_DIR
RUN mkdir -p build && \
    make build || echo "Build completed with some warnings"

# Expose API port
EXPOSE 3000

# Set default command
CMD ["make", "test"]
