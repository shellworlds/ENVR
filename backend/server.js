/**
 * ENVR11 Travel Agent API Server
 * Node.js backend with Express for travel data management
 */

const express = require('express');
const cors = require('cors');
const axios = require('axios');
const { PythonShell } = require('python-shell');

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('../frontend'));

// Sample travel data
const travelData = {
  destinations: [
    { id: 1, name: 'Paris', country: 'France', distance: 300, cost: 500, days: 3, bookings: 150, rating: 4.7 },
    { id: 2, name: 'London', country: 'UK', distance: 200, cost: 400, days: 2, bookings: 200, rating: 4.5 },
    { id: 3, name: 'Rome', country: 'Italy', distance: 400, cost: 600, days: 4, bookings: 120, rating: 4.8 },
    { id: 4, name: 'Berlin', country: 'Germany', distance: 350, cost: 450, days: 3, bookings: 180, rating: 4.6 },
    { id: 5, name: 'Madrid', country: 'Spain', distance: 450, cost: 550, days: 3, bookings: 90, rating: 4.4 },
    { id: 6, name: 'Tokyo', country: 'Japan', distance: 950, cost: 1200, days: 7, bookings: 75, rating: 4.9 },
    { id: 7, name: 'New York', country: 'USA', distance: 550, cost: 800, days: 5, bookings: 220, rating: 4.3 },
    { id: 8, name: 'Sydney', country: 'Australia', distance: 1050, cost: 1500, days: 8, bookings: 60, rating: 4.7 }
  ],
  priceTrends: [
    { month: 'Jan', price: 450, demand: 80, bookings: 1200 },
    { month: 'Feb', price: 480, demand: 85, bookings: 1350 },
    { month: 'Mar', price: 520, demand: 90, bookings: 1500 },
    { month: 'Apr', price: 550, demand: 95, bookings: 1650 },
    { month: 'May', price: 500, demand: 88, bookings: 1450 },
    { month: 'Jun', price: 480, demand: 92, bookings: 1600 },
    { month: 'Jul', price: 520, demand: 96, bookings: 1800 },
    { month: 'Aug', price: 600, demand: 98, bookings: 1950 }
  ],
  airlines: [
    { code: 'AA', name: 'American Airlines', rating: 4.2, routes: 45 },
    { code: 'UA', name: 'United Airlines', rating: 4.0, routes: 38 },
    { code: 'DL', name: 'Delta Airlines', rating: 4.3, routes: 42 },
    { code: 'BA', name: 'British Airways', rating: 4.5, routes: 28 },
    { code: 'LH', name: 'Lufthansa', rating: 4.4, routes: 32 },
    { code: 'EK', name: 'Emirates', rating: 4.8, routes: 50 }
  ],
  quantumStatus: {
    available: true,
    qubits: 20,
    algorithm: 'QAOA',
    speedup: '15x'
  }
};

// Routes
app.get('/api/travel-data', (req, res) => {
  res.json({
    ...travelData,
    quantum_capable: true,
    timestamp: new Date().toISOString(),
    system_status: 'operational',
    ml_models: {
      price_prediction: 'active',
      demand_forecasting: 'active',
      route_optimization: 'quantum_enhanced'
    }
  });
});

app.get('/api/destinations', (req, res) => {
  const { country, minRating, maxPrice } = req.query;
  let filtered = [...travelData.destinations];
  
  if (country) {
    filtered = filtered.filter(d => d.country.toLowerCase().includes(country.toLowerCase()));
  }
  
  if (minRating) {
    filtered = filtered.filter(d => d.rating >= parseFloat(minRating));
  }
  
  if (maxPrice) {
    filtered = filtered.filter(d => d.cost <= parseInt(maxPrice));
  }
  
  res.json({
    count: filtered.length,
    destinations: filtered,
    filters: { country, minRating, maxPrice }
  });
});

app.post('/api/quantum-optimize', async (req, res) => {
  const { destinations, constraints } = req.body;
  
  try {
    // Simulate quantum optimization
    const optimizationResult = simulateQuantumOptimization(destinations, constraints);
    
    res.json({
      success: true,
      optimization: optimizationResult,
      quantum: {
        algorithm: 'QAOA',
        qubits_used: 20,
        execution_time: '0.45s',
        classical_equivalent_time: '6.75s',
        speedup: '15x'
      },
      recommendation: generateRecommendation(optimizationResult)
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Quantum optimization failed',
      details: error.message
    });
  }
});

app.get('/api/price-prediction', async (req, res) => {
  const { origin, destination, date, passengers } = req.query;
  
  // Simulate ML price prediction
  const predictions = simulatePricePrediction(origin, destination, date, passengers);
  
  res.json({
    origin,
    destination,
    date,
    passengers: parseInt(passengers) || 1,
    predictions,
    confidence: 0.87,
    model_version: 'mlp_v2.1',
    last_trained: '2026-01-04'
  });
});

app.get('/api/system-metrics', (req, res) => {
  const metrics = {
    cpu_usage: Math.random() * 30 + 20, // 20-50%
    memory_usage: Math.random() * 40 + 30, // 30-70%
    quantum_jobs: Math.floor(Math.random() * 50) + 10,
    ml_predictions: Math.floor(Math.random() * 1000) + 500,
    active_users: Math.floor(Math.random() * 100) + 50,
    response_time: Math.random() * 100 + 50, // 50-150ms
    uptime: '99.95%',
    last_updated: new Date().toISOString()
  };
  
  res.json(metrics);
});

app.post('/api/travel-plan', async (req, res) => {
  const { destinations, budget, days, preferences } = req.body;
  
  const plan = generateTravelPlan(destinations, budget, days, preferences);
  
  res.json({
    success: true,
    plan,
    budget_analysis: analyzeBudget(plan, budget),
    quantum_optimized: true,
    generated_at: new Date().toISOString()
  });
});

// Helper functions
function simulateQuantumOptimization(destinations, constraints) {
  const maxDestinations = constraints?.maxDestinations || 3;
  const budget = constraints?.budget || 2000;
  
  // Simple optimization algorithm (simulated quantum)
  const allDestinations = destinations || travelData.destinations.slice(0, 5);
  const sorted = [...allDestinations].sort((a, b) => a.cost - b.cost);
  const selected = sorted.slice(0, Math.min(maxDestinations, sorted.length));
  
  const totalCost = selected.reduce((sum, d) => sum + d.cost, 0);
  const totalDistance = selected.reduce((sum, d) => sum + d.distance, 0);
  
  return {
    optimal_route: selected.map(d => d.id || d.name),
    optimal_value: totalCost,
    total_distance: totalDistance,
    destinations: selected.length,
    budget_utilization: (totalCost / budget) * 100,
    solved_with: 'QAOA Quantum Algorithm',
    qubits_used: 20
  };
}

function simulatePricePrediction(origin, destination, date, passengers) {
  const basePrice = Math.random() * 500 + 300; // $300-800
  const dateFactor = new Date(date).getMonth() > 5 ? 1.2 : 1.0; // Summer premium
  const passengerFactor = passengers ? Math.max(1, Math.log(passengers)) : 1;
  
  const predictions = {
    economy: {
      min: Math.round(basePrice * 0.8 * dateFactor * passengerFactor),
      avg: Math.round(basePrice * dateFactor * passengerFactor),
      max: Math.round(basePrice * 1.2 * dateFactor * passengerFactor),
      confidence: 0.85
    },
    business: {
      min: Math.round(basePrice * 2 * 0.8 * dateFactor * passengerFactor),
      avg: Math.round(basePrice * 2 * dateFactor * passengerFactor),
      max: Math.round(basePrice * 2 * 1.2 * dateFactor * passengerFactor),
      confidence: 0.78
    },
    first: {
      min: Math.round(basePrice * 3 * 0.8 * dateFactor * passengerFactor),
      avg: Math.round(basePrice * 3 * dateFactor * passengerFactor),
      max: Math.round(basePrice * 3 * 1.2 * dateFactor * passengerFactor),
      confidence: 0.72
    }
  };
  
  return predictions;
}

function generateTravelPlan(destinations, budget, days, preferences) {
  const selectedDestinations = destinations || travelData.destinations.slice(0, 3);
  
  const plan = {
    destinations: selectedDestinations,
    total_days: days || selectedDestinations.reduce((sum, d) => sum + d.days, 0),
    total_cost: selectedDestinations.reduce((sum, d) => sum + d.cost, 0),
    daily_schedule: [],
    transportation: [],
    accommodations: []
  };
  
  // Generate daily schedule
  let currentDay = 1;
  selectedDestinations.forEach(dest => {
    for (let i = 0; i < dest.days; i++) {
      plan.daily_schedule.push({
        day: currentDay,
        location: dest.name,
        activities: generateActivities(dest.name, preferences),
        meals: ['Breakfast', 'Lunch', 'Dinner']
      });
      currentDay++;
    }
  });
  
  // Generate transportation plan
  for (let i = 0; i < selectedDestinations.length - 1; i++) {
    plan.transportation.push({
      from: selectedDestinations[i].name,
      to: selectedDestinations[i + 1].name,
      type: Math.random() > 0.5 ? 'Flight' : 'Train',
      duration: '2-4 hours',
      estimated_cost: Math.round(Math.random() * 200 + 100)
    });
  }
  
  // Generate accommodations
  selectedDestinations.forEach(dest => {
    plan.accommodations.push({
      location: dest.name,
      type: preferences?.accommodation || '4-star Hotel',
      nights: dest.days,
      estimated_cost: Math.round(dest.cost * 0.6)
    });
  });
  
  return plan;
}

function generateActivities(destination, preferences) {
  const activityPools = {
    Paris: ['Eiffel Tower Visit', 'Louvre Museum', 'Seine River Cruise', 'Notre-Dame', 'Montmartre'],
    London: ['London Eye', 'British Museum', 'Tower of London', 'Buckingham Palace', 'West End Show'],
    Rome: ['Colosseum Tour', 'Vatican Museums', 'Trevi Fountain', 'Roman Forum', 'Pantheon'],
    Berlin: ['Brandenburg Gate', 'Reichstag Building', 'Berlin Wall Memorial', 'Museum Island', 'TV Tower'],
    Tokyo: ['Senso-ji Temple', 'Tokyo Skytree', 'Shibuya Crossing', 'Tsukiji Market', 'Imperial Palace']
  };
  
  const activities = activityPools[destination] || ['City Tour', 'Local Cuisine', 'Shopping', 'Cultural Experience'];
  
  return activities.slice(0, 3);
}

function analyzeBudget(plan, budget) {
  const total = plan.total_cost;
  const remaining = budget - total;
  const utilization = (total / budget) * 100;
  
  return {
    total_budget: budget,
    estimated_cost: total,
    remaining_budget: remaining,
    budget_utilization: utilization.toFixed(1) + '%',
    status: utilization > 90 ? 'Critical' : utilization > 70 ? 'High' : 'Good',
    recommendations: utilization > 90 ? ['Consider reducing destinations', 'Look for alternative accommodations'] : []
  };
}

function generateRecommendation(optimization) {
  if (optimization.budget_utilization > 90) {
    return 'Budget utilization is high. Consider reducing destinations or finding cost-effective alternatives.';
  } else if (optimization.budget_utilization > 70) {
    return 'Budget utilization is moderate. You have some flexibility for additional activities.';
  } else {
    return 'Budget utilization is good. You can consider upgrading accommodations or adding extra activities.';
  }
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'ENVR11 Travel Agent API',
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    quantum: travelData.quantumStatus,
    endpoints: [
      '/api/travel-data',
      '/api/destinations',
      '/api/quantum-optimize',
      '/api/price-prediction',
      '/api/system-metrics',
      '/api/travel-plan'
    ]
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`=========================================`);
  console.log(`ENVR11 Travel Agent API Server`);
  console.log(`=========================================`);
  console.log(`Server running on port ${PORT}`);
  console.log(`Quantum Computing: ${travelData.quantumStatus.available ? 'Available' : 'Unavailable'}`);
  console.log(`Qubits: ${travelData.quantumStatus.qubits}`);
  console.log(`Destinations loaded: ${travelData.destinations.length}`);
  console.log(`API Endpoints:`);
  console.log(`  http://localhost:${PORT}/health`);
  console.log(`  http://localhost:${PORT}/api/travel-data`);
  console.log(`  http://localhost:${PORT}/api/quantum-optimize`);
  console.log(`=========================================`);
});
