/**
 * React: B2B Data Flow Monitoring Dashboard
 * Real-time monitoring for datalake, ETL, and warehouse operations
 */
import React, { useState, useEffect, useCallback } from 'react';
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';
import {
  Database, RefreshCw, Upload, Download, AlertTriangle,
  CheckCircle, Activity, BarChart3, Server, Cpu,
  HardDrive, Network, Users, Settings, Bell
} from 'lucide-react';
import './styles/DataDashboard.css';

const B2BDataDashboard = () => {
  const [pipelines, setPipelines] = useState([]);
  const [activePipeline, setActivePipeline] = useState(null);
  const [dataMetrics, setDataMetrics] = useState({
    totalIngested: 0,
    totalProcessed: 0,
    successRate: 0,
    avgLatency: 0
  });
  const [systemHealth, setSystemHealth] = useState({
    datalake: 'healthy',
    warehouse: 'healthy',
    etl: 'healthy',
    api: 'healthy'
  });
  const [recentActivities, setRecentActivities] = useState([]);

  // Mock data - replace with API calls
  useEffect(() => {
    // Load pipelines
    const mockPipelines = [
      {
        id: 'pipeline_1',
        name: 'Enterprise Corp - Transactions',
        source: 'REST API',
        destination: 'Snowflake',
        status: 'running',
        lastRun: '2 minutes ago',
        recordsProcessed: 125000,
        successRate: 99.8
      },
      {
        id: 'pipeline_2',
        name: 'Retail Chain - Sales Data',
        source: 'PostgreSQL',
        destination: 'BigQuery',
        status: 'success',
        lastRun: '15 minutes ago',
        recordsProcessed: 85000,
        successRate: 99.5
      },
      {
        id: 'pipeline_3',
        name: 'Healthcare Inc - Patient Data',
        source: 'Kafka Stream',
        destination: 'Redshift',
        status: 'warning',
        lastRun: '1 hour ago',
        recordsProcessed: 45000,
        successRate: 97.2
      }
    ];
    
    setPipelines(mockPipelines);
    setActivePipeline(mockPipelines[0]);

    // Load metrics
    setDataMetrics({
      totalIngested: 1250000,
      totalProcessed: 1180000,
      successRate: 99.2,
      avgLatency: 1250
    });

    // Load activities
    setRecentActivities([
      { id: 1, pipeline: 'Enterprise Corp', action: 'Data Ingestion', status: 'success', time: '2 min ago', records: 1250 },
      { id: 2, pipeline: 'Retail Chain', action: 'ETL Processing', status: 'success', time: '15 min ago', records: 850 },
      { id: 3, pipeline: 'Healthcare Inc', action: 'Quality Check', status: 'warning', time: '1 hour ago', records: 450 },
      { id: 4, pipeline: 'Enterprise Corp', action: 'Warehouse Load', status: 'success', time: '2 hours ago', records: 12500 }
    ]);
  }, []);

  // Chart data
  const latencyData = [
    { hour: '00:00', latency: 1200 },
    { hour: '04:00', latency: 1100 },
    { hour: '08:00', latency: 1500 },
    { hour: '12:00', latency: 1800 },
    { hour: '16:00', latency: 1400 },
    { hour: '20:00', latency: 1000 }
  ];

  const volumeData = [
    { day: 'Mon', ingested: 250000, processed: 245000 },
    { day: 'Tue', ingested: 280000, processed: 275000 },
    { day: 'Wed', ingested: 300000, processed: 295000 },
    { day: 'Thu', ingested: 320000, processed: 315000 },
    { day: 'Fri', ingested: 290000, processed: 285000 }
  ];

  const sourceDistribution = [
    { name: 'API', value: 45 },
    { name: 'Database', value: 30 },
    { name: 'Files', value: 15 },
    { name: 'Streams', value: 10 }
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  const handleRunPipeline = useCallback((pipelineId) => {
    console.log(`Running pipeline: ${pipelineId}`);
    // API call would go here
    alert(`Pipeline ${pipelineId} execution started`);
  }, []);

  const handlePausePipeline = useCallback((pipelineId) => {
    console.log(`Pausing pipeline: ${pipelineId}`);
    // API call would go here
    alert(`Pipeline ${pipelineId} paused`);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'success': return '#10B981';
      case 'running': return '#3B82F6';
      case 'warning': return '#F59E0B';
      case 'error': return '#EF4444';
      default: return '#6B7280';
    }
  };

  return (
    <div className="b2b-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-left">
          <Database size={32} className="header-icon" />
          <div>
            <h1>B2B Data Flow Platform</h1>
            <p className="subtitle">Datalake • ETL • Warehousing • Analytics</p>
          </div>
        </div>
        <div className="header-right">
          <div className="header-stats">
            <div className="stat-item">
              <Activity size={20} />
              <span>{dataMetrics.totalIngested.toLocaleString()} Ingested</span>
            </div>
            <div className="stat-item">
              <RefreshCw size={20} />
              <span>{dataMetrics.successRate}% Success Rate</span>
            </div>
            <div className="stat-item">
              <Cpu size={20} />
              <span>{dataMetrics.avgLatency}ms Avg Latency</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Dashboard */}
      <div className="dashboard-grid">
        {/* Pipeline Overview */}
        <div className="dashboard-card full-width">
          <div className="card-header">
            <h2><Server size={20} /> Active Data Pipelines</h2>
            <button className="btn btn-primary">
              <RefreshCw size={16} /> Refresh All
            </button>
          </div>
          <div className="pipelines-grid">
            {pipelines.map(pipeline => (
              <div 
                key={pipeline.id}
                className={`pipeline-card ${pipeline.status}`}
                onClick={() => setActivePipeline(pipeline)}
              >
                <div className="pipeline-header">
                  <h3>{pipeline.name}</h3>
                  <span className={`status-badge ${pipeline.status}`}>
                    {pipeline.status === 'success' && <CheckCircle size={14} />}
                    {pipeline.status === 'warning' && <AlertTriangle size={14} />}
                    {pipeline.status === 'running' && <Activity size={14} />}
                    {pipeline.status}
                  </span>
                </div>
                <div className="pipeline-details">
                  <div className="detail-row">
                    <span>Source:</span>
                    <span className="value">{pipeline.source}</span>
                  </div>
                  <div className="detail-row">
                    <span>Destination:</span>
                    <span className="value">{pipeline.destination}</span>
                  </div>
                  <div className="detail-row">
                    <span>Last Run:</span>
                    <span className="value">{pipeline.lastRun}</span>
                  </div>
                  <div className="detail-row">
                    <span>Records:</span>
                    <span className="value">{pipeline.recordsProcessed.toLocaleString()}</span>
                  </div>
                  <div className="detail-row">
                    <span>Success Rate:</span>
                    <span className="value">{pipeline.successRate}%</span>
                  </div>
                </div>
                <div className="pipeline-actions">
                  <button 
                    className="btn btn-sm btn-primary"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleRunPipeline(pipeline.id);
                    }}
                  >
                    <RefreshCw size={14} /> Run Now
                  </button>
                  <button 
                    className="btn btn-sm btn-outline"
                    onClick={(e) => {
                      e.stopPropagation();
                      handlePausePipeline(pipeline.id);
                    }}
                  >
                    Pause
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="dashboard-card">
          <h2><BarChart3 size={20} /> Processing Latency</h2>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={latencyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="hour" />
              <YAxis label={{ value: 'ms', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Area type="monotone" dataKey="latency" stroke="#8884d8" fill="#8884d8" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Data Volume */}
        <div className="dashboard-card">
          <h2><Upload size={20} /> Data Volume</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={volumeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="ingested" fill="#8884d8" name="Ingested" />
              <Bar dataKey="processed" fill="#82ca9d" name="Processed" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Source Distribution */}
        <div className="dashboard-card">
          <h2><HardDrive size={20} /> Source Distribution</h2>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={sourceDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {sourceDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* System Health */}
        <div className="dashboard-card">
          <h2><Activity size={20} /> System Health</h2>
          <div className="health-grid">
            {Object.entries(systemHealth).map(([system, status]) => (
              <div key={system} className="health-item">
                <div className="health-label">
                  {system === 'datalake' && <HardDrive size={16} />}
                  {system === 'warehouse' && <Database size={16} />}
                  {system === 'etl' && <RefreshCw size={16} />}
                  {system === 'api' && <Network size={16} />}
                  <span>{system.charAt(0).toUpperCase() + system.slice(1)}</span>
                </div>
                <div className={`health-status ${status}`}>
                  <div className="status-dot" style={{ backgroundColor: getStatusColor(status) }} />
                  <span>{status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activities */}
        <div className="dashboard-card">
          <h2><Bell size={20} /> Recent Activities</h2>
          <div className="activities-list">
            {recentActivities.map(activity => (
              <div key={activity.id} className="activity-item">
                <div className="activity-info">
                  <strong>{activity.pipeline}</strong>
                  <span>{activity.action}</span>
                </div>
                <div className="activity-meta">
                  <span className="records">{activity.records.toLocaleString()} records</span>
                  <span className={`status ${activity.status}`}>
                    {activity.status === 'success' && <CheckCircle size={12} />}
                    {activity.status === 'warning' && <AlertTriangle size={12} />}
                    {activity.status}
                  </span>
                  <span className="time">{activity.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="dashboard-card">
          <h2><Settings size={20} /> Quick Actions</h2>
          <div className="actions-grid">
            <button className="action-btn">
              <Upload size={18} />
              <span>Trigger Ingestion</span>
            </button>
            <button className="action-btn">
              <RefreshCw size={18} />
              <span>Run ETL</span>
            </button>
            <button className="action-btn">
              <Database size={18} />
              <span>Refresh Warehouse</span>
            </button>
            <button className="action-btn">
              <AlertTriangle size={18} />
              <span>Run Quality Checks</span>
            </button>
            <button className="action-btn">
              <Download size={18} />
              <span>Export Reports</span>
            </button>
            <button className="action-btn">
              <Users size={18} />
              <span>Manage Clients</span>
            </button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="dashboard-footer">
        <div className="footer-info">
          <div className="info-item">
            <span className="label">Last Updated:</span>
            <span className="value">{new Date().toLocaleTimeString()}</span>
          </div>
          <div className="info-item">
            <span className="label">Platform:</span>
            <span className="value">B2B Data Flow v2.5.0</span>
          </div>
          <div className="info-item">
            <span className="label">Status:</span>
            <span className="value status-good">All Systems Operational</span>
          </div>
        </div>
        <div className="footer-links">
          <a href="#">Documentation</a>
          <a href="#">API Reference</a>
          <a href="#">Support</a>
          <a href="#">Settings</a>
        </div>
      </footer>
    </div>
  );
};

// Export styles (simplified)
const styles = `
.b2b-dashboard {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #f1f5f9;
  min-height: 100vh;
  padding: 20px;
}

.dashboard-header {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
  border: 1px solid #475569;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  color: #3b82f6;
}

.subtitle {
  color: #94a3b8;
  font-size: 14px;
  margin-top: 4px;
}

.header-stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #cbd5e1;
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-outline {
  background: transparent;
  border: 1px solid #475569;
  color: #cbd5e1;
}

.pipelines-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.pipeline-card {
  background: rgba(15, 23, 42, 0.8);
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.pipeline-card:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.pipeline-card.running {
  border-left: 4px solid #3b82f6;
}

.pipeline-card.success {
  border-left: 4px solid #10b981;
}

.pipeline-card.warning {
  border-left: 4px solid #f59e0b;
}

.pipeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.status-badge.success {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.status-badge.running {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.status-badge.warning {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-size: 14px;
}

.detail-row .value {
  color: #cbd5e1;
  font-weight: 500;
}

.pipeline-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.health-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.health-item {
  background: rgba(15, 23, 42, 0.8);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.health-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.health-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.activities-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.activity-item {
  background: rgba(15, 23, 42, 0.8);
  border-radius: 8px;
  padding: 12px;
}

.activity-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.activity-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #94a3b8;
}

.status.success {
  color: #10b981;
}

.status.warning {
  color: #f59e0b;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.action-btn {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid #475569;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.dashboard-footer {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #475569;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-info {
  display: flex;
  gap: 30px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.label {
  font-size: 12px;
  color: #94a3b8;
}

.value {
  font-size: 14px;
  color: #cbd5e1;
}

.status-good {
  color: #10b981;
  font-weight: 500;
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-links a {
  color: #94a3b8;
  text-decoration: none;
  font-size: 14px;
}

.footer-links a:hover {
  color: #3b82f6;
}
`;

export default B2BDataDashboard;
