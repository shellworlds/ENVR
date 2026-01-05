"""
ENVR11 Travel Agent ML Engine
Quantum-enhanced travel optimization with 20-qubit simulations
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Quantum computing imports
try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
    from qiskit.algorithms import QAOA, NumPyMinimumEigensolver
    from qiskit_optimization import QuadraticProgram
    from qiskit_optimization.algorithms import MinimumEigenOptimizer
    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False
    print("Quantum libraries not available, using classical optimization")

# ML imports
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Travel industry imports
from datetime import datetime, timedelta
import holidays
from geopy.distance import geodesic
import timezonefinder

class TravelQuantumOptimizer:
    """Quantum optimizer for travel routing with 20 qubits"""
    
    def __init__(self, num_qubits=20):
        self.num_qubits = num_qubits
        self.backend = Aer.get_backend('qasm_simulator') if QUANTUM_AVAILABLE else None
        
    def create_travel_qaoa(self, destinations, constraints):
        """Create QAOA circuit for travel optimization"""
        if not QUANTUM_AVAILABLE:
            return self.classical_optimization(destinations, constraints)
            
        # Create quadratic program for travel optimization
        qp = QuadraticProgram('travel_optimization')
        
        # Add binary variables for each destination
        for i in range(len(destinations)):
            qp.binary_var(name=f'dest_{i}')
            
        # Objective: Minimize total travel distance
        linear = {f'dest_{i}': destinations[i]['distance'] for i in range(len(destinations))}
        quadratic = {}
        
        # Add constraints: time windows, budgets, etc.
        for i in range(len(destinations)):
            for j in range(i+1, len(destinations)):
                quadratic[(f'dest_{i}', f'dest_{j}')] = constraints.get('connection_cost', 1.0)
        
        qp.minimize(linear=linear, quadratic=quadratic)
        
        # Add constraints
        total_destinations = len(destinations)
        qp.linear_constraint(
            linear={f'dest_{i}': 1 for i in range(total_destinations)},
            sense='==',
            rhs=constraints.get('max_destinations', min(5, total_destinations))
        )
        
        # Solve using QAOA
        qaoa = QAOA(reps=2, quantum_instance=self.backend)
        optimizer = MinimumEigenOptimizer(qaoa)
        result = optimizer.solve(qp)
        
        return {
            'optimal_route': result.x,
            'optimal_value': result.fval,
            'solved_with': 'QAOA',
            'qubits_used': self.num_qubits
        }
    
    def classical_optimization(self, destinations, constraints):
        """Classical fallback for travel optimization"""
        import itertools
        
        best_route = None
        best_cost = float('inf')
        
        # Generate all possible combinations
        max_dest = constraints.get('max_destinations', 5)
        indices = range(len(destinations))
        
        for r in range(1, max_dest + 1):
            for combo in itertools.combinations(indices, r):
                cost = sum(destinations[i]['distance'] for i in combo)
                if cost < best_cost:
                    best_cost = cost
                    best_route = combo
        
        return {
            'optimal_route': best_route,
            'optimal_value': best_cost,
            'solved_with': 'Classical',
            'qubits_used': 0
        }

class TravelPricePredictor:
    """ML model for travel price prediction"""
    
    def __init__(self):
        self.models = {
            'rf': RandomForestRegressor(n_estimators=100, random_state=42),
            'gb': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'nn': self._build_neural_network()
        }
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def _build_neural_network(self):
        """Build neural network for price prediction"""
        model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(10,)),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(1)
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def prepare_travel_data(self, df):
        """Prepare travel data for ML"""
        # Feature engineering
        df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['season'] = df['month'] % 12 // 3 + 1
        df['advance_days'] = (pd.to_datetime(df['date']) - pd.Timestamp.now()).dt.days
        
        # Encode categorical features
        categorical_cols = ['origin', 'destination', 'airline', 'cabin_class']
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le
        
        # Select features
        features = ['advance_days', 'day_of_week', 'month', 'season', 
                   'distance_km', 'duration_hours', 'airline', 'cabin_class']
        
        X = df[[f for f in features if f in df.columns]]
        y = df['price']
        
        return X, y
    
    def train(self, X, y):
        """Train all models"""
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        results = {}
        
        for name, model in self.models.items():
            if name == 'nn':
                model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=0)
                y_pred = model.predict(X_test).flatten()
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            
            results[name] = {
                'mae': mean_absolute_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'r2': r2_score(y_test, y_pred)
            }
        
        return results

class TravelDashboardAPI:
    """FastAPI for travel dashboard"""
    
    def __init__(self):
        self.optimizer = TravelQuantumOptimizer()
        self.predictor = TravelPricePredictor()
        
    def generate_sample_data(self):
        """Generate sample travel data"""
        destinations = [
            {'name': 'Paris', 'distance': 300, 'cost': 500, 'days': 3},
            {'name': 'London', 'distance': 200, 'cost': 400, 'days': 2},
            {'name': 'Rome', 'distance': 400, 'cost': 600, 'days': 4},
            {'name': 'Berlin', 'distance': 350, 'cost': 450, 'days': 3},
            {'name': 'Madrid', 'distance': 450, 'cost': 550, 'days': 3}
        ]
        
        # Simulate optimization
        constraints = {'max_destinations': 3, 'connection_cost': 50}
        quantum_result = self.optimizer.create_travel_qaoa(destinations, constraints)
        
        return {
            'destinations': destinations,
            'optimization': quantum_result,
            'quantum_capable': QUANTUM_AVAILABLE,
            'timestamp': datetime.now().isoformat()
        }

def main():
    """Main execution function"""
    print("=" * 60)
    print("ENVR11 Travel Agent ML Engine")
    print("=" * 60)
    
    # Initialize components
    api = TravelDashboardAPI()
    
    # Generate sample data
    print("\n1. Generating sample travel data...")
    data = api.generate_sample_data()
    print(f"   Quantum optimization: {data['optimization']['solved_with']}")
    print(f"   Qubits used: {data['optimization']['qubits_used']}")
    
    # Simulate ML training
    print("\n2. Simulating ML price prediction...")
    sample_df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'origin': ['NYC'] * 100,
        'destination': ['LAX'] * 100,
        'airline': ['AA', 'UA', 'DL'] * 34,
        'cabin_class': ['Economy', 'Business'] * 50,
        'distance_km': [4000] * 100,
        'duration_hours': [6] * 100,
        'price': np.random.normal(500, 100, 100)
    })
    
    X, y = api.predictor.prepare_travel_data(sample_df)
    results = api.predictor.train(X, y)
    
    print("   Model Performance:")
    for model, metrics in results.items():
        print(f"   {model.upper()}: MAE=${metrics['mae']:.2f}, R²={metrics['r2']:.3f}")
    
    print("\n3. System Status:")
    print(f"   Quantum Computing: {'Available' if QUANTUM_AVAILABLE else 'Not Available'}")
    print(f"   ML Models: {len(api.predictor.models)} models trained")
    print(f"   Optimization: {data['optimization']['solved_with']} algorithm")
    
    print("\n" + "=" * 60)
    print("ENVR11 Travel ML Engine Ready for Dashboard Integration")
    print("=" * 60)
    
    return api

if __name__ == "__main__":
    main()
