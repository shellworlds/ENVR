/**
 * Node.js: Client Encryption API Server
 * REST API for client encryption management
 */
const express = require('express');
const crypto = require('crypto');
const fs = require('fs').promises;
const path = require('path');
const winston = require('winston');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'logs/encryption-api.log' }),
        new winston.transports.Console({ format: winston.format.simple() })
    ]
});

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req, res, next) => {
    logger.info({
        method: req.method,
        url: req.url,
        clientId: req.headers['x-client-id'] || 'unknown',
        timestamp: new Date().toISOString()
    });
    next();
});

// Security headers middleware
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-XSS-Protection', '1; mode=block');
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    next();
});

// Data directories
const DATA_DIR = './data';
const KEY_STORE = path.join(DATA_DIR, 'keys');
const AUDIT_LOG = path.join(DATA_DIR, 'audit.log');

// Ensure directories exist
const initDirectories = async () => {
    await fs.mkdir(DATA_DIR, { recursive: true });
    await fs.mkdir(KEY_STORE, { recursive: true });
    logger.info('Directories initialized');
};

// Encryption service
class EncryptionService {
    constructor() {
        this.algorithms = {
            'aes-256-gcm': { keyLength: 32, ivLength: 12, tagLength: 16 },
            'aes-256-cbc': { keyLength: 32, ivLength: 16 },
            'chacha20-poly1305': { keyLength: 32, ivLength: 12, tagLength: 16 }
        };
    }

    async generateKey(algorithm = 'aes-256-gcm') {
        const algo = this.algorithms[algorithm];
        if (!algo) {
            throw new Error(`Unsupported algorithm: ${algorithm}`);
        }

        const key = crypto.randomBytes(algo.keyLength);
        const keyId = `key_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
        
        return {
            keyId,
            algorithm,
            key: key.toString('base64'),
            created: new Date().toISOString()
        };
    }

    async encryptText(text, key, algorithm = 'aes-256-gcm') {
        const algo = this.algorithms[algorithm];
        const iv = crypto.randomBytes(algo.ivLength);
        
        let cipher;
        switch (algorithm) {
            case 'aes-256-gcm':
                cipher = crypto.createCipheriv('aes-256-gcm', Buffer.from(key, 'base64'), iv);
                break;
            case 'aes-256-cbc':
                cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key, 'base64'), iv);
                break;
            case 'chacha20-poly1305':
                cipher = crypto.createCipheriv('chacha20-poly1305', Buffer.from(key, 'base64'), iv);
                break;
            default:
                throw new Error(`Unsupported algorithm: ${algorithm}`);
        }

        let encrypted = cipher.update(text, 'utf8', 'base64');
        encrypted += cipher.final('base64');

        const result = {
            ciphertext: encrypted,
            iv: iv.toString('base64'),
            algorithm,
            timestamp: new Date().toISOString()
        };

        if (algo.tagLength) {
            result.tag = cipher.getAuthTag().toString('base64');
        }

        return result;
    }

    async decryptText(encryptedData, key) {
        const { ciphertext, iv, algorithm, tag } = encryptedData;
        const algo = this.algorithms[algorithm];
        
        let decipher;
        switch (algorithm) {
            case 'aes-256-gcm':
                decipher = crypto.createDecipheriv('aes-256-gcm', Buffer.from(key, 'base64'), Buffer.from(iv, 'base64'));
                if (tag) decipher.setAuthTag(Buffer.from(tag, 'base64'));
                break;
            case 'aes-256-cbc':
                decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key, 'base64'), Buffer.from(iv, 'base64'));
                break;
            case 'chacha20-poly1305':
                decipher = crypto.createDecipheriv('chacha20-poly1305', Buffer.from(key, 'base64'), Buffer.from(iv, 'base64'));
                if (tag) decipher.setAuthTag(Buffer.from(tag, 'base64'));
                break;
            default:
                throw new Error(`Unsupported algorithm: ${algorithm}`);
        }

        let decrypted = decipher.update(ciphertext, 'base64', 'utf8');
        decrypted += decipher.final('utf8');

        return decrypted;
    }

    async generateRSAKeyPair(keySize = 4096) {
        return new Promise((resolve, reject) => {
            crypto.generateKeyPair('rsa', {
                modulusLength: keySize,
                publicKeyEncoding: {
                    type: 'spki',
                    format: 'pem'
                },
                privateKeyEncoding: {
                    type: 'pkcs8',
                    format: 'pem'
                }
            }, (err, publicKey, privateKey) => {
                if (err) reject(err);
                else resolve({ publicKey, privateKey });
            });
        });
    }
}

// Client manager
class ClientManager {
    constructor() {
        this.clients = new Map();
        this.encryptionService = new EncryptionService();
    }

    async registerClient(clientData) {
        const clientId = `client_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
        const client = {
            id: clientId,
            ...clientData,
            createdAt: new Date().toISOString(),
            status: 'active',
            keys: []
        };

        this.clients.set(clientId, client);
        await this.logAudit('client_registered', clientId, clientData);
        
        return client;
    }

    async generateClientKey(clientId, algorithm = 'aes-256-gcm') {
        const client = this.clients.get(clientId);
        if (!client) throw new Error('Client not found');

        const keyData = await this.encryptionService.generateKey(algorithm);
        client.keys.push(keyData);

        await this.saveClientData(clientId);
        await this.logAudit('key_generated', clientId, { algorithm, keyId: keyData.keyId });

        return keyData;
    }

    async encryptForClient(clientId, plaintext, keyId = null) {
        const client = this.clients.get(clientId);
        if (!client) throw new Error('Client not found');

        let keyData;
        if (keyId) {
            keyData = client.keys.find(k => k.keyId === keyId);
        } else {
            // Use latest key
            keyData = client.keys[client.keys.length - 1];
        }

        if (!keyData) throw new Error('No encryption key found');

        const encrypted = await this.encryptionService.encryptText(
            plaintext, 
            keyData.key, 
            keyData.algorithm
        );

        await this.logAudit('data_encrypted', clientId, {
            keyId: keyData.keyId,
            dataSize: plaintext.length,
            algorithm: keyData.algorithm
        });

        return {
            ...encrypted,
            keyId: keyData.keyId,
            clientId
        };
    }

    async decryptForClient(clientId, encryptedData) {
        const client = this.clients.get(clientId);
        if (!client) throw new Error('Client not found');

        const keyData = client.keys.find(k => k.keyId === encryptedData.keyId);
        if (!keyData) throw new Error('Encryption key not found');

        const decrypted = await this.encryptionService.decryptText(
            encryptedData,
            keyData.key
        );

        await this.logAudit('data_decrypted', clientId, {
            keyId: keyData.keyId,
            dataSize: decrypted.length
        });

        return decrypted;
    }

    async rotateClientKeys(clientId) {
        const client = this.clients.get(clientId);
        if (!client) throw new Error('Client not found');

        // Generate new key using same algorithm as last key
        const lastKey = client.keys[client.keys.length - 1];
        const newKey = await this.generateClientKey(clientId, lastKey.algorithm);

        // Mark old keys for deletion (after grace period)
        client.keys.forEach(key => {
            if (key.keyId !== newKey.keyId) {
                key.status = 'deprecated';
            }
        });

        await this.saveClientData(clientId);
        await this.logAudit('keys_rotated', clientId, {
            oldKeys: client.keys.length - 1,
            newKeyId: newKey.keyId
        });

        return {
            newKey,
            deprecatedKeys: client.keys.filter(k => k.status === 'deprecated').length
        };
    }

    async getClientCompliance(clientId) {
        const client = this.clients.get(clientId);
        if (!client) throw new Error('Client not found');

        const now = new Date();
        const keyAge = client.keys.map(k => {
            const created = new Date(k.created);
            const ageDays = (now - created) / (1000 * 60 * 60 * 24);
            return { keyId: k.keyId, ageDays };
        });

        const compliance = {
            clientId,
            totalKeys: client.keys.length,
            activeKeys: client.keys.filter(k => k.status !== 'deprecated').length,
            keyRotationNeeded: keyAge.some(k => k.ageDays > 90),
            lastAudit: client.lastAudit || 'Never',
            complianceScore: this.calculateComplianceScore(client)
        };

        return compliance;
    }

    calculateComplianceScore(client) {
        let score = 100;
        
        // Deduct for old keys
        const now = new Date();
        client.keys.forEach(key => {
            const age = (now - new Date(key.created)) / (1000 * 60 * 60 * 24);
            if (age > 90) score -= 10;
            if (age > 180) score -= 20;
        });

        // Deduct for missing audit
        if (!client.lastAudit) score -= 15;

        return Math.max(0, score);
    }

    async saveClientData(clientId) {
        const client = this.clients.get(clientId);
        const filePath = path.join(KEY_STORE, `${clientId}.json`);
        
        // Don't save actual keys to disk in production
        const safeClient = {
            ...client,
            keys: client.keys.map(k => ({
                keyId: k.keyId,
                algorithm: k.algorithm,
                created: k.created,
                status: k.status
                // Note: Not saving actual key material
            }))
        };

        await fs.writeFile(filePath, JSON.stringify(safeClient, null, 2));
    }

    async logAudit(action, clientId, details) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            action,
            clientId,
            details,
            userAgent: 'encryption-api'
        };

        await fs.appendFile(AUDIT_LOG, JSON.stringify(logEntry) + '\n');
        logger.info(`Audit: ${action} for ${clientId}`, details);
    }
}

// Initialize services
const clientManager = new ClientManager();

// API Routes

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'client-encryption-api',
        version: '1.0.0'
    });
});

// Register new client
app.post('/api/clients', async (req, res) => {
    try {
        const clientData = req.body;
        const client = await clientManager.registerClient(clientData);
        
        res.status(201).json({
            success: true,
            message: 'Client registered successfully',
            client: {
                id: client.id,
                name: client.name,
                encryptionType: client.encryptionType,
                status: client.status
            }
        });
    } catch (error) {
        logger.error('Client registration failed:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Generate encryption key for client
app.post('/api/clients/:clientId/keys', async (req, res) => {
    try {
        const { clientId } = req.params;
        const { algorithm = 'aes-256-gcm' } = req.body;
        
        const keyData = await clientManager.generateClientKey(clientId, algorithm);
        
        res.json({
            success: true,
            message: 'Encryption key generated',
            key: {
                keyId: keyData.keyId,
                algorithm: keyData.algorithm,
                created: keyData.created
            }
        });
    } catch (error) {
        logger.error('Key generation failed:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Encrypt data
app.post('/api/clients/:clientId/encrypt', async (req, res) => {
    try {
        const { clientId } = req.params;
        const { plaintext, keyId } = req.body;
        
        if (!plaintext) {
            return res.status(400).json({
                success: false,
                error: 'Plaintext is required'
            });
        }

        const encrypted = await clientManager.encryptForClient(clientId, plaintext, keyId);
        
        res.json({
            success: true,
            message: 'Data encrypted successfully',
            encrypted
        });
    } catch (error) {
        logger.error('Encryption failed:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Decrypt data
app.post('/api/clients/:clientId/decrypt', async (req, res) => {
    try {
        const { clientId } = req.params;
        const encryptedData = req.body;
        
        const decrypted = await clientManager.decryptForClient(clientId, encryptedData);
        
        res.json({
            success: true,
            message: 'Data decrypted successfully',
            decrypted
        });
    } catch (error) {
        logger.error('Decryption failed:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Rotate client keys
app.post('/api/clients/:clientId/keys/rotate', async (req, res) => {
    try {
        const { clientId } = req.params;
        
        const rotationResult = await clientManager.rotateClientKeys(clientId);
        
        res.json({
            success: true,
            message: 'Keys rotated successfully',
            ...rotationResult
        });
    } catch (error) {
        logger.error('Key rotation failed:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get client compliance report
app.get('/api/clients/:clientId/compliance', async (req, res) => {
    try {
        const { clientId } = req.params;
        
        const compliance = await clientManager.getClientCompliance(clientId);
        
        res.json({
            success: true,
            compliance
        });
    } catch (error) {
        logger.error('Compliance check failed:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// List all clients
app.get('/api/clients', (req, res) => {
    const clients = Array.from(clientManager.clients.values()).map(client => ({
        id: client.id,
        name: client.name,
        encryptionType: client.encryptionType,
        status: client.status,
        keyCount: client.keys.length,
        createdAt: client.createdAt
    }));
    
    res.json({
        success: true,
        clients,
        count: clients.length
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    logger.error('Unhandled error:', err);
    res.status(500).json({
        success: false,
        error: 'Internal server error',
        message: err.message
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        error: 'Endpoint not found'
    });
});

// Start server
const startServer = async () => {
    await initDirectories();
    
    app.listen(PORT, () => {
        logger.info(`Client Encryption API server running on port ${PORT}`);
        console.log(`
        🚀 Client Encryption API Server
        =================================
        📍 Port: ${PORT}
        📁 Data: ${DATA_DIR}
        📝 Logs: ./logs/
        
        Available endpoints:
        GET  /health                    - Health check
        POST /api/clients               - Register new client
        POST /api/clients/:id/keys      - Generate encryption key
        POST /api/clients/:id/encrypt   - Encrypt data
        POST /api/clients/:id/decrypt   - Decrypt data
        POST /api/clients/:id/keys/rotate - Rotate keys
        GET  /api/clients/:id/compliance - Compliance report
        GET  /api/clients               - List all clients
        
        Ready for client encryption management!
        `);
    });
};

startServer().catch(console.error);

module.exports = app; // For testing
