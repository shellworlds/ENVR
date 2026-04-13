import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [noiseScore, setNoiseScore] = useState(0.0);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/v1/noise/current');
        setNoiseScore(res.data.score);
      } catch (e) {
        console.error('API unreachable');
      }
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Kryptur PT-OF 1.6 Dashboard</h1>
      <div>Noise Likelihood Score: {noiseScore.toFixed(3)}</div>
    </div>
  );
}

export default App;
