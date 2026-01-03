/**
 * React: Client Encryption Dashboard
 * Real-time encryption monitoring and management interface
 */
import React, { useState, useEffect, useCallback } from 'react';
import { 
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { 
  Shield, Key, Lock, Unlock, RotateCw, FileText, AlertTriangle,
  CheckCircle, XCircle, Activity, Database, Users 
} from 'lucide-react';
import './styles/EncryptionDashboard.css';

const EncryptionDashboard = () => {
  const [clients, setClients] = useState([]);
  const [activeClient, setActiveClient] = useState(null);
  const [encryptionStats, setEncryptionStats] = useState({
    totalEncrypted: 0,
    activeKeys: 0,
    complianceScore: 0,
    lastAudit: ''
  });
  
  const [recentActivities, setRecentActivities] = useState([]);
  const [keyRotationSchedule, setKeyRotationSchedule] = useState([]);
  const [systemHealth, setSystemHealth] = useState({
    status: 'healthy',
    issues: []
  });

  // Mock data - replace with API calls
  useEffect(() => {
    // Load clients
    const mockClients = [
      {
        id: 'fintech_corp',
        name: 'FinTech Corp',
        encryptionType: 'AES-256-GCM',
        compliance: 'PCI-DSS',
        dataClassification: 'Highly Sensitive',
        keyRotationDays: 30,
        lastAudit: '2024-01-15',
        status: 'active'
      },
      {
        id: 'healthcare_inc',
        name: 'Healthcare Inc',
        encryptionType: 'RSA-4096',
        compliance: 'HIPAA',
        dataClassification: 'Protected Health',
        keyRotationDays: 60,
        lastAudit: '2024-01-10',
        status: 'active'
      },
      {
        id: 'ecommerce_global',
        name: 'Ecommerce Global',
        encryptionType: 'ChaCha20-Poly1305',
        compliance: 'GDPR',
        dataClassification: 'Personal Data',
        keyRotationDays: 90,
        lastAudit: '2024-01-05',
        status: 'warning'
      }
    ];
    
    setClients(mockClients);
    setActiveClient(mockClients[0]);
    
    // Load stats
    setEncryptionStats({
      totalEncrypted: 15423,
      activeKeys: 42,
      complianceScore: 94,
      lastAudit: '2024-01-15'
    });
    
    // Load recent activities
    setRecentActivities([
      { id: 1, client: 'FinTech Corp', action: 'Key Rotation', timestamp: '10 min ago', status: 'success' },
      { id: 2, client: 'Healthcare Inc', action: 'File Encryption', timestamp: '25 min ago', status: 'success' },
      { id: 3, client: 'Ecommerce Global', action: 'Compliance Scan', timestamp: '1 hour ago', status: 'warning' },
      { id: 4, client: 'FinTech Corp', action: 'Audit Log Export', timestamp: '2 hours ago', status: 'success' }
    ]);
    
    // Key rotation schedule
    setKeyRotationSchedule([
      { client: 'FinTech Corp', nextRotation: '2024-02-15', daysLeft: 15 },
      { client: 'Healthcare Inc', nextRotation: '2024-03-10', daysLeft: 45 },
      { client: 'Ecommerce Global', nextRotation: '2024-04-05', daysLeft: 71 }
    ]);
    
    // System health
    setSystemHealth({
      status: 'healthy',
      issues: [
        { component: 'Key Storage', status: 'operational' },
        { component: 'Audit System', status: 'operational' },
        { component: 'Backup Service', status: 'warning' }
      ]
    });
  }, []);

  const handleEncryptFile = useCallback(async (clientId, file) => {
    console.log(`Encrypting file for ${clientId}:`, file.name);
    // API call would go here
    alert(`Encryption request sent for ${clientId}`);
  }, []);

  const handleRotateKeys = useCallback(async (clientId) => {
    console.log(`Rotating keys for ${clientId}`);
    // API call would go here
    alert(`Key rotation initiated for ${clientId}`);
  }, []);

  const handleGenerateReport = useCallback(async (clientId) => {
    console.log(`Generating report for ${clientId}`);
    // API call would go here
    alert(`Compliance report generated for ${clientId}`);
  }, []);

  // Chart data
  const encryptionData = [
    { name: 'AES-256-GCM', value: 65 },
    { name: 'RSA-4096', value: 20 },
    { name: 'ChaCha20', value: 10 },
    { name: 'Other', value: 5 }
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  const activityData = [
    { day: 'Mon', encryptions: 2400, decryptions: 1800 },
    { day: 'Tue', encryptions: 3200, decryptions: 2200 },
    { day: 'Wed', encryptions: 2800, decryptions: 1900 },
    { day: 'Thu', encryptions: 3500, decryptions: 2500 },
    { day: 'Fri', encryptions: 2900, decryptions: 2100 }
  ];

  return (
    <div className="encryption-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-title">
          <Shield size={32} className="header-icon" />
          <h1>Client Encryption Management System</h1>
        </div>
        <div className="header-stats">
          <div className="stat-item">
            <Key size={20} />
            <span>{encryptionStats.activeKeys} Active Keys</span>
          </div>
          <div className="stat-item">
            <Lock size={20} />
            <span>{encryptionStats.totalEncrypted.toLocaleString()} Files Encrypted</span>
          </div>
          <div className="stat-item">
            <CheckCircle size={20} />
            <span>{encryptionStats.complianceScore}% Compliance</span>
          </div>
        </div>
      </header>

      {/* Main Dashboard */}
      <div className="dashboard-grid">
        {/* Client Selection Panel */}
        <div className="dashboard-card clients-panel">
          <h2><Users size={20} /> Managed Clients</h2>
          <div className="clients-list">
            {clients.map(client => (
              <div 
                key={client.id}
                className={`client-item ${activeClient?.id === client.id ? 'active' : ''} ${client.status}`}
                onClick={() => setActiveClient(client)}
              >
                <div className="client-info">
                  <h3>{client.name}</h3>
                  <div className="client-tags">
                    <span className="tag encryption">{client.encryptionType}</span>
                    <span className="tag compliance">{client.compliance}</span>
                    <span className="tag classification">{client.dataClassification}</span>
                  </div>
                </div>
                <div className="client-status">
                  {client.status === 'active' && <CheckCircle size={16} color="#10B981" />}
                  {client.status === 'warning' && <AlertTriangle size={16} color="#F59E0B" />}
                  <span>Rotation in {client.keyRotationDays} days</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Active Client Details */}
        {activeClient && (
          <div className="dashboard-card client-details">
            <h2><Database size={20} /> {activeClient.name} - Encryption Details</h2>
            <div className="detail-grid">
              <div className="detail-item">
                <strong>Encryption Type:</strong>
                <span className="value">{activeClient.encryptionType}</span>
              </div>
              <div className="detail-item">
                <strong>Compliance Standard:</strong>
                <span className="value">{activeClient.compliance}</span>
              </div>
              <div className="detail-item">
                <strong>Data Classification:</strong>
                <span className="value">{activeClient.dataClassification}</span>
              </div>
              <div className="detail-item">
                <strong>Key Rotation:</strong>
                <span className="value">Every {activeClient.keyRotationDays} days</span>
              </div>
              <div className="detail-item">
                <strong>Last Audit:</strong>
                <span className="value">{activeClient.lastAudit}</span>
              </div>
            </div>
            
            <div className="client-actions">
              <button 
                className="btn btn-primary"
                onClick={() => handleRotateKeys(activeClient.id)}
              >
                <RotateCw size={16} /> Rotate Keys
              </button>
              <button 
                className="btn btn-secondary"
                onClick={() => handleGenerateReport(activeClient.id)}
              >
                <FileText size={16} /> Generate Report
              </button>
              <div className="file-upload">
                <input 
                  type="file" 
                  id="encrypt-file"
                  onChange={(e) => handleEncryptFile(activeClient.id, e.target.files[0])}
                />
                <label htmlFor="encrypt-file" className="btn btn-outline">
                  <Lock size={16} /> Encrypt File
                </label>
              </div>
            </div>
          </div>
        )}

        {/* Encryption Statistics */}
        <div className="dashboard-card">
          <h2><Activity size={20} /> Encryption Statistics</h2>
          <div className="stats-charts">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={encryptionData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {encryptionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Activity Chart */}
        <div className="dashboard-card">
          <h2>📈 Daily Activity</h2>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={activityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="encryptions" stroke="#8884d8" strokeWidth={2} />
              <Line type="monotone" dataKey="decryptions" stroke="#82ca9d" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Recent Activities */}
        <div className="dashboard-card">
          <h2>🔄 Recent Activities</h2>
          <div className="activities-list">
            {recentActivities.map(activity => (
              <div key={activity.id} className="activity-item">
                <div className="activity-info">
                  <strong>{activity.client}</strong>
                  <span>{activity.action}</span>
                </div>
                <div className="activity-meta">
                  <span className="timestamp">{activity.timestamp}</span>
                  <span className={`status ${activity.status}`}>
                    {activity.status === 'success' && <CheckCircle size={14} />}
                    {activity.status === 'warning' && <AlertTriangle size={14} />}
                    {activity.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Key Rotation Schedule */}
        <div className="dashboard-card">
          <h2><RotateCw size={20} /> Key Rotation Schedule</h2>
          <div className="rotation-schedule">
            {keyRotationSchedule.map((item, index) => (
              <div key={index} className="rotation-item">
                <div className="rotation-client">{item.client}</div>
                <div className="rotation-details">
                  <span>Next: {item.nextRotation}</span>
                  <span className={`days-left ${item.daysLeft < 30 ? 'urgent' : ''}`}>
                    {item.daysLeft} days left
                  </span>
                </div>
                <button 
                  className="btn btn-sm"
                  onClick={() => handleRotateKeys(item.client.toLowerCase().replace(' ', '_'))}
                >
                  Rotate Now
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* System Health */}
        <div className="dashboard-card">
          <h2>🩺 System Health</h2>
          <div className="health-status">
            <div className={`health-indicator ${systemHealth.status}`}>
              {systemHealth.status === 'healthy' && <CheckCircle size={24} />}
              {systemHealth.status === 'warning' && <AlertTriangle size={24} />}
              <span>Overall Status: {systemHealth.status.toUpperCase()}</span>
            </div>
            <div className="health-components">
              {systemHealth.issues.map((issue, index) => (
                <div key={index} className={`health-component ${issue.status}`}>
                  <span>{issue.component}</span>
                  <span className="status-badge">{issue.status}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions Footer */}
      <footer className="dashboard-footer">
        <div className="quick-actions">
          <button className="btn btn-primary">
            <Shield size={16} /> Run Security Audit
          </button>
          <button className="btn btn-secondary">
            <FileText size={16} /> Export All Reports
          </button>
          <button className="btn btn-outline">
            <Database size={16} /> Backup Configuration
          </button>
        </div>
        <div className="system-info">
          <span>Last Updated: {new Date().toLocaleTimeString()}</span>
          <span>Version: 2.4.1</span>
          <span>Encryption Framework: FIPS 140-2 Compliant</span>
        </div>
      </footer>
    </div>
  );
};

// Export styles (simplified)
const styles = `
.encryption-dashboard {
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

.btn {
  padding: 10px 20px;
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

.clients-panel {
  grid-column: span 2;
}

.client-item {
  background: rgba(15, 23, 42, 0.8);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.client-item:hover {
  border-color: #3b82f6;
}

.client-item.active {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.client-tags {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.tag.encryption {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.tag.compliance {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.tag.classification {
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status.success {
  color: #10b981;
}

.status.warning {
  color: #f59e0b;
}

.rotation-item {
  background: rgba(15, 23, 42, 0.8);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.days-left.urgent {
  color: #ef4444;
  font-weight: 600;
}

.health-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.health-indicator.healthy {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.health-indicator.warning {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.dashboard-footer {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #475569;
}

.quick-actions {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.system-info {
  display: flex;
  justify-content: space-between;
  color: #94a3b8;
  font-size: 14px;
}
`;

// Export component
export default EncryptionDashboard;
