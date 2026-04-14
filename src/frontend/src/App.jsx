import React, { useState, useEffect } from 'react';

function App() {
  const [status, setStatus] = useState({ mxc_temp_mk: 0, jpa_bias_ma: 0 });

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch('/v1/status');
        const data = await res.json();
        setStatus(data);
      } catch (e) {
        console.error('API error', e);
      }
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>AE Kryptur Dashboard</h1>
      <p>MXC Temperature: {status.mxc_temp_mk.toFixed(2)} mK</p>
      <p>JPA Bias: {status.jpa_bias_ma.toFixed(3)} mA</p>
    </div>
  );
}

export default App;
