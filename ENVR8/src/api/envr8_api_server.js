/**
 * ENVR8 Advanced API Server
 * B2B Data Flow with Security Middleware
 * Built with: Node.js, Express, Security Headers
 */
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// 5 Crucial Processes Endpoints
const processes = [
  {
    id: 1,
    name: 'Secure Data Pipeline',
    description: 'B2B data flow with encryption and validation',
    tools: ['Apache Airflow', 'MLflow', 'Trivy', 'Snyk'],
    endpoint: '/api/pipeline'
  },
  {
    id: 2,
    name: 'MLOps Lifecycle',
    description: 'End-to-end ML model management',
    tools: ['Kubeflow', 'MLflow', 'Prometheus', 'Grafana'],
    endpoint: '/api/mlops'
  },
  {
    id: 3,
    name: 'Threat Detection',
    description: 'Real-time cyber attack monitoring',
    tools: ['Snort', 'Wazuh', 'osquery', 'Falco'],
    endpoint: '/api/security'
  },
  {
    id: 4,
    name: 'Code Security',
    description: 'Vulnerability scanning and prevention',
    tools: ['Checkov', 'GitLeaks', 'Snyk', 'Trivy'],
    endpoint: '/api/code-security'
  },
  {
    id: 5,
    name: 'Monitoring & Response',
    description: 'System health and incident management',
    tools: ['Prometheus', 'Grafana', 'Jaeger', 'ELK Stack'],
    endpoint: '/api/monitoring'
  }
];

// Platform information
const platformInfo = {
  name: 'ENVR8 Advanced Platform',
  version: '1.0.0',
  supportedPlatforms: ['Linux (Lenovo ThinkPad)', 'Mac OS X', 'Windows WSL'],
  systemRequirements: {
    memory: '8GB minimum, 32GB recommended',
    storage: '50GB minimum',
    os: 'Ubuntu 20.04+, macOS 11+, Windows 10+'
  }
};

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'ENVR8 Advanced API Server',
    platform: platformInfo,
    processes: processes.length,
    tools: 16,
    status: 'operational'
  });
});

// Processes endpoint
app.get('/api/processes', (req, res) => {
  res.json({
    processes: processes,
    total: processes.length,
    description: '5 crucial processes for B2B data flow with MLOps and security'
  });
});

// Platform-specific installation guide
app.get('/api/install/:platform', (req, res) => {
  const platform = req.params.platform;
  const guides = {
    linux: {
      commands: [
        'sudo apt-get update',
        'sudo apt-get install -y docker.io docker-compose',
        'sudo apt-get install -y python3-pip nodejs npm golang',
        'pip install mlflow kubeflow',
        'npm install -g snyk trivy'
      ],
      note: 'Optimized for Lenovo ThinkPad with Ubuntu Linux'
    },
    mac: {
      commands: [
        'brew update',
        'brew install mlflow kubeflow',
        'brew install docker node',
        'pip3 install mlflow',
        'npm install -g snyk'
      ],
      note: 'Mac OS X installation'
    },
    windows: {
      commands: [
        'choco install docker-desktop',
        'choco install python nodejs',
        'pip install mlflow',
        'npm install -g snyk',
        'Install WSL2 for Linux compatibility'
      ],
      note: 'Windows with WSL recommended'
    }
  };

  if (guides[platform]) {
    res.json(guides[platform]);
  } else {
    res.status(400).json({ error: 'Platform not supported' });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    system: platformInfo.supportedPlatforms[0],
    tools: '16 advanced tools integrated'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`ENVR8 API Server running on port ${PORT}`);
  console.log(`Platform: ${platformInfo.supportedPlatforms[0]}`);
  console.log(`Integrated Tools: 16 advanced tools`);
  console.log(`Processes: ${processes.length} crucial processes`);
  console.log(`Access: http://localhost:${PORT}`);
});
