// File: module_api.js
// Language: JavaScript/Node.js
// Purpose: Web API for module operations

const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

// In-memory storage for modules
let modules = [];
let rings = [];

// Ring model
class Ring {
    constructor(id, name, isLocal) {
        this.id = id;
        this.name = name;
        this.isLocal = isLocal;
    }
}

// Module model
class Module {
    constructor(id, name, ringId, isProjective, isFree, generators = []) {
        this.id = id;
        this.name = name;
        this.ringId = ringId;
        this.isProjective = isProjective;
        this.isFree = isFree;
        this.generators = generators;
        this.theorems = [];
    }

    // Theorem 1: Lifting property
    verifyLiftingProperty() {
        if (this.isProjective) {
            return {
                theorem: "Lifting Property",
                status: "Verified",
                description: "Given surjection ψ: M → N and map ν: P → N, ∃ μ: P → M such that ψ∘μ = ν"
            };
        }
        return { theorem: "Lifting Property", status: "Failed", description: "Module not projective" };
    }

    // Theorem 2: Splitting property
    verifySplittingProperty() {
        if (this.isProjective) {
            return {
                theorem: "Splitting Property",
                status: "Verified",
                description: "Every short exact sequence 0 → L → M → P → 0 splits"
            };
        }
        return { theorem: "Splitting Property", status: "Failed", description: "Module not projective" };
    }

    // Theorem 3: Direct summand of free
    verifyDirectSummand() {
        if (this.isProjective) {
            return {
                theorem: "Direct Summand of Free",
                status: "Verified",
                description: "P is isomorphic to a direct summand of a free module F"
            };
        }
        return { theorem: "Direct Summand of Free", status: "Failed", description: "Module not projective" };
    }

    // Theorem 4: Local ring case
    verifyLocalFree(ring) {
        if (this.isProjective && ring.isLocal && this.generators.length > 0) {
            return {
                theorem: "Local Ring Theorem",
                status: "Verified",
                description: `Over local ring ${ring.name}, finitely generated projective module is FREE`
            };
        }
        return {
            theorem: "Local Ring Theorem",
            status: "Conditional",
            description: "Requires: projective + finitely generated + local ring"
        };
    }
}

// Initialize with sample data
function initializeData() {
    const localRing = new Ring(1, "A_local", true);
    rings.push(localRing);

    const projectiveModule = new Module(
        1,
        "P_finitely_generated",
        1,
        true,
        false,
        ["x1", "x2", "x3"]
    );
    modules.push(projectiveModule);
}

// API Routes

// Get all modules
app.get('/api/modules', (req, res) => {
    res.json({
        success: true,
        count: modules.length,
        modules: modules
    });
});

// Create new module
app.post('/api/modules', (req, res) => {
    const { name, ringId, isProjective, isFree, generators } = req.body;
    
    const newModule = new Module(
        modules.length + 1,
        name,
        ringId,
        isProjective || false,
        isFree || false,
        generators || []
    );
    
    modules.push(newModule);
    res.json({
        success: true,
        message: "Module created successfully",
        module: newModule
    });
});

// Verify theorems for a module
app.get('/api/modules/:id/theorems', (req, res) => {
    const moduleId = parseInt(req.params.id);
    const module = modules.find(m => m.id === moduleId);
    const ring = rings.find(r => r.id === module.ringId);

    if (!module) {
        return res.status(404).json({ success: false, message: "Module not found" });
    }

    const theorems = [
        module.verifyLiftingProperty(),
        module.verifySplittingProperty(),
        module.verifyDirectSummand(),
        module.verifyLocalFree(ring)
    ];

    res.json({
        success: true,
        module: module.name,
        theorems: theorems
    });
});

// Theorem explanation endpoint
app.get('/api/theorems/:theorem', (req, res) => {
    const theorem = req.params.theorem;
    const explanations = {
        'lifting': {
            name: "Lifting Property",
            statement: "P is projective iff given any surjection ψ: M → N and map ν: P → N, ∃ μ: P → M such that ψ∘μ = ν",
            significance: "Characterizes projective modules via diagram completion"
        },
        'splitting': {
            name: "Splitting Property",
            statement: "P is projective iff every short exact sequence 0 → L → M → P → 0 splits",
            significance: "Relates projectivity to decomposition of modules"
        },
        'direct-summand': {
            name: "Direct Summand of Free",
            statement: "P is projective iff P is a direct summand of a free module F",
            significance: "Connects projectivity to freeness"
        },
        'local': {
            name: "Local Ring Theorem",
            statement: "Over a local ring A, a finitely generated module P is projective iff it is free",
            significance: "Simplifies classification over local rings"
        }
    };

    const explanation = explanations[theorem] || {
        name: "Unknown Theorem",
        statement: "Theorem not found",
        significance: "Please check the theorem name"
    };

    res.json(explanation);
});

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        service: 'Module Theory API',
        version: '1.0.0',
        timestamp: new Date().toISOString()
    });
});

// Initialize and start server
initializeData();

app.listen(port, () => {
    console.log(`=== Module Theory API ===`);
    console.log(`Server running on port ${port}`);
    console.log(`Endpoints:`);
    console.log(`  GET /api/modules - List all modules`);
    console.log(`  POST /api/modules - Create new module`);
    console.log(`  GET /api/modules/:id/theorems - Verify theorems for module`);
    console.log(`  GET /api/theorems/:theorem - Get theorem explanation`);
    console.log(`  GET /health - Health check`);
    console.log(`=========================`);
});

module.exports = app;
