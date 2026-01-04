"""
ECG Arrhythmia Classification Tool
Machine Learning models for arrhythmia detection and classification
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Import ML libraries (optional imports for flexibility)
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not available. Using simplified models.")

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch not available. Using simplified models.")

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Scikit-learn not available. Using simplified models.")

class ECGArrhythmiaClassifier:
    """Advanced arrhythmia classification using multiple ML approaches"""
    
    def __init__(self, sampling_rate: int = 500):
        self.sampling_rate = sampling_rate
        self.arrhythmia_classes = {
            0: 'Normal Sinus Rhythm',
            1: 'Atrial Fibrillation',
            2: 'Atrial Flutter',
            3: 'Premature Ventricular Contraction',
            4: 'Premature Atrial Contraction',
            5: 'Ventricular Tachycardia',
            6: 'Supraventricular Tachycardia',
            7: 'Sinus Bradycardia',
            8: 'Sinus Tachycardia',
            9: 'Bundle Branch Block',
            10: 'Heart Block',
            11: 'Paced Rhythm'
        }
        
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        
    def train_classical_ml(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2):
        """Train classical ML models"""
        if not SKLEARN_AVAILABLE:
            print("Scikit-learn not available. Cannot train classical ML models.")
            return
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['classical'] = scaler
        
        # Train multiple models
        models_to_train = {
            'random_forest': RandomForestClassifier(
                n_estimators=100, 
                max_depth=10, 
                random_state=42,
                class_weight='balanced'
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100, 
                learning_rate=0.1, 
                max_depth=5, 
                random_state=42
            ),
            'svm': SVC(
                C=1.0, 
                kernel='rbf', 
                gamma='scale', 
                probability=True,
                class_weight='balanced',
                random_state=42
            ),
            'mlp': MLPClassifier(
                hidden_layer_sizes=(100, 50), 
                activation='relu',
                solver='adam',
                max_iter=1000,
                random_state=42
            )
        }
        
        results = {}
        for model_name, model in models_to_train.items():
            print(f"Training {model_name}...")
            model.fit(X_train_scaled, y_train)
            self.models[model_name] = model
            
            # Evaluate
            y_pred = model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            
            results[model_name] = {
                'accuracy': accuracy,
                'model': model,
                'predictions': y_pred,
                'true_labels': y_test
            }
            
            # Feature importance for tree-based models
            if hasattr(model, 'feature_importances_'):
                self.feature_importance[model_name] = model.feature_importances_
        
        self.classical_results = results
        return results
    
    def build_cnn_model(self, input_shape: Tuple, num_classes: int):
        """Build CNN model for raw ECG classification"""
        if not TF_AVAILABLE:
            print("TensorFlow not available. Cannot build CNN model.")
            return None
        
        model = models.Sequential([
            # First convolutional block
            layers.Conv1D(64, kernel_size=10, activation='relu', input_shape=input_shape),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.2),
            
            # Second convolutional block
            layers.Conv1D(128, kernel_size=8, activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.2),
            
            # Third convolutional block
            layers.Conv1D(256, kernel_size=6, activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.2),
            
            # Fourth convolutional block
            layers.Conv1D(512, kernel_size=4, activation='relu'),
            layers.BatchNormalization(),
            layers.GlobalAveragePooling1D(),
            layers.Dropout(0.3),
            
            # Dense layers
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            # Output layer
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy', 
                    keras.metrics.Precision(name='precision'),
                    keras.metrics.Recall(name='recall'),
                    keras.metrics.AUC(name='auc')]
        )
        
        return model
    
    def build_lstm_model(self, input_shape: Tuple, num_classes: int):
        """Build LSTM model for ECG sequence classification"""
        if not TF_AVAILABLE:
            print("TensorFlow not available. Cannot build LSTM model.")
            return None
        
        model = models.Sequential([
            # Bidirectional LSTM layers
            layers.Bidirectional(layers.LSTM(128, return_sequences=True), input_shape=input_shape),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Bidirectional(layers.LSTM(64, return_sequences=True)),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Bidirectional(layers.LSTM(32)),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            # Dense layers
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            # Output layer
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def build_hybrid_model(self, input_shape: Tuple, num_classes: int):
        """Build hybrid CNN-LSTM model"""
        if not TF_AVAILABLE:
            print("TensorFlow not available. Cannot build hybrid model.")
            return None
        
        inputs = keras.Input(shape=input_shape)
        
        # CNN branch
        x = layers.Conv1D(64, kernel_size=10, activation='relu')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling1D(pool_size=2)(x)
        x = layers.Dropout(0.2)(x)
        
        x = layers.Conv1D(128, kernel_size=8, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling1D(pool_size=2)(x)
        x = layers.Dropout(0.2)(x)
        
        # LSTM branch
        y = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(inputs)
        y = layers.BatchNormalization()(y)
        y = layers.Dropout(0.3)(y)
        
        y = layers.Bidirectional(layers.LSTM(32))(y)
        y = layers.BatchNormalization()(y)
        y = layers.Dropout(0.3)(y)
        
        # Merge branches
        combined = layers.Concatenate()([layers.GlobalAveragePooling1D()(x), y])
        
        # Dense layers
        z = layers.Dense(128, activation='relu')(combined)
        z = layers.BatchNormalization()(z)
        z = layers.Dropout(0.3)(z)
        
        z = layers.Dense(64, activation='relu')(z)
        z = layers.BatchNormalization()(z)
        z = layers.Dropout(0.3)(z)
        
        # Output
        outputs = layers.Dense(num_classes, activation='softmax')(z)
        
        model = keras.Model(inputs=inputs, outputs=outputs)
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_deep_learning(self, X_train: np.ndarray, y_train: np.ndarray, 
                           X_val: np.ndarray, y_val: np.ndarray,
                           input_shape: Tuple, num_classes: int):
        """Train deep learning models"""
        if not TF_AVAILABLE:
            print("TensorFlow not available. Cannot train deep learning models.")
            return {}
        
        results = {}
        
        # Models to train
        models_config = {
            'cnn': self.build_cnn_model(input_shape, num_classes),
            'lstm': self.build_lstm_model(input_shape, num_classes),
            'hybrid': self.build_hybrid_model(input_shape, num_classes)
        }
        
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6
            )
        ]
        
        for model_name, model in models_config.items():
            if model is None:
                continue
                
            print(f"Training {model_name}...")
            
            history = model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                epochs=50,
                batch_size=32,
                callbacks=callbacks,
                verbose=1
            )
            
            # Evaluate
            val_loss, val_accuracy = model.evaluate(X_val, y_val, verbose=0)
            
            results[model_name] = {
                'model': model,
                'history': history.history,
                'val_accuracy': val_accuracy,
                'val_loss': val_loss
            }
            
            self.models[model_name] = model
        
        self.dl_results = results
        return results
    
    def predict(self, ecg_signal: np.ndarray, model_type: str = 'ensemble') -> Dict:
        """Predict arrhythmia class"""
        predictions = {}
        
        if model_type == 'ensemble' and self.models:
            # Ensemble prediction
            for model_name, model in self.models.items():
                if model_name in ['cnn', 'lstm', 'hybrid'] and TF_AVAILABLE:
                    # Reshape for DL models
                    if len(ecg_signal.shape) == 1:
                        ecg_reshaped = ecg_signal.reshape(1, -1, 1)
                    else:
                        ecg_reshaped = ecg_signal
                    
                    pred = model.predict(ecg_reshaped, verbose=0)
                    predictions[model_name] = {
                        'probabilities': pred[0],
                        'predicted_class': int(np.argmax(pred[0])),
                        'class_name': self.arrhythmia_classes.get(int(np.argmax(pred[0])), 'Unknown')
                    }
                    
                elif SKLEARN_AVAILABLE and hasattr(model, 'predict_proba'):
                    # Classical ML models
                    if model_name in self.scalers:
                        scaled_input = self.scalers['classical'].transform(ecg_signal.reshape(1, -1))
                    else:
                        scaled_input = ecg_signal.reshape(1, -1)
                    
                    pred_proba = model.predict_proba(scaled_input)
                    predictions[model_name] = {
                        'probabilities': pred_proba[0],
                        'predicted_class': int(model.predict(scaled_input)[0]),
                        'class_name': self.arrhythmia_classes.get(int(model.predict(scaled_input)[0]), 'Unknown')
                    }
        else:
            # Use specific model
            if model_type in self.models:
                model = self.models[model_type]
                
                if TF_AVAILABLE and model_type in ['cnn', 'lstm', 'hybrid']:
                    if len(ecg_signal.shape) == 1:
                        ecg_reshaped = ecg_signal.reshape(1, -1, 1)
                    else:
                        ecg_reshaped = ecg_signal
                    
                    pred = model.predict(ecg_reshaped, verbose=0)
                    predictions = {
                        'probabilities': pred[0],
                        'predicted_class': int(np.argmax(pred[0])),
                        'class_name': self.arrhythmia_classes.get(int(np.argmax(pred[0])), 'Unknown'),
                        'confidence': float(np.max(pred[0]))
                    }
                elif SKLEARN_AVAILABLE and hasattr(model, 'predict_proba'):
                    if model_type in self.scalers:
                        scaled_input = self.scalers['classical'].transform(ecg_signal.reshape(1, -1))
                    else:
                        scaled_input = ecg_signal.reshape(1, -1)
                    
                    pred_proba = model.predict_proba(scaled_input)
                    predictions = {
                        'probabilities': pred_proba[0],
                        'predicted_class': int(model.predict(scaled_input)[0]),
                        'class_name': self.arrhythmia_classes.get(int(model.predict(scaled_input)[0]), 'Unknown'),
                        'confidence': float(np.max(pred_proba[0]))
                    }
        
        return predictions
    
    def explain_prediction(self, ecg_signal: np.ndarray, model_type: str = 'random_forest') -> Dict:
        """Explain model prediction using feature importance or attention"""
        explanation = {}
        
        if model_type in self.feature_importance:
            # Feature importance explanation
            importance = self.feature_importance[model_type]
            top_features_idx = np.argsort(importance)[-10:][::-1]  # Top 10 features
            
            explanation['method'] = 'feature_importance'
            explanation['top_features'] = [
                {'feature_index': int(idx), 'importance': float(importance[idx])}
                for idx in top_features_idx
            ]
            
            # Map to feature names if available
            if hasattr(self, 'feature_names'):
                for feat in explanation['top_features']:
                    if feat['feature_index'] < len(self.feature_names):
                        feat['feature_name'] = self.feature_names[feat['feature_index']]
        
        elif model_type in ['cnn', 'lstm', 'hybrid'] and TF_AVAILABLE:
            # Gradient-based explanation (simplified)
            explanation['method'] = 'gradient_importance'
            explanation['message'] = 'Deep learning model - use Grad-CAM or attention visualization for detailed explanation'
            
            # Simplified gradient calculation
            model = self.models[model_type]
            ecg_tensor = tf.convert_to_tensor(ecg_signal.reshape(1, -1, 1), dtype=tf.float32)
            
            with tf.GradientTape() as tape:
                tape.watch(ecg_tensor)
                predictions = model(ecg_tensor)
                top_class = tf.argmax(predictions[0])
                top_score = predictions[0][top_class]
            
            gradients = tape.gradient(top_score, ecg_tensor)
            importance = tf.reduce_mean(tf.abs(gradients), axis=-1).numpy().flatten()
            
            top_indices = np.argsort(importance)[-20:][::-1]
            explanation['important_segments'] = [
                {'sample_index': int(idx), 'importance': float(importance[idx])}
                for idx in top_indices
            ]
        
        return explanation
    
    def clinical_risk_assessment(self, predictions: Dict) -> Dict:
        """Perform clinical risk assessment based on predictions"""
        risk_assessment = {
            'risk_level': 'LOW',
            'confidence': 0.0,
            'recommendations': [],
            'urgent_action_required': False
        }
        
        if 'predicted_class' in predictions:
            predicted_class = predictions['predicted_class']
            confidence = predictions.get('confidence', 0.0)
            
            # High-risk arrhythmias
            high_risk_classes = [1, 2, 5, 6, 10]  # AFib, AFL, VT, SVT, Heart Block
            moderate_risk_classes = [3, 4, 9]     # PVC, PAC, BBB
            low_risk_classes = [0, 7, 8, 11]      # Normal, Brady, Tachy, Paced
            
            if predicted_class in high_risk_classes:
                risk_assessment['risk_level'] = 'HIGH'
                risk_assessment['urgent_action_required'] = True
                risk_assessment['recommendations'].append('Immediate cardiology consultation')
                risk_assessment['recommendations'].append('Consider hospital admission')
                risk_assessment['recommendations'].append('Continuous ECG monitoring required')
                
            elif predicted_class in moderate_risk_classes:
                risk_assessment['risk_level'] = 'MODERATE'
                risk_assessment['recommendations'].append('Schedule cardiology follow-up')
                risk_assessment['recommendations'].append('Consider Holter monitoring')
                risk_assessment['recommendations'].append('Lifestyle modifications recommended')
                
            else:
                risk_assessment['risk_level'] = 'LOW'
                risk_assessment['recommendations'].append('Routine follow-up')
                risk_assessment['recommendations'].append('Maintain healthy lifestyle')
            
            risk_assessment['confidence'] = confidence
            
            # Adjust based on confidence
            if confidence < 0.7:
                risk_assessment['recommendations'].append('Low confidence prediction - consider manual review')
            elif confidence > 0.9:
                risk_assessment['recommendations'].append('High confidence prediction - automated action possible')
        
        return risk_assessment
    
    def generate_classification_report(self, predictions: Dict, risk_assessment: Dict) -> str:
        """Generate comprehensive classification report"""
        report = []
        report.append("=" * 80)
        report.append("ARRHYTHMIA CLASSIFICATION REPORT")
        report.append("=" * 80)
        
        if 'predicted_class' in predictions:
            predicted_class = predictions['predicted_class']
            class_name = predictions.get('class_name', 'Unknown')
            confidence = predictions.get('confidence', 0.0)
            
            report.append(f"Predicted Arrhythmia: {class_name}")
            report.append(f"Prediction Confidence: {confidence:.1%}")
            report.append(f"Risk Level: {risk_assessment['risk_level']}")
            report.append("")
            
            report.append("Clinical Risk Assessment:")
            report.append("-" * 40)
            for i, rec in enumerate(risk_assessment['recommendations'], 1):
                report.append(f"{i}. {rec}")
            
            if risk_assessment['urgent_action_required']:
                report.append("")
                report.append("⚠️  URGENT ACTION REQUIRED ⚠️")
                report.append("This arrhythmia requires immediate medical attention.")
            
            report.append("")
            report.append("Probability Distribution:")
            report.append("-" * 40)
            
            if 'probabilities' in predictions:
                probs = predictions['probabilities']
                for class_idx, prob in enumerate(probs):
                    if prob > 0.01:  # Only show probabilities > 1%
                        class_name = self.arrhythmia_classes.get(class_idx, f'Class {class_idx}')
                        report.append(f"{class_name}: {prob:.1%}")
        
        elif 'ensemble' in predictions:
            report.append("Ensemble Model Predictions:")
            report.append("-" * 40)
            
            for model_name, model_pred in predictions['ensemble'].items():
                report.append(f"{model_name.upper()}: {model_pred['class_name']} "
                            f"(Confidence: {np.max(model_pred['probabilities']):.1%})")
        
        report.append("")
        report.append("Note: This is an automated analysis. All predictions should be")
        report.append("reviewed by a qualified cardiologist before clinical action.")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_model(self, model_name: str, filepath: str):
        """Save trained model to disk"""
        if model_name in self.models:
            model = self.models[model_name]
            
            if TF_AVAILABLE and isinstance(model, keras.Model):
                model.save(filepath)
                print(f"Saved TensorFlow model to {filepath}")
            elif SKLEARN_AVAILABLE:
                import joblib
                joblib.dump(model, filepath)
                print(f"Saved scikit-learn model to {filepath}")
            else:
                print(f"Cannot save model {model_name}: unsupported type")
        else:
            print(f"Model {model_name} not found")
    
    def load_model(self, model_name: str, filepath: str):
        """Load trained model from disk"""
        try:
            if filepath.endswith('.h5') or filepath.endswith('.keras'):
                if TF_AVAILABLE:
                    model = keras.models.load_model(filepath)
                    self.models[model_name] = model
                    print(f"Loaded TensorFlow model from {filepath}")
                else:
                    print("TensorFlow not available. Cannot load .h5/.keras model.")
            else:
                import joblib
                model = joblib.load(filepath)
                self.models[model_name] = model
                print(f"Loaded scikit-learn model from {filepath}")
        except Exception as e:
            print(f"Error loading model: {e}")

def generate_synthetic_data(num_samples: int = 1000, num_features: int = 100) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic ECG feature data for demonstration"""
    np.random.seed(42)
    
    # Generate random features
    X = np.random.randn(num_samples, num_features)
    
    # Create some feature patterns for different classes
    for i in range(num_samples):
        # Add class-specific patterns
        if i < num_samples // 4:
            # Class 0: Normal rhythm features
            X[i, :10] += 1.0  # Strong first 10 features
        elif i < num_samples // 2:
            # Class 1: AFib features
            X[i, 10:20] += 1.5  # Different set of features
            X[i, :5] -= 0.5    # Weaken some features
        elif i < 3 * num_samples // 4:
            # Class 2: PVC features
            X[i, 20:30] += 2.0  # Another set of features
        else:
            # Class 3: Other arrhythmias
            X[i, 30:40] += 1.0
            X[i, 40:50] -= 1.0
    
    # Generate labels (4 classes for simplicity)
    y = np.zeros(num_samples, dtype=int)
    y[num_samples//4:num_samples//2] = 1
    y[num_samples//2:3*num_samples//4] = 2
    y[3*num_samples//4:] = 3
    
    return X, y

def generate_synthetic_ecg_signals(num_signals: int = 100, signal_length: int = 5000) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic raw ECG signals for deep learning"""
    np.random.seed(42)
    
    signals = []
    labels = []
    
    for i in range(num_signals):
        t = np.linspace(0, 10, signal_length)
        
        # Base ECG components
        base_signal = np.sin(2 * np.pi * 1 * t)  # Heart rate ~60 bpm
        
        # Add class-specific patterns
        if i < num_signals // 4:
            # Normal rhythm
            signal = base_signal + 0.5 * np.sin(2 * np.pi * 5 * t)  # QRS complexes
            label = 0
        elif i < num_signals // 2:
            # AFib - irregular rhythm
            signal = base_signal * (1 + 0.3 * np.sin(2 * np.pi * 0.5 * t))  # Amplitude modulation
            signal += 0.3 * np.random.randn(signal_length)  # More noise
            label = 1
        elif i < 3 * num_signals // 4:
            # PVC - occasional large spikes
            signal = base_signal.copy()
            pvc_indices = np.random.choice(signal_length, 10, replace=False)
            signal[pvc_indices] += 2.0  # PVC spikes
            label = 2
        else:
            # Sinus tachycardia - faster rhythm
            signal = np.sin(2 * np.pi * 1.5 * t) + 0.5 * np.sin(2 * np.pi * 7.5 * t)
            label = 3
        
        # Add baseline noise
        signal += 0.1 * np.random.randn(signal_length)
        
        signals.append(signal)
        labels.append(label)
    
    signals = np.array(signals)
    labels = np.array(labels)
    
    # Reshape for CNN/LSTM (samples, timesteps, channels)
    signals = signals.reshape(-1, signal_length, 1)
    
    return signals, labels

def main():
    """Example usage of ECG Arrhythmia Classifier"""
    print("Initializing ECG Arrhythmia Classifier...")
    classifier = ECGArrhythmiaClassifier()
    
    print("\n1. Training Classical ML Models...")
    print("-" * 40)
    
    # Generate synthetic feature data
    X_features, y_features = generate_synthetic_data(num_samples=1000, num_features=50)
    print(f"Feature data shape: {X_features.shape}")
    print(f"Labels shape: {y_features.shape}")
    print(f"Class distribution: {np.bincount(y_features)}")
    
    # Train classical ML models
    if SKLEARN_AVAILABLE:
        results = classifier.train_classical_ml(X_features, y_features, test_size=0.2)
        
        # Print results
        for model_name, result in results.items():
            print(f"{model_name}: Accuracy = {result['accuracy']:.3f}")
    
    print("\n2. Training Deep Learning Models...")
    print("-" * 40)
    
    # Generate synthetic raw ECG data
    X_signals, y_signals = generate_synthetic_ecg_signals(num_signals=200, signal_length=5000)
    print(f"ECG signals shape: {X_signals.shape}")
    print(f"Signal labels shape: {y_signals.shape}")
    print(f"Class distribution: {np.bincount(y_signals)}")
    
    # Split for DL training
    if TF_AVAILABLE and len(X_signals) > 0:
        X_train, X_temp, y_train, y_temp = train_test_split(
            X_signals, y_signals, test_size=0.3, random_state=42, stratify=y_signals
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
        )
        
        print(f"Training set: {X_train.shape}")
        print(f"Validation set: {X_val.shape}")
        
        # Train DL models
        input_shape = (X_train.shape[1], X_train.shape[2])
        num_classes = len(np.unique(y_signals))
        
        dl_results = classifier.train_deep_learning(
            X_train, y_train, X_val, y_val,
            input_shape, num_classes
        )
        
        # Print DL results
        for model_name, result in dl_results.items():
            print(f"{model_name}: Val Accuracy = {result['val_accuracy']:.3f}")
    
    print("\n3. Making Predictions...")
    print("-" * 40)
    
    # Generate a test signal
    test_signal = generate_synthetic_ecg_signals(num_signals=1, signal_length=5000)[0][0]
    
    # Predict using ensemble
    predictions = classifier.predict(test_signal, model_type='ensemble')
    
    # Clinical risk assessment
    if 'predicted_class' in predictions:
        risk_assessment = classifier.clinical_risk_assessment(predictions)
        
        # Generate report
        report = classifier.generate_classification_report(predictions, risk_assessment)
        print(report)
        
        # Explain prediction
        if 'random_forest' in classifier.models:
            explanation = classifier.explain_prediction(test_signal.flatten(), model_type='random_forest')
            print("\nPrediction Explanation:")
            print(f"Method: {explanation['method']}")
            if 'top_features' in explanation:
                print("Top important features:")
                for feat in explanation['top_features'][:5]:
                    print(f"  Feature {feat['feature_index']}: Importance = {feat['importance']:.4f}")
    
    print("\n4. Saving Models...")
    print("-" * 40)
    
    # Save a model (example)
    if 'random_forest' in classifier.models:
        classifier.save_model('random_forest', 'random_forest_model.pkl')
    
    if TF_AVAILABLE and 'cnn' in classifier.models:
        classifier.save_model('cnn', 'cnn_model.h5')
    
    print("\n" + "=" * 80)
    print("ARRHYTHMIA CLASSIFICATION DEMONSTRATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
