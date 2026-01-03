/**
 * Next.js: Client Encryption Dashboard Page
 * Server-side rendered encryption management
 */
import { GetServerSideProps } from 'next';
import { useState } from 'react';
import EncryptionDashboard from '../components/EncryptionDashboard';
import { 
  getClients, 
  getEncryptionStats, 
  getRecentActivities,
  Client,
  EncryptionStats 
} from '../lib/encryption-api';

interface Props {
  initialClients: Client[];
  initialStats: EncryptionStats;
  initialActivities: any[];
}

export default function EncryptionPage({ 
  initialClients, 
  initialStats, 
  initialActivities 
}: Props) {
  const [clients, setClients] = useState(initialClients);
  const [stats, setStats] = useState(initialStats);
  
  return (
    <div className="min-h-screen bg-gray-50">
      <EncryptionDashboard 
        clients={clients}
        stats={stats}
        activities={initialActivities}
      />
    </div>
  );
}

export const getServerSideProps: GetServerSideProps = async () => {
  try {
    const [clients, stats, activities] = await Promise.all([
      getClients(),
      getEncryptionStats(),
      getRecentActivities()
    ]);
    
    return {
      props: {
        initialClients: clients,
        initialStats: stats,
        initialActivities: activities
      }
    };
  } catch (error) {
    return {
      props: {
        initialClients: [],
        initialStats: {},
        initialActivities: []
      }
    };
  }
};
