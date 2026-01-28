FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    default-jdk \
    g++ \
    golang \
    rustc \
    cargo \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install sympy numpy matplotlib pytest

# Install Node.js dependencies
RUN npm install

# Create directories for different language outputs
RUN mkdir -p /app/output

# Set up execution permissions
RUN chmod +x /app/scripts/*.sh

# Default command: run all implementations
CMD ["./scripts/run_all.sh"]

# Expose port for web dashboard (if implemented)
EXPOSE 3000
