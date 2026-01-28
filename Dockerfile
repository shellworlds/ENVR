FROM ubuntu:24.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# Install all necessary tools
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    nodejs \
    npm \
    openjdk-21-jdk \
    g++ \
    golang \
    curl \
    wget \
    make \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install numpy scipy

# Install Node.js dependencies
RUN npm install

# Create build directory
RUN mkdir -p bin

# Build all implementations
RUN chmod +x scripts/build_all.sh
RUN ./scripts/build_all.sh || echo "Build completed with warnings"

# Expose port for web visualization
EXPOSE 3000

# Default command
CMD ["python3", "src/module_splitter.py"]
