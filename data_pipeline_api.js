/**
 * Node.js: B2B Data Pipeline API Server
 * REST API for datalake, ETL, and warehouse operations
 */
const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3001;

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'logs/data-pipeline-api.log' }),
        new winston.transports.Console({ format: winston.format.simple() })
    ]
});

// Middleware
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req, res, next) => {
    logger.info({
        method: req.method,
        url: req.url,
        client: req.headers['x-client-id'] || 'unknown',
        timestamp: new Date().toISOString()
    });
    next();
});

// Data directories
const DATA_DIR = './data_pipeline';
const PIPELINES_DIR = path.join(DATA_DIR, 'pipelines');
const METRICS_DIR = path.join(DATA_DIR, 'metrics');
const LOGS_DIR = path.join(DATA_DIR, 'logs');

// Ensure directories exist
const initDirectories = async () => {
    await fs.mkdir(DATA_DIR, { recursive: true });
    await fs.mkdir(PIPELINES_DIR, { recursive: true });
    await fs.mkdir(METRICS_DIR, { recursive: true });
    await fs.mkdir(LOGS_DIR, { recursive: true });
    logger.info('Data pipeline directories initialized');
};

// Data Pipeline Manager
class PipelineManager {
    constructor() {
        this.pipelines = new Map();
        this.metrics = {
            totalIngested: 0,
            totalProcessed: 0,
            successfulRuns: 0,
            failedRuns: 0
        };
    }

    async createPipeline(pipelineConfig) {
        const pipelineId = `pipeline_${uuidv4().slice(0, 8)}`;
        
        const pipeline = {
            id: pipelineId,
            ...pipelineConfig,
            createdAt: new Date().toISOString(),
            status: 'active',
            lastRun: null,
            nextRun: this.calculateNextRun(pipelineConfig.schedule),
            runs: []
        };

        this.pipelines.set(pipelineId, pipeline);
        await this.savePipeline(pipelineId);
        
        logger.info(`Pipeline created: ${pipelineId}`, { client: pipelineConfig.clientId });
        
        return pipeline;
    }

    calculateNextRun(schedule) {
        // Simplified schedule calculation
        // In production: Use cron-parser or similar
        const now = new Date();
        const nextRun = new Date(now);
        nextRun.setHours(nextRun.getHours() + 1); // Default: hourly
        return nextRun.toISOString();
    }

    async executePipeline(pipelineId, manualTrigger = false) {
        const pipeline = this.pipelines.get(pipelineId);
        if (!pipeline) {
            throw new Error('Pipeline not found');
        }

        const runId = `run_${uuidv4().slice(0, 8)}`;
        const startTime = new Date();

        try {
            logger.info(`Starting pipeline execution: ${pipelineId}`, { runId });
            
            // Update pipeline status
            pipeline.status = 'running';
            pipeline.lastRun = startTime.toISOString();

            // Simulate pipeline execution steps
            const executionResult = await this.simulatePipelineExecution(pipeline);

            // Update metrics
            this.metrics.totalIngested += executionResult.recordsIngested;
            this.metrics.totalProcessed += executionResult.recordsProcessed;
            this.metrics.successfulRuns += 1;

            // Log run
            const run = {
                id: runId,
                pipelineId,
                startTime: startTime.toISOString(),
                endTime: new Date().toISOString(),
                status: 'success',
                recordsIngested: executionResult.recordsIngested,
                recordsProcessed: executionResult.recordsProcessed,
                executionTime: Date.now() - startTime.getTime(),
                triggeredBy: manualTrigger ? 'manual' : 'schedule'
            };

            pipeline.runs.push(run);
            pipeline.status = 'success';

            await this.savePipeline(pipelineId);
            await this.logPipelineRun(run);

            logger.info(`Pipeline execution successful: ${pipelineId}`, run);

            return {
                success: true,
                runId,
                ...run,
                pipelineName: pipeline.name
            };

        } catch (error) {
            // Handle execution failure
            this.metrics.failedRuns += 1;

            const run = {
                id: runId,
                pipelineId,
                startTime: startTime.toISOString(),
                endTime: new Date().toISOString(),
                status: 'failed',
                error: error.message,
                executionTime: Date.now() - startTime.getTime(),
                triggeredBy: manualTrigger ? 'manual' : 'schedule'
            };

            pipeline.runs.push(run);
            pipeline.status = 'failed';

            await this.savePipeline(pipelineId);
            await this.logPipelineRun(run);

            logger.error(`Pipeline execution failed: ${pipelineId}`, error);

            return {
                success: false,
                runId,
                ...run,
                pipelineName: pipeline.name
            };
        }
    }

    async simulatePipelineExecution(pipeline) {
        // Simulate different pipeline steps
        const steps = [
            { name: 'Extract', duration: 1000, records: 1000 },
            { name: 'Validate', duration: 500, records: 980 },
            { name: 'Transform', duration: 1500, records: 950 },
            { name: 'Load', duration: 800, records: 950 }
        ];

        for (const step of steps) {
            await new Promise(resolve => setTimeout(resolve, step.duration));
            logger.debug(`Pipeline step completed: ${step.name}`, {
                pipelineId: pipeline.id,
                step,
                clientId: pipeline.clientId
            });
        }

        return {
            recordsIngested: steps[0].records,
            recordsProcessed: steps[steps.length - 1].records
        };
    }

    async getPipelineMetrics(pipelineId) {
        const pipeline = this.pipelines.get(pipelineId);
        if (!pipeline) {
            throw new Error('Pipeline not found');
        }

        const runs = pipeline.runs.slice(-10); // Last 10 runs
        const successRate = runs.length > 0 
            ? (runs.filter(r => r.status === 'success').length / runs.length) * 100
            : 0;

        return {
            pipelineId,
            pipelineName: pipeline.name,
            totalRuns: pipeline.runs.length,
            successfulRuns: pipeline.runs.filter(r => r.status === 'success').length,
            failedRuns: pipeline.runs.filter(r => r.status === 'failed').length,
            successRate,
            avgExecutionTime: runs.length > 0
                ? runs.reduce((sum, r) => sum + r.executionTime, 0) / runs.length
                : 0,
            lastRun: pipeline.lastRun,
            nextRun: pipeline.nextRun
        };
    }

    async savePipeline(pipelineId) {
        const pipeline = this.pipelines.get(pipelineId);
        const filePath = path.join(PIPELINES_DIR, `${pipelineId}.json`);
        
        await fs.writeFile(filePath, JSON.stringify(pipeline, null, 2));
    }

    async logPipelineRun(run) {
        const logPath = path.join(LOGS_DIR, `${run.pipelineId}_${run.id}.json`);
        await fs.writeFile(logPath, JSON.stringify(run, null, 2));
    }

    getSystemMetrics() {
        return {
            ...this.metrics,
            activePipelines: Array.from(this.pipelines.values()).filter(p => p.status === 'active').length,
            totalPipelines: this.pipelines.size,
            timestamp: new Date().toISOString()
        };
    }
}

// Initialize pipeline manager
const pipelineManager = new PipelineManager();

// API Routes

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        service: 'b2b-data-pipeline-api',
        version: '1.0.0',
        timestamp: new Date().toISOString()
    });
});

// Create new pipeline
app.post('/api/pipelines', async (req, res) => {
    try {
        const pipelineConfig = req.body;
        
        // Validate required fields
        if (!pipelineConfig.name || !pipelineConfig.clientId || !pipelineConfig.sourceType) {
            return res.status(400).json({
                success: false,
                error: 'Missing required fields: name, clientId, sourceType'
            });
        }

        const pipeline = await pipelineManager.createPipeline(pipelineConfig);
        
        res.status(201).json({
            success: true,
            message: 'Pipeline created successfully',
            pipeline: {
                id: pipeline.id,
                name: pipeline.name,
                clientId: pipeline.clientId,
                status: pipeline.status,
                createdAt: pipeline.createdAt
            }
        });
    } catch (error) {
        logger.error('Pipeline creation failed:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Execute pipeline
app.post('/api/pipelines/:pipelineId/execute', async (req, res) => {
    try {
        const { pipelineId } = req.params;
        const { manual = false } = req.body;
        
        const result = await pipelineManager.executePipeline(pipelineId, manual);
        
        res.json({
            success: result.success,
            message: result.success ? 'Pipeline executed successfully' : 'Pipeline execution failed',
            ...result
        });
    } catch (error) {
        logger.error('Pipeline execution failed:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get pipeline metrics
app.get('/api/pipelines/:pipelineId/metrics', async (req, res) => {
    try {
        const { pipelineId } = req.params;
        
        const metrics = await pipelineManager.getPipelineMetrics(pipelineId);
        
        res.json({
            success: true,
            metrics
        });
    } catch (error) {
        logger.error('Failed to get pipeline metrics:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// List all pipelines
app.get('/api/pipelines', (req, res) => {
    const pipelines = Array.from(pipelineManager.pipelines.values()).map(p => ({
        id: p.id,
        name: p.name,
        clientId: p.clientId,
        sourceType: p.sourceType,
        destination: p.destination,
        status: p.status,
        lastRun: p.lastRun,
        nextRun: p.nextRun,
        createdAt: p.createdAt
    }));
    
    res.json({
        success: true,
        pipelines,
        count: pipelines.length
    });
});

// Get system metrics
app.get('/api/metrics/system', (req, res) => {
    const metrics = pipelineManager.getSystemMetrics();
    
    res.json({
        success: true,
        metrics
    });
});

// Get pipeline runs
app.get('/api/pipelines/:pipelineId/runs', async (req, res) => {
    try {
        const { pipelineId } = req.params;
        const { limit = 20 } = req.query;
        
        const pipeline = pipelineManager.pipelines.get(pipelineId);
        if (!pipeline) {
            return res.status(404).json({
                success: false,
                error: 'Pipeline not found'
            });
        }
        
        const runs = pipeline.runs
            .slice(-parseInt(limit))
            .map(r => ({
                id: r.id,
                status: r.status,
                startTime: r.startTime,
                endTime: r.endTime,
                executionTime: r.executionTime,
                recordsIngested: r.recordsIngested,
                recordsProcessed: r.recordsProcessed,
                triggeredBy: r.triggeredBy
            }));
        
        res.json({
            success: true,
            runs,
            count: runs.length
        });
    } catch (error) {
        logger.error('Failed to get pipeline runs:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Update pipeline configuration
app.put('/api/pipelines/:pipelineId', async (req, res) => {
    try {
        const { pipelineId } = req.params;
        const updates = req.body;
        
        const pipeline = pipelineManager.pipelines.get(pipelineId);
        if (!pipeline) {
            return res.status(404).json({
                success: false,
                error: 'Pipeline not found'
            });
        }
        
        // Update allowed fields
        const allowedUpdates = ['name', 'schedule', 'config', 'status'];
        Object.keys(updates).forEach(key => {
            if (allowedUpdates.includes(key)) {
                pipeline[key] = updates[key];
            }
        });
        
        if (updates.schedule) {
            pipeline.nextRun = pipelineManager.calculateNextRun(updates.schedule);
        }
        
        await pipelineManager.savePipeline(pipelineId);
        
        res.json({
            success: true,
            message: 'Pipeline updated successfully',
            pipeline: {
                id: pipeline.id,
                name: pipeline.name,
                status: pipeline.status,
                nextRun: pipeline.nextRun
            }
        });
    } catch (error) {
        logger.error('Pipeline update failed:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
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
        logger.info(`B2B Data Pipeline API server running on port ${PORT}`);
        console.log(`
        🚀 B2B Data Pipeline API Server
        =================================
        📍 Port: ${PORT}
        📁 Data: ${DATA_DIR}
        📝 Logs: ./logs/
        
        Available endpoints:
        GET  /health                    - Health check
        POST /api/pipelines             - Create pipeline
        POST /api/pipelines/:id/execute - Execute pipeline
        GET  /api/pipelines/:id/metrics - Pipeline metrics
        GET  /api/pipelines             - List pipelines
        GET  /api/metrics/system        - System metrics
        GET  /api/pipelines/:id/runs    - Pipeline runs
        PUT  /api/pipelines/:id         - Update pipeline
        
        Ready for B2B data operations!
        `);
    });
};

startServer().catch(console.error);

module.exports = app; // For testing
