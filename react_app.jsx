/**
 * React: Quantum AI Dashboard Component
 * Modern React with hooks, context, and real-time updates
 */
import React, { useState, useEffect, useContext, useCallback } from 'react';
import { 
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { WebSocketContext } from './context/WebSocketContext';
import { QuantumAPI } from './services/quantumAPI';
import './styles/QuantumDashboard.css';

const QuantumDashboard = () => {
  const [quantumState, setQuantumState] = useState({
    qubits: 0,
    gates: [],
    entanglement: 0,
    coherenceTime: 0,
    temperature: 0
  });
  
  const [inferenceResults, setInferenceResults] = useState([]);
  const [performanceMetrics, setPerformanceMetrics] = useState({
    latency: [],
    throughput: [],
    accuracy: []
  });
  
  const [isTraining, setIsTraining] = useState(false);
  const [trainingProgress, setTrainingProgress] = useState(0);
  const { socket } = useContext(WebSocketContext);
  
  // Real-time quantum state updates via WebSocket
  useEffect(() => {
    if (!socket) return;
    
    const handleQuantumUpdate = (data) => {
      setQuantumState(prev => ({
        ...prev,
        ...data.quantumState
      }));
    };
    
    const handleInferenceResult = (data) => {
      setInferenceResults(prev => [data, ...prev.slice(0, 9)]);
    };
    
    const handleTrainingProgress = (data) => {
      setTrainingProgress(data.progress);
      setIsTraining(data.progress < 100);
    };
    
    socket.on('quantum_update', handleQuantumUpdate);
    socket.on('inference_result', handleInferenceResult);
    socket.on('training_progress', handleTrainingProgress);
    
    return () => {
      socket.off('quantum_update', handleQuantumUpdate);
      socket.off('inference_result', handleInferenceResult);
      socket.off('training_progress', handleTrainingProgress);
    };
  }, [socket]);
  
  // Fetch initial data
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [state, metrics] = await Promise.all([
          QuantumAPI.getQuantumState(),
          QuantumAPI.getPerformanceMetrics()
        ]);
        
        setQuantumState(state);
        setPerformanceMetrics(metrics);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      }
    };
    
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30s
    
    return () => clearInterval(interval);
  }, []);
  
  const startTraining = useCallback(async () => {
    setIsTraining(true);
    setTrainingProgress(0);
    
    try {
      await QuantumAPI.startTraining({
        epochs: 100,
        batchSize: 32,
        learningRate: 0.001,
        quantumEnhanced: true
      });
    } catch (error) {
      console.error('Training failed:', error);
      setIsTraining(false);
    }
  }, []);
  
  const runInference = useCallback(async (prompt) => {
    try {
      const result = await QuantumAPI.runInference({
        prompt,
        temperature: 0.7,
        maxTokens: 100,
        quantumOptimized: true
      });
      
      setInferenceResults(prev => [result, ...prev.slice(0, 9)]);
      return result;
    } catch (error) {
      console.error('Inference failed:', error);
      throw error;
    }
  }, []);
  
  // Chart data preparation
  const latencyData = performanceMetrics.latency.map((value, index) => ({
    time: index,
    latency: value
  }));
  
  const quantumMetrics = [
    { name: 'Entanglement', value: quantumState.entanglement, color: '#8884d8' },
    { name: 'Coherence', value: quantumState.coherenceTime, color: '#82ca9d' },
    { name: 'Fidelity', value: 0.95, color: '#ffc658' }
  ];
  
  const inferenceStats = inferenceResults.reduce((acc, result) => {
    acc.tokens += result.tokenCount || 0;
    acc.time += result.inferenceTime || 0;
    return acc;
  }, { tokens: 0, time: 0 });
  
  return (
    <div className="quantum-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <h1>🚀 Quantum AI Dashboard</h1>
        <div className="header-stats">
          <span className="stat-item">
            <strong>Qubits:</strong> {quantumState.qubits}
          </span>
          <span className="stat-item">
            <strong>Gates:</strong> {quantumState.gates.length}
          </span>
          <span className="stat-item">
            <strong>Temperature:</strong> {quantumState.temperature}K
          </span>
        </div>
      </header>
      
      {/* Main Dashboard Grid */}
      <div className="dashboard-grid">
        {/* Quantum State Visualization */}
        <div className="dashboard-card full-width">
          <h2>⚛️ Quantum State Monitor</h2>
          <div className="quantum-visualization">
            <div className="qubit-display">
              {Array.from({ length: quantumState.qubits }).map((_, i) => (
                <div key={i} className="qubit">
                  <div className="qubit-sphere" style={{
                    transform: `rotate(${i * 45}deg)`
                  }} />
                  <span className="qubit-label">Q{i}</span>
                </div>
              ))}
            </div>
            <div className="quantum-metrics">
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={quantumMetrics}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {quantumMetrics.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
        
        {/* Performance Metrics */}
        <div className="dashboard-card">
          <h2>📈 Performance Metrics</h2>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={latencyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" label={{ value: 'Time', position: 'insideBottom' }} />
              <YAxis label={{ value: 'Latency (ms)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="latency" stroke="#8884d8" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        
        {/* Inference Control Panel */}
        <div className="dashboard-card">
          <h2>🤖 AI Inference</h2>
          <div className="inference-controls">
            <textarea
              className="prompt-input"
              placeholder="Enter your prompt for quantum-enhanced inference..."
              rows={3}
              defaultValue="Explain quantum superposition in simple terms"
            />
            <button 
              className="inference-button"
              onClick={() => runInference("Explain quantum superposition")}
            >
              Run Inference
            </button>
            
            {isTraining && (
              <div className="training-progress">
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ width: `${trainingProgress}%` }}
                  />
                </div>
                <span>Training: {trainingProgress}%</span>
              </div>
            )}
          </div>
          
          <div className="inference-stats">
            <div className="stat-box">
              <h3>Recent Inferences</h3>
              <p>{inferenceResults.length} requests</p>
            </div>
            <div className="stat-box">
              <h3>Total Tokens</h3>
              <p>{inferenceStats.tokens}</p>
            </div>
            <div className="stat-box">
              <h3>Avg Time</h3>
              <p>{(inferenceStats.time / inferenceResults.length || 0).toFixed(2)}s</p>
            </div>
          </div>
        </div>
        
        {/* Recent Inference Results */}
        <div className="dashboard-card">
          <h2>📝 Recent Results</h2>
          <div className="results-list">
            {inferenceResults.slice(0, 5).map((result, index) => (
              <div key={index} className="result-item">
                <div className="result-header">
                  <span className="result-id">#{index + 1}</span>
                  <span className="result-time">{result.timestamp || 'Just now'}</span>
                </div>
                <p className="result-text">
                  {result.text?.substring(0, 100)}...
                </p>
                <div className="result-metrics">
                  <span>Tokens: {result.tokenCount || 'N/A'}</span>
                  <span>Time: {result.inferenceTime?.toFixed(2)}s</span>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* System Health */}
        <div className="dashboard-card">
          <h2>🩺 System Health</h2>
          <div className="health-metrics">
            <div className="health-item">
              <span className="health-label">CPU Usage</span>
              <div className="health-bar">
                <div className="health-fill cpu" style={{ width: '65%' }} />
              </div>
              <span className="health-value">65%</span>
            </div>
            <div className="health-item">
              <span className="health-label">GPU Memory</span>
              <div className="health-bar">
                <div className="health-fill gpu" style={{ width: '82%' }} />
              </div>
              <span className="health-value">82%</span>
            </div>
            <div className="health-item">
              <span className="health-label">Quantum Processor</span>
              <div className="health-bar">
                <div className="health-fill quantum" style={{ width: '45%' }} />
              </div>
              <span className="health-value">45%</span>
            </div>
          </div>
        </div>
        
        {/* Quick Actions */}
        <div className="dashboard-card">
          <h2>⚡ Quick Actions</h2>
          <div className="action-buttons">
            <button 
              className="action-button primary"
              onClick={startTraining}
              disabled={isTraining}
            >
              {isTraining ? 'Training...' : 'Start Training'}
            </button>
            <button className="action-button secondary">
              Optimize Models
            </button>
            <button className="action-button danger">
              Emergency Stop
            </button>
            <button className="action-button">
              Export Data
            </button>
          </div>
        </div>
      </div>
      
      {/* Footer Stats */}
      <footer className="dashboard-footer">
        <div className="footer-stats">
          <div className="footer-stat">
            <span className="stat-label">Uptime</span>
            <span className="stat-value">99.8%</span>
          </div>
          <div className="footer-stat">
            <span className="stat-label">Total Requests</span>
            <span className="stat-value">1,234,567</span>
          </div>
          <div className="footer-stat">
            <span className="stat-label">Avg Response Time</span>
            <span className="stat-value">124ms</span>
          </div>
          <div className="footer-stat">
            <span className="stat-label">Energy Usage</span>
            <span className="stat-value">2.4 kW/h</span>
          </div>
        </div>
        <div className="footer-info">
          <span>Quantum AI System v2.1.4 • Last updated: Just now</span>
          <span>Status: <span className="status-good">● Operational</span></span>
        </div>
      </footer>
    </div>
  );
};

// CSS Styles (simplified)
const styles = `
.quantum-dashboard {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #f1f5f9;
  min-height: 100vh;
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #334155;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.dashboard-card {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #475569;
  backdrop-filter: blur(10px);
}

.full-width {
  grid-column: 1 / -1;
}

.quantum-visualization {
  display: flex;
  gap: 40px;
  align-items: center;
}

.qubit-display {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.qubit {
  position: relative;
  width: 60px;
  height: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.qubit-sphere {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  animation: spin 4s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.inference-controls {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.prompt-input {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid #475569;
  border-radius: 8px;
  padding: 12px;
  color: #f1f5f9;
  font-size: 14px;
  resize: vertical;
}

.inference-button {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.inference-button:hover {
  transform: translateY(-2px);
}

.health-metrics {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.health-bar {
  background: rgba(71, 85, 105, 0.5);
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  flex-grow: 1;
}

.health-fill {
  height: 100%;
  border-radius: 4px;
}

.health-fill.cpu { background: #10b981; }
.health-fill.gpu { background: #8b5cf6; }
.health-fill.quantum { background: #06b6d4; }

.action-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.action-button {
  padding: 10px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.action-button.primary {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.action-button.secondary {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid #3b82f6;
}

.action-button.danger {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid #ef4444;
}

.dashboard-footer {
  background: rgba(15, 23, 42, 0.8);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #334155;
}

.footer-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.status-good {
  color: #10b981;
  font-weight: 600;
}
`;

// Export component
export default QuantumDashboard;
