// ENVR9 Node.js Survey Server
const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.get('/', (req, res) => {
    res.json({
        service: 'ENVR9 Node.js Survey Server',
        status: 'active',
        version: '1.0.0'
    });
});

app.get('/api/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        nodeVersion: process.version
    });
});

app.get('/api/tools', (req, res) => {
    res.json({
        tools: [
            { name: 'Node.js', purpose: 'JavaScript runtime' },
            { name: 'Express.js', purpose: 'Web framework' },
            { name: 'Docker', purpose: 'Container platform' },
            { name: 'Git', purpose: 'Version control' }
        ]
    });
});

app.listen(port, () => {
    console.log(`ENVR9 Node.js server running on port ${port}`);
});
