#!/bin/bash

echo "=== Building Java Quantum Service ==="

# Check if Java is installed
if ! command -v javac &> /dev/null; then
    echo "Java compiler not found. Installing..."
    
    if [ -f /etc/debian_version ]; then
        sudo apt update
        sudo apt install -y default-jdk
    elif [ "$(uname)" == "Darwin" ]; then
        brew install openjdk
    else
        echo "Please install Java manually"
        exit 1
    fi
fi

# Create build directory
mkdir -p build/java
mkdir -p build/java/classes

# Compile Java files
echo "Compiling Java source files..."
javac -d build/java/classes \
    -cp "." \
    src/java/QuantumService.java

if [ $? -eq 0 ]; then
    echo "Compilation successful!"
    
    # Create JAR file
    echo "Creating JAR file..."
    cd build/java/classes
    jar cfe quantum-service.jar quantum.jv.platform.QuantumService \
        quantum/jv/platform/*.class
    
    mv quantum-service.jar ..
    cd ../../..
    
    echo "JAR created: build/java/quantum-service.jar"
    
    # Create run script
    cat > build/java/run_quantum.sh << 'RUNSCRIPT'
#!/bin/bash
echo "Running Java Quantum Service..."
java -jar quantum-service.jar
RUNSCRIPT
    
    chmod +x build/java/run_quantum.sh
    
    echo ""
    echo "To run the Java quantum service:"
    echo "  cd build/java"
    echo "  ./run_quantum.sh"
else
    echo "Compilation failed!"
    exit 1
fi
