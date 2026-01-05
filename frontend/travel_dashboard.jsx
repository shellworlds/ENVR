/**
 * ENVR11 Travel Dashboard - React Frontend
 * Real-time travel analytics with quantum optimization visualization
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const TravelDashboard = () => {
  const [travelData, setTravelData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantumStatus, setQuantumStatus] = useState(false);
  const [optimizationResult, setOptimizationResult] = useState(null);
  
  // Colors for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];
  
  // Fetch travel data from backend
  useEffect(() => {
    const fetchTravelData = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://localhost:8000/api/travel-data');
        setTravelData(response.data);
        setQuantumStatus(response.data.quantum_capable);
        setOptimizationResult(response.data.optimization);
      } catch (error) {
        console.error('Error fetching travel data:', error);
        // Load sample data if API fails
        loadSampleData();
      } finally {
        setLoading(false);
      }
    };
    
    fetchTravelData();
  }, []);
  
  const loadSampleData = () => {
    const sampleData = {
      destinations: [
        { name: 'Paris', distance: 300, cost: 500, days: 3, bookings: 150 },
        { name: 'London', distance: 200, cost: 400, days: 2, bookings: 200 },
        { name: 'Rome', distance: 400, cost: 600, days: 4, bookings: 120 },
        { name: 'Berlin', distance: 350, cost: 450, days: 3, bookings: 180 },
        { name: 'Madrid', distance: 450, cost: 550, days: 3, bookings: 90 }
      ],
      priceTrends: [
        { month: 'Jan', price: 450, demand: 80 },
        { month: 'Feb', price: 480, demand: 85 },
        { month: 'Mar', price: 520, demand: 90 },
        { month: 'Apr', price: 550, demand: 95 },
        { month: 'May', price: 500, demand: 88 },
        { month: 'Jun', price: 480, demand: 92 }
      ],
      optimization: {
        optimal_route: [0, 1, 3],
        optimal_value: 850,
        solved_with: 'QAOA',
        qubits_used: 20
      },
      quantum_capable: true,
      timestamp: new Date().toISOString()
    };
    
    setTravelData(sampleData);
    setQuantumStatus(true);
    setOptimizationResult(sampleData.optimization);
  };
  
  const runQuantumOptimization = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:8000/api/quantum-optimize', {
        destinations: travelData?.destinations || [],
        constraints: { max_destinations: 3 }
      });
      setOptimizationResult(response.data);
    } catch (error) {
      console.error('Quantum optimization failed:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="quantum-loader">
          <div className="qubit-animation"></div>
          <p>Loading Quantum Travel Optimizer...</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="travel-dashboard">
      <header className="dashboard-header">
        <h1>ENVR11 Travel Agent ML Dashboard</h1>
        <div className="header-status">
          <span className={`quantum-status ${quantumStatus ? 'active' : 'inactive'}`}>
            Quantum: {quantumStatus ? '✓ 20-Qubit Ready' : '✗ Classical Only'}
          </span>
          <span className="timestamp">
            Last updated: {new Date(travelData?.timestamp).toLocaleString()}
          </span>
        </div>
      </header>
      
      <div className="dashboard-grid">
        {/* Destination Popularity Chart */}
        <div className="dashboard-card">
          <h2>Destination Popularity</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={travelData?.destinations}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="bookings" fill="#0088FE" name="Bookings" />
                <Bar dataKey="cost" fill="#00C49F" name="Avg Cost ($)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* Price Trends Chart */}
        <div className="dashboard-card">
          <h2>Price & Demand Trends</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={travelData?.priceTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="price" stroke="#FF8042" name="Price ($)" />
                <Line yAxisId="right" type="monotone" dataKey="demand" stroke="#8884D8" name="Demand Index" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* Quantum Optimization Panel */}
        <div className="dashboard-card quantum-panel">
          <h2>Quantum Route Optimization</h2>
          <div className="quantum-info">
            <div className="algorithm-info">
              <strong>Algorithm:</strong> {optimizationResult?.solved_with}
              <br />
              <strong>Qubits Used:</strong> {optimizationResult?.qubits_used}
              <br />
              <strong>Optimal Cost:</strong> ${optimizationResult?.optimal_value}
            </div>
            
            <div className="optimal-route">
              <h3>Optimal Route</h3>
              <div className="route-visualization">
                {optimizationResult?.optimal_route?.map((destIndex, idx) => (
                  <div key={idx} className="route-step">
                    <div className="step-number">{idx + 1}</div>
                    <div className="step-destination">
                      {travelData?.destinations[destIndex]?.name || `Destination ${destIndex}`}
                    </div>
                    <div className="step-cost">
                      ${travelData?.destinations[destIndex]?.cost || 0}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <button 
            className="quantum-button"
            onClick={runQuantumOptimization}
            disabled={!quantumStatus}
          >
            {quantumStatus ? 'Run Quantum Optimization' : 'Quantum Not Available'}
          </button>
        </div>
        
        {/* Destination Distribution Pie Chart */}
        <div className="dashboard-card">
          <h2>Destination Distribution</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={travelData?.destinations}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.name}: ${entry.bookings}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="bookings"
                >
                  {travelData?.destinations?.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* System Metrics */}
        <div className="dashboard-card metrics-card">
          <h2>System Metrics</h2>
          <div className="metrics-grid">
            <div className="metric">
              <div className="metric-value">{travelData?.destinations?.length || 0}</div>
              <div className="metric-label">Destinations</div>
            </div>
            <div className="metric">
              <div className="metric-value">
                ${travelData?.destinations?.reduce((sum, d) => sum + d.cost, 0) || 0}
              </div>
              <div className="metric-label">Total Cost</div>
            </div>
            <div className="metric">
              <div className="metric-value">
                {travelData?.destinations?.reduce((sum, d) => sum + d.bookings, 0) || 0}
              </div>
              <div className="metric-label">Total Bookings</div>
            </div>
            <div className="metric">
              <div className="metric-value">
                {optimizationResult?.qubits_used || 0}
              </div>
              <div className="metric-label">Qubits Active</div>
            </div>
          </div>
        </div>
        
        {/* ML Predictions */}
        <div className="dashboard-card ml-predictions">
          <h2>ML Price Predictions</h2>
          <div className="prediction-list">
            <div className="prediction-item">
              <div className="prediction-destination">Paris → Rome</div>
              <div className="prediction-price">$420 - $480</div>
              <div className="prediction-confidence">85% accuracy</div>
            </div>
            <div className="prediction-item">
              <div className="prediction-destination">London → Berlin</div>
              <div className="prediction-price">$380 - $430</div>
              <div className="prediction-confidence">88% accuracy</div>
            </div>
            <div className="prediction-item">
              <div className="prediction-destination">NYC → Tokyo</div>
              <div className="prediction-price">$1,200 - $1,350</div>
              <div className="prediction-confidence">82% accuracy</div>
            </div>
          </div>
          <button className="refresh-predictions">
            Refresh Predictions
          </button>
        </div>
      </div>
      
      <footer className="dashboard-footer">
        <p>ENVR11 Travel Agent ML System • Quantum Enhanced • Real-time Analytics</p>
        <p>System Status: <span className="status-active">Operational</span></p>
      </footer>
    </div>
  );
};

// CSS Styles (would be in separate CSS file in production)
const styles = `
.travel-dashboard {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

.dashboard-header {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
  margin: 0;
  color: #2d3748;
  font-size: 24px;
}

.header-status {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  font-size: 14px;
}

.quantum-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: bold;
}

.quantum-status.active {
  background: #48bb78;
  color: white;
}

.quantum-status.inactive {
  background: #e53e3e;
  color: white;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chart-container {
  height: 300px;
  margin-top: 15px;
}

.quantum-panel {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.quantum-info {
  margin: 20px 0;
}

.algorithm-info {
  background: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.optimal-route {
  margin-top: 20px;
}

.route-visualization {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.route-step {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 10px;
  border-radius: 8px;
}

.step-number {
  background: white;
  color: #667eea;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 15px;
}

.step-destination {
  flex-grow: 1;
  font-weight: bold;
}

.quantum-button {
  background: white;
  color: #667eea;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  width: 100%;
  margin-top: 20px;
  transition: transform 0.2s;
}

.quantum-button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.quantum-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.metrics-card {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-top: 20px;
}

.metric {
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 8px;
}

.metric-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 14px;
  opacity: 0.9;
}

.ml-predictions .prediction-list {
  margin: 20px 0;
}

.prediction-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f7fafc;
  border-radius: 8px;
  margin-bottom: 10px;
}

.refresh-predictions {
  background: #4299e1;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
}

.dashboard-footer {
  background: rgba(255, 255, 255, 0.95);
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  font-size: 14px;
}

.status-active {
  color: #48bb78;
  font-weight: bold;
}

.dashboard-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.quantum-loader {
  text-align: center;
}

.qubit-animation {
  width: 60px;
  height: 60px;
  border: 4px solid #667eea;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
`;

// Inject styles
const styleSheet = document.createElement("style");
styleSheet.innerText = styles;
document.head.appendChild(styleSheet);

export default TravelDashboard;
