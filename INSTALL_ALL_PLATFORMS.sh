#!/bin/bash
# Cross-platform installation script for ENVR Module Splitter
# Supports: Linux (Ubuntu/Debian/Fedora), macOS, Windows (Git Bash)

set -e

echo "ENVR Module Splitter - Cross-Platform Installation"
echo "=================================================="

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "Linux" ;;
        Darwin*)    echo "macOS" ;;
        CYGWIN*|MINGW*|MSYS*) echo "Windows" ;;
        *)          echo "Unknown" ;;
    esac
}

OS=$(detect_os)
echo "Detected OS: $OS"

# Install dependencies based on OS
install_dependencies() {
    echo -e "\nInstalling dependencies for $OS..."
    
    case $OS in
        "Linux")
            # Ubuntu/Debian
            if command -v apt &> /dev/null; then
                echo "Detected Ubuntu/Debian system"
                sudo apt update
                sudo apt install -y git python3 python3-pip nodejs npm default-jdk g++ golang docker.io curl wget
            # Fedora/RHEL
            elif command -v dnf &> /dev/null; then
                echo "Detected Fedora/RHEL system"
                sudo dnf install -y git python3 python3-pip nodejs npm java-latest-openjdk-devel gcc-c++ golang docker curl wget
            else
                echo "Unsupported Linux distribution. Please install manually:"
                echo "- git, python3, pip, nodejs, npm, java, g++, go, docker"
            fi
            ;;
            
        "macOS")
            echo "Setting up macOS..."
            # Check for Homebrew
            if ! command -v brew &> /dev/null; then
                echo "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install git python node openjdk@21 gcc go docker curl wget
            ;;
            
        "Windows")
            echo "Windows installation guide:"
            echo ""
            echo "Please install the following manually:"
            echo "1. Git for Windows: https://git-scm.com/download/win"
            echo "2. Python 3.12+: https://www.python.org/downloads/"
            echo "3. Node.js LTS: https://nodejs.org/"
            echo "4. Java JDK 21: https://adoptium.net/"
            echo "5. MinGW-w64 for C++: https://www.mingw-w64.org/"
            echo "6. Go: https://go.dev/dl/"
            echo "7. Docker Desktop: https://www.docker.com/products/docker-desktop/"
            echo ""
            echo "After installation, restart terminal and run this script again from Git Bash."
            exit 0
            ;;
        *)
            echo "Unsupported OS. Please install dependencies manually."
            exit 1
            ;;
    esac
}

# Clone repository function
clone_repository() {
    echo -e "\nAvailable ENVR Module Splitter repositories:"
    echo "1. Zius-Global/ZENVR (Client: Zius Global)"
    echo "2. dt-uk/DENVR (Client: Data-T UK)"
    echo "3. qb-eu/QENVR (Client: QB Europe)"
    echo "4. vipul-zius/ZENVR (Client: Vipul Zius)"
    echo "5. mike-aeq/AENVR (Client: Mike A-EQ)"
    echo "6. shellworlds/ENVR (Master reference)"
    
    read -p "Enter repository number (1-6, default 6): " repo_num
    
    case ${repo_num:-6} in
        1) REPO="Zius-Global/ZENVR"; BRANCH="ZENVR41"; CLIENT="Zius Global" ;;
        2) REPO="dt-uk/DENVR"; BRANCH="DENVR41"; CLIENT="Data-T UK" ;;
        3) REPO="qb-eu/QENVR"; BRANCH="QENVR41"; CLIENT="QB Europe" ;;
        4) REPO="vipul-zius/ZENVR"; BRANCH="ZENVR41"; CLIENT="Vipul Zius" ;;
        5) REPO="mike-aeq/AENVR"; BRANCH="AENVR41"; CLIENT="Mike A-EQ" ;;
        6) REPO="shellworlds/ENVR"; BRANCH="ENVR41"; CLIENT="Master Reference" ;;
        *) REPO="shellworlds/ENVR"; BRANCH="ENVR41"; CLIENT="Master Reference" ;;
    esac
    
    echo -e "\nCloning $CLIENT repository..."
    echo "Repository: $REPO"
    echo "Branch: $BRANCH"
    
    git clone -b $BRANCH https://github.com/$REPO.git envr-module-splitter-$CLIENT
    cd envr-module-splitter-$CLIENT
    
    echo -e "\nRepository cloned successfully!"
    echo "Directory: $(pwd)"
    ls -la
}

# Install Python dependencies
install_python_deps() {
    echo -e "\nInstalling Python dependencies..."
    if command -v pip3 &> /dev/null; then
        pip3 install numpy scipy --user
    elif command -v pip &> /dev/null; then
        pip install numpy scipy --user
    else
        echo "Warning: pip not found. Python dependencies not installed."
        echo "Install pip and run: pip install numpy scipy"
    fi
}

# Install Node.js dependencies
install_node_deps() {
    echo -e "\nInstalling Node.js dependencies..."
    if command -v npm &> /dev/null; then
        npm install
    else
        echo "Warning: npm not found. Node.js dependencies not installed."
        echo "Install Node.js and run: npm install"
    fi
}

# Build all implementations
build_all() {
    echo -e "\nBuilding all implementations..."
    if [ -f scripts/build_all.sh ]; then
        chmod +x scripts/build_all.sh
        ./scripts/build_all.sh
    else
        echo "Build script not found. Creating build directory..."
        mkdir -p bin
        echo "Build directory created: bin/"
    fi
}

# Test all implementations
test_all() {
    echo -e "\nTesting Module Splitting Theorem implementations..."
    if [ -f scripts/test_all.sh ]; then
        chmod +x scripts/test_all.sh
        ./scripts/test_all.sh
    else
        echo "Test script not found. Running manual tests..."
        
        # Test Python
        echo -e "\n--- Testing Python ---"
        python3 src/module_splitter.py 2>/dev/null || echo "Python test failed or not installed"
        
        # Test Java
        echo -e "\n--- Testing Java ---"
        javac -d bin src/ModuleSplitter.java 2>/dev/null && \
        java -cp bin com.envr.modulesplitter.ModuleSplitter 2>/dev/null || echo "Java test failed or not installed"
        
        # Test Go
        echo -e "\n--- Testing Go ---"
        go run src/module_splitter.go 2>/dev/null || echo "Go test failed or not installed"
    fi
}

# Display project information
show_info() {
    echo -e "\n=================================================="
    echo "ENVR MODULE SPLITTER - INSTALLATION COMPLETE"
    echo "=================================================="
    echo "Client: $CLIENT"
    echo "Repository: $REPO"
    echo "Branch: $BRANCH"
    echo "Directory: $(pwd)"
    echo ""
    echo "IMPLEMENTATIONS AVAILABLE:"
    echo "1. Python: Theorem verification (src/module_splitter.py)"
    echo "2. Java: Enterprise implementation (src/ModuleSplitter.java)"
    echo "3. C++: High-performance (src/module_splitter.cpp)"
    echo "4. Go: Concurrent verification (src/module_splitter.go)"
    echo "5. React/Next.js: Web visualization (docs/visualization.html)"
    echo ""
    echo "QUICK START COMMANDS:"
    echo "  Python:    python3 src/module_splitter.py"
    echo "  Java:      javac -d bin src/ModuleSplitter.java && java -cp bin com.envr.modulesplitter.ModuleSplitter"
    echo "  C++:       g++ -std=c++11 -o bin/splitter src/module_splitter.cpp && ./bin/splitter"
    echo "  Go:        go run src/module_splitter.go"
    echo "  Web UI:    open docs/visualization.html in browser"
    echo ""
    echo "DOCUMENTATION:"
    echo "  - README.md: Project overview and setup"
    echo "  - POC_REPORT.md: Comprehensive proof of concept"
    echo "  - FINAL_REPOSITORY_TABLE.md: Deployment status"
    echo ""
    echo "SUPPORT:"
    echo "  Primary Developer: shellworlds"
    echo "  GitHub: https://github.com/$REPO/tree/$BRANCH"
    echo "=================================================="
}

# Main installation function
main() {
    echo "Starting ENVR Module Splitter installation..."
    
    # Step 1: Install dependencies
    install_dependencies
    
    # Step 2: Clone repository
    clone_repository
    
    # Step 3: Install language dependencies
    install_python_deps
    install_node_deps
    
    # Step 4: Build implementations
    build_all
    
    # Step 5: Test implementations
    test_all
    
    # Step 6: Show information
    show_info
    
    echo -e "\nInstallation completed successfully!"
    echo "Next: Review the project files and run implementations."
}

# Run main function
main "$@"
