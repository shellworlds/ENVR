/**
 * Quantum JV Platform - Node.js Express Server
 * REST API for quantum circuit operations
 */

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { PythonShell } = require('python-shell');

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Quantum API Routes
app.get('/api/quantum/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Quantum JV Platform API',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

app.post('/api/quantum/circuit', async (req, res) => {
  try {
    const { circuitType, qubits, gates } = req.body;
    
    // Python integration for quantum computation
    const options = {
      mode: 'text',
      pythonPath: 'python3',
      scriptPath: './src/python',
      args: [JSON.stringify({ circuitType, qubits, gates })]
    };
    
    PythonShell.run('quantum_processor.py', options, (err, results) => {
      if (err) {
        console.error('Python execution error:', err);
        return res.status(500).json({ error: 'Quantum computation failed' });
      }
      
      res.json({
        success: true,
        circuit: req.body,
        result: JSON.parse(results[0]),
        executionTime: new Date().toISOString()
      });
    });
    
  } catch (error) {
    console.error('Circuit creation error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/api/quantum/simulate/:circuitId', (req, res) => {
  const { circuitId } = req.params;
  const shots = req.query.shots || 1024;
  
  // Mock simulation for now
  const results = {
    circuitId,
    shots: parseInt(shots),
    counts: {
      '00': Math.floor(Math.random() * shots * 0.4),
      '01': Math.floor(Math.random() * shots * 0.3),
      '10': Math.floor(Math.random() * shots * 0.2),
      '11': Math.floor(Math.random() * shots * 0.1)
    },
    statevector: Array(4).fill(0).map(() => ({
      real: Math.random() - 0.5,
      imag: Math.random() - 0.5
    })),
    executionTime: Math.random() * 1000 + 100
  };
  
  res.json(results);
});

// Client management routes
app.post('/api/clients/register', (req, res) => {
  const { clientName, email, repository } = req.body;
  
  // Validate required fields
  if (!clientName || !repository) {
    return res.status(400).json({ error: 'Client name and repository are required' });
  }
  
  const clientData = {
    id: Date.now().toString(),
    name: clientName,
    email: email || '',
    repository,
    apiKey: generateApiKey(),
    createdAt: new Date().toISOString(),
    status: 'active'
  };
  
  res.json({
    success: true,
    message: 'Client registered successfully',
    client: clientData,
    nextSteps: [
      'Add webhook to repository',
      'Configure API integration',
      'Set up authentication tokens'
    ]
  });
});

function generateApiKey() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let apiKey = 'qkv_';
  for (let i = 0; i < 32; i++) {
    apiKey += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return apiKey;
}

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something broke!', details: err.message });
});

// Start server
app.listen(PORT, () => {
  console.log(`Quantum JV Platform Server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/quantum/health`);
  console.log(`API Documentation available at /api/docs`);
});
