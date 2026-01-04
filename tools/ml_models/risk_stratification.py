"""
ECG Risk Stratification System
Advanced risk assessment for cardiovascular events
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.svm import SVR
    from sklearn.neural_network import MLPRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Scikit-learn not available. Using simplified models.")

class ECGRiskStratification:
    """Comprehensive ECG-based risk stratification system"""
    
    def __init__(self):
        self.risk_categories = {
            'VERY_LOW': {'score_range': (0, 10), 'color': '#27ae60', 'description': 'Minimal risk'},
            'LOW': {'score_range': (11, 30), 'color': '#2ecc71', 'description': 'Low risk'},
            'MODERATE': {'score_range': (31, 50), 'color': '#f39c12', 'description': 'Moderate risk'},
            'HIGH': {'score_range': (51, 70), 'color': '#e67e22', 'description': 'High risk'},
            'VERY_HIGH': {'score_range': (71, 100), 'color': '#e74c3c', 'description': 'Very high risk'}
        }
        
        self.clinical_guidelines = {
            'aha_acc_2023': self._aha_acc_2023_guidelines,
            'esc_2022': self._esc_2022_guidelines,
            'fda_class_ii': self._fda_class_ii_requirements
        }
        
        self.models = {}
        self.scalers = {}
        
    def calculate_basic_risk_score(self, ecg_features: Dict) -> float:
        """Calculate basic risk score from ECG features"""
        score = 50.0  # Baseline score
        
        # Adjust based on key ECG parameters
        if 'heart_rate' in ecg_features:
            hr = ecg_features['heart_rate']
            if hr < 50 or hr > 120:
                score += 15
            elif hr < 60 or hr > 100:
                score += 8
        
        if 'qt_interval' in ecg_features:
            qt = ecg_features['qt_interval']
            if qt > 500:
                score += 25
            elif qt > 450:
                score += 15
            elif qt > 440:
                score += 5
        
        if 'hrv' in ecg_features:
            hrv = ecg_features['hrv']
            if hrv < 20:
                score += 10
            elif hrv < 30:
                score += 5
        
        if 'qrs_duration' in ecg_features:
            qrs = ecg_features['qrs_duration']
            if qrs > 120:
                score += 10
        
        if 'st_depression' in ecg_features:
            st_dep = ecg_features['st_depression']
            if st_dep > 0.5:
                score += st_dep * 10
        
        if 'arrhythmia_present' in ecg_features and ecg_features['arrhythmia_present']:
            score += 20
        
        # Apply sigmoid normalization to keep score between 0-100
        score = 100 / (1 + np.exp(-0.1 * (score - 50)))
        
        return min(max(score, 0), 100)
    
    def calculate_advanced_risk_score(self, patient_data: Dict, ecg_features: Dict) -> Dict:
        """Calculate advanced risk score with multiple components"""
        risk_components = {}
        
        # 1. Arrhythmia Risk
        risk_components['arrhythmia_risk'] = self._calculate_arrhythmia_risk(ecg_features)
        
        # 2. Ischemia Risk
        risk_components['ischemia_risk'] = self._calculate_ischemia_risk(ecg_features)
        
        # 3. Heart Failure Risk
        risk_components['heart_failure_risk'] = self._calculate_heart_failure_risk(patient_data, ecg_features)
        
        # 4. Sudden Cardiac Death Risk
        risk_components['scd_risk'] = self._calculate_scd_risk(patient_data, ecg_features)
        
        # 5. Overall Composite Risk
        composite_risk = (
            risk_components['arrhythmia_risk'] * 0.3 +
            risk_components['ischemia_risk'] * 0.25 +
            risk_components['heart_failure_risk'] * 0.25 +
            risk_components['scd_risk'] * 0.2
        )
        
        risk_components['composite_risk'] = composite_risk
        
        # Add risk category
        risk_components['risk_category'] = self._categorize_risk(composite_risk)
        risk_components['risk_score'] = composite_risk * 100
        
        # Calculate time-to-event probabilities
        risk_components['event_probabilities'] = self._calculate_event_probabilities(
            risk_components, patient_data
        )
        
        return risk_components
    
    def _calculate_arrhythmia_risk(self, ecg_features: Dict) -> float:
        """Calculate arrhythmia risk"""
        risk = 0.0
        
        # Heart rate variability
        if 'hrv' in ecg_features:
            hrv = ecg_features['hrv']
            if hrv < 20:
                risk += 0.4
            elif hrv < 30:
                risk += 0.2
        
        # QTc interval
        if 'qt_interval' in ecg_features:
            qt = ecg_features['qt_interval']
            if qt > 500:
                risk += 0.6
            elif qt > 450:
                risk += 0.3
        
        # Premature beats
        if 'premature_beats' in ecg_features:
            pvc_count = ecg_features['premature_beats'].get('pvc_count', 0)
            pac_count = ecg_features['premature_beats'].get('pac_count', 0)
            
            if pvc_count > 10:  # >10 PVCs per hour
                risk += min(0.3, pvc_count / 100)
            if pac_count > 20:  # >20 PACs per hour
                risk += min(0.2, pac_count / 200)
        
        # Existing arrhythmia
        if 'arrhythmia_type' in ecg_features:
            arrhythmia = ecg_features['arrhythmia_type']
            if arrhythmia in ['Atrial Fibrillation', 'Ventricular Tachycardia']:
                risk += 0.5
            elif arrhythmia in ['Atrial Flutter', 'SVT']:
                risk += 0.3
        
        return min(risk, 1.0)
    
    def _calculate_ischemia_risk(self, ecg_features: Dict) -> float:
        """Calculate ischemia risk"""
        risk = 0.0
        
        # ST segment depression/elevation
        if 'st_depression' in ecg_features:
            st_dep = ecg_features['st_depression']
            if st_dep > 2.0:  # >2mm depression
                risk += 0.6
            elif st_dep > 1.0:  # >1mm depression
                risk += 0.3
            elif st_dep > 0.5:  # >0.5mm depression
                risk += 0.1
        
        if 'st_elevation' in ecg_features:
            st_elev = ecg_features['st_elevation']
            if st_elev > 1.0:  # >1mm elevation
                risk += 0.4
        
        # T-wave abnormalities
        if 't_wave_inversion' in ecg_features and ecg_features['t_wave_inversion']:
            risk += 0.2
        
        # Q-waves (indicate previous MI)
        if 'pathological_q_waves' in ecg_features and ecg_features['pathological_q_waves']:
            risk += 0.3
        
        return min(risk, 1.0)
    
    def _calculate_heart_failure_risk(self, patient_data: Dict, ecg_features: Dict) -> float:
        """Calculate heart failure risk"""
        risk = 0.0
        
        # Patient factors
        if 'age' in patient_data:
            age = patient_data['age']
            if age > 70:
                risk += 0.2
            elif age > 60:
                risk += 0.1
        
        if 'hypertension' in patient_data and patient_data['hypertension']:
            risk += 0.15
        
        if 'diabetes' in patient_data and patient_data['diabetes']:
            risk += 0.15
        
        if 'previous_mi' in patient_data and patient_data['previous_mi']:
            risk += 0.25
        
        # ECG factors
        if 'qrs_duration' in ecg_features:
            qrs = ecg_features['qrs_duration']
            if qrs > 150:  >150ms indicates possible LBBB
                risk += 0.3
            elif qrs > 120:
                risk += 0.15
        
        if 'left_ventricular_hypertrophy' in ecg_features and ecg_features['left_ventricular_hypertrophy']:
            risk += 0.2
        
        if 'atrial_fibrillation' in ecg_features and ecg_features['atrial_fibrillation']:
            risk += 0.15
        
        return min(risk, 1.0)
    
    def _calculate_scd_risk(self, patient_data: Dict, ecg_features: Dict) -> float:
        """Calculate sudden cardiac death risk"""
        risk = 0.0
        
        # High-risk factors
        if 'ejection_fraction' in patient_data:
            ef = patient_data['ejection_fraction']
            if ef < 30:
                risk += 0.5
            elif ef < 40:
                risk += 0.3
        
        if 'previous_scd' in patient_data and patient_data['previous_scd']:
            risk += 0.4
        
        if 'family_history_scd' in patient_data and patient_data['family_history_scd']:
            risk += 0.2
        
        # ECG risk markers
        if 'qt_interval' in ecg_features:
            qt = ecg_features['qt_interval']
            if qt > 500:
                risk += 0.6
            elif qt > 450:
                risk += 0.3
        
        if 'brugada_pattern' in ecg_features and ecg_features['brugada_pattern']:
            risk += 0.5
        
        if 'epsilon_waves' in ecg_features and ecg_features['epsilon_waves']:  # ARVC marker
            risk += 0.4
        
        if 'late_potentials' in ecg_features and ecg_features['late_potentials']:
            risk += 0.3
        
        # Reduced HRV
        if 'hrv' in ecg_features and ecg_features['hrv'] < 20:
            risk += 0.2
        
        return min(risk, 1.0)
    
    def _calculate_event_probabilities(self, risk_components: Dict, patient_data: Dict) -> Dict:
        """Calculate probabilities of specific cardiac events"""
        probabilities = {}
        
        # Base rates from population studies
        base_rates = {
            'arrhythmic_event': 0.02,  # 2% annual risk in general population
            'myocardial_infarction': 0.01,  # 1% annual risk
            'heart_failure': 0.015,  # 1.5% annual risk
            'sudden_cardiac_death': 0.001,  # 0.1% annual risk
            'stroke': 0.008  # 0.8% annual risk
        }
        
        # Adjust based on risk components
        risk_multipliers = {
            'arrhythmic_event': 1 + risk_components['arrhythmia_risk'] * 10,
            'myocardial_infarction': 1 + risk_components['ischemia_risk'] * 8,
            'heart_failure': 1 + risk_components['heart_failure_risk'] * 12,
            'sudden_cardiac_death': 1 + risk_components['scd_risk'] * 15,
            'stroke': 1 + risk_components['arrhythmia_risk'] * 5  # AFib increases stroke risk
        }
        
        # Calculate probabilities for different time horizons
        time_horizons = [30, 90, 365, 1825]  # days: 1 month, 3 months, 1 year, 5 years
        
        for event, base_rate in base_rates.items():
            probabilities[event] = {}
            multiplier = risk_multipliers.get(event, 1.0)
            
            for horizon in time_horizons:
                # Convert annual rate to horizon-specific rate
                horizon_years = horizon / 365
                adjusted_rate = 1 - (1 - base_rate * multiplier) ** horizon_years
                probabilities[event][f'{horizon}_days'] = min(adjusted_rate, 0.99)
        
        return probabilities
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk score into clinical categories"""
        for category, info in self.risk_categories.items():
            low, high = info['score_range']
            if low <= risk_score * 100 <= high:
                return category
        return 'MODERATE'  # Default
    
    def _aha_acc_2023_guidelines(self, risk_components: Dict) -> List[str]:
        """Apply AHA/ACC 2023 guidelines"""
        recommendations = []
        
        if risk_components['arrhythmia_risk'] > 0.7:
            recommendations.append("Consider implantable cardioverter-defibrillator (ICD) evaluation")
        
        if risk_components['ischemia_risk'] > 0.6:
            recommendations.append("Recommend coronary angiography for ischemia evaluation")
            recommendations.append("Consider stress testing if not contraindicated")
        
        if risk_components['heart_failure_risk'] > 0.5:
            recommendations.append("Optimize guideline-directed medical therapy (GDMT)")
            recommendations.append("Consider cardiac resynchronization therapy (CRT) if QRS > 150ms")
        
        if risk_components['scd_risk'] > 0.4:
            recommendations.append("Primary prevention ICD may be indicated")
            recommendations.append("Consider electrophysiology study")
        
        if risk_components['composite_risk'] > 0.6:
            recommendations.append("High risk - refer to heart team for multidisciplinary evaluation")
        
        return recommendations
    
    def _esc_2022_guidelines(self, risk_components: Dict) -> List[str]:
        """Apply ESC 2022 guidelines"""
        recommendations = []
        
        if risk_components['arrhythmia_risk'] > 0.6:
            recommendations.append("Consider 24-hour Holter monitoring")
            recommendations.append("Evaluate for catheter ablation if symptomatic")
        
        if risk_components['ischemia_risk'] > 0.5:
            recommendations.append("Perform non-invasive ischemia testing")
            recommendations.append("Consider coronary CT angiography")
        
        if risk_components['composite_risk'] > 0.5:
            recommendations.append("Intensify risk factor modification")
            recommendations.append("Consider cardiology referral")
        
        return recommendations
    
    def _fda_class_ii_requirements(self, risk_components: Dict) -> List[str]:
        """Apply FDA Class II medical device requirements"""
        requirements = []
        
        if risk_components['composite_risk'] > 0.4:
            requirements.append("Clinical validation required for high-risk prediction")
            requirements.append("Post-market surveillance recommended")
        
        if risk_components['scd_risk'] > 0.3:
            requirements.append("Risk mitigation strategies required")
            requirements.append("User training and clinical support needed")
        
        return requirements
    
    def generate_risk_report(self, patient_data: Dict, ecg_features: Dict, 
                           risk_components: Dict) -> str:
        """Generate comprehensive risk stratification report"""
        report = []
        report.append("=" * 80)
        report.append("CARDIAC RISK STRATIFICATION REPORT")
        report.append("=" * 80)
        report.append(f"Patient ID: {patient_data.get('patient_id', 'Unknown')}")
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Risk Score Summary
        report.append("RISK ASSESSMENT SUMMARY")
        report.append("-" * 40)
        report.append(f"Overall Risk Score: {risk_components.get('risk_score', 0):.1f}/100")
        report.append(f"Risk Category: {risk_components.get('risk_category', 'UNKNOWN')}")
        report.append(f"Category Description: {self.risk_categories.get(risk_components.get('risk_category', 'MODERATE'), {}).get('description', '')}")
        report.append("")
        
        # Component Scores
        report.append("RISK COMPONENT ANALYSIS")
        report.append("-" * 40)
        components = ['arrhythmia_risk', 'ischemia_risk', 'heart_failure_risk', 'scd_risk']
        for comp in components:
            if comp in risk_components:
                score = risk_components[comp] * 100
                report.append(f"{comp.replace('_', ' ').title()}: {score:.1f}/100")
        report.append("")
        
        # Event Probabilities
        report.append("EVENT PROBABILITIES")
        report.append("-" * 40)
        if 'event_probabilities' in risk_components:
            probs = risk_components['event_probabilities']
            for event, horizons in probs.items():
                report.append(f"\n{event.replace('_', ' ').title()}:")
                for horizon, prob in horizons.items():
                    days = horizon.replace('_days', '')
                    if int(days) == 365:
                        report.append(f"  1-year risk: {prob:.1%}")
                    elif int(days) == 1825:
                        report.append(f"  5-year risk: {prob:.1%}")
        report.append("")
        
        # Clinical Guidelines
        report.append("CLINICAL GUIDELINE RECOMMENDATIONS")
        report.append("-" * 40)
        
        all_recommendations = []
        for guideline_name, guideline_func in self.clinical_guidelines.items():
            recs = guideline_func(risk_components)
            if recs:
                report.append(f"\n{guideline_name.upper()} Recommendations:")
                for rec in recs:
                    report.append(f"  • {rec}")
                    all_recommendations.append(rec)
        
        # Priority Recommendations
        report.append("\nPRIORITY ACTIONS")
        report.append("-" * 40)
        
        if risk_components.get('risk_category') in ['HIGH', 'VERY_HIGH']:
            report.append("1. IMMEDIATE CARDIOLOGY REFERRAL REQUIRED")
            report.append("2. Consider hospitalization for monitoring")
            report.append("3. Initiate appropriate medical therapy")
        elif risk_components.get('risk_category') == 'MODERATE':
            report.append("1. Schedule cardiology follow-up within 2-4 weeks")
            report.append("2. Optimize risk factor management")
            report.append("3. Consider additional cardiac testing")
        else:
            report.append("1. Routine follow-up per primary care")
            report.append("2. Continue preventive measures")
            report.append("3. Reassess in 6-12 months")
        
        report.append("")
        report.append("KEY ECG FINDINGS")
        report.append("-" * 40)
        
        key_findings = []
        if 'heart_rate' in ecg_features:
            hr = ecg_features['heart_rate']
            if hr < 60 or hr > 100:
                key_findings.append(f"Heart rate: {hr:.0f} bpm (outside normal range)")
        
        if 'qt_interval' in ecg_features:
            qt = ecg_features['qt_interval']
            if qt > 440:
                key_findings.append(f"QT interval: {qt:.0f} ms (prolonged)")
        
        if 'arrhythmia_type' in ecg_features:
            arrhythmia = ecg_features['arrhythmia_type']
            if arrhythmia != 'Normal Sinus Rhythm':
                key_findings.append(f"Arrhythmia: {arrhythmia}")
        
        for finding in key_findings[:5]:  # Show top 5 findings
            report.append(f"• {finding}")
        
        if not key_findings:
            report.append("• No significant ECG abnormalities detected")
        
        report.append("")
        report.append("DISCLAIMER")
        report.append("-" * 40)
        report.append("This risk assessment is based on automated analysis of ECG data")
        report.append("and should be used as a decision support tool only.")
        report.append("All clinical decisions should be made by qualified healthcare")
        report.append("professionals considering the complete clinical picture.")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def train_ml_risk_model(self, X: np.ndarray, y: np.ndarray, model_type: str = 'random_forest'):
        """Train machine learning model for risk prediction"""
        if not SKLEARN_AVAILABLE:
            print("Scikit-learn not available.")
            return None
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Select model
        if model_type == 'random_forest':
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        elif model_type == 'svm':
            model = SVR(kernel='rbf', C=1.0, gamma='scale')
        elif model_type == 'neural_network':
            model = MLPRegressor(
                hidden_layer_sizes=(100, 50),
                activation='relu',
                solver='adam',
                max_iter=1000,
                random_state=42
            )
        else:
            print(f"Unknown model type: {model_type}")
            return None
        
        # Train model
        print(f"Training {model_type} model...")
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Performance:")
        print(f"  MSE: {mse:.4f}")
        print(f"  MAE: {mae:.4f}")
        print(f"  R²: {r2:.4f}")
        
        # Store model and scaler
        self.models[model_type] = model
        self.scalers[model_type] = scaler
        
        return {
            'model': model,
            'scaler': scaler,
            'metrics': {'mse': mse, 'mae': mae, 'r2': r2},
            'predictions': y_pred,
            'actual': y_test
        }
    
    def predict_with_ml(self, features: np.ndarray, model_type: str = 'random_forest') -> Dict:
        """Predict risk using trained ML model"""
        if model_type not in self.models or model_type not in self.scalers:
            print(f"Model {model_type} not trained.")
            return {}
        
        model = self.models[model_type]
        scaler = self.scalers[model_type]
        
        # Scale features
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        
        # Calculate prediction interval (simplified)
        # In practice, use proper uncertainty quantification
        std_dev = 0.1  # Assuming 10% uncertainty
        lower_bound = max(0, prediction - 1.96 * std_dev)
        upper_bound = min(1, prediction + 1.96 * std_dev)
        
        return {
            'predicted_risk': float(prediction),
            'confidence_interval': (float(lower_bound), float(upper_bound)),
            'confidence_level': 0.95,
            'model_type': model_type
        }
    
    def save_models(self, output_dir: str = 'models'):
        """Save trained models to disk"""
        import os
        import joblib
        
        os.makedirs(output_dir, exist_ok=True)
        
        for model_name, model in self.models.items():
            if model_name in self.scalers:
                # Save model
                model_path = os.path.join(output_dir, f'{model_name}_model.pkl')
                joblib.dump(model, model_path)
                
                # Save scaler
                scaler_path = os.path.join(output_dir, f'{model_name}_scaler.pkl')
                joblib.dump(self.scalers[model_name], scaler_path)
                
                print(f"Saved {model_name} model to {model_path}")
                print(f"Saved {model_name} scaler to {scaler_path}")

def generate_sample_patient_data() -> Dict:
    """Generate sample patient data for demonstration"""
    return {
        'patient_id': 'DEMO001',
        'age': 65,
        'gender': 'Male',
        'hypertension': True,
        'diabetes': False,
        'previous_mi': True,
        'ejection_fraction': 35,
        'family_history_scd': True,
        'smoker': False,
        'cholesterol_total': 220,
        'cholesterol_ldl': 150
    }

def generate_sample_ecg_features() -> Dict:
    """Generate sample ECG features for demonstration"""
    return {
        'heart_rate': 85,
        'hrv': 25,
        'qt_interval': 460,
        'qrs_duration': 110,
        'st_depression': 1.2,
        'st_elevation': 0.0,
        't_wave_inversion': True,
        'pathological_q_waves': False,
        'arrhythmia_type': 'Atrial Fibrillation',
        'arrhythmia_present': True,
        'premature_beats': {'pvc_count': 15, 'pac_count': 30},
        'left_ventricular_hypertrophy': True,
        'brugada_pattern': False,
        'epsilon_waves': False,
        'late_potentials': True
    }

def generate_training_data(n_samples: int = 1000, n_features: int = 20) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic training data"""
    np.random.seed(42)
    
    # Generate features
    X = np.random.randn(n_samples, n_features)
    
    # Create risk scores with some pattern
    risk_scores = np.zeros(n_samples)
    
    # Add risk patterns
    for i in range(n_samples):
        # Age effect
        age_feature = X[i, 0]
        risk_scores[i] += abs(age_feature) * 0.1
        
        # ECG abnormality effects
        for j in range(5, 10):
            risk_scores[i] += abs(X[i, j]) * 0.15
        
        # Comorbidity effects
        for j in range(10, 15):
            risk_scores[i] += max(0, X[i, j]) * 0.2
    
    # Normalize to 0-1 range
    risk_scores = (risk_scores - risk_scores.min()) / (risk_scores.max() - risk_scores.min())
    
    # Add noise
    risk_scores += np.random.normal(0, 0.1, n_samples)
    risk_scores = np.clip(risk_scores, 0, 1)
    
    return X, risk_scores

def main():
    """Demonstration of ECG Risk Stratification System"""
    print("Initializing ECG Risk Stratification System...")
    print("=" * 80)
    
    # Create risk stratification system
    risk_system = ECGRiskStratification()
    
    # Generate sample data
    print("\n1. Loading sample data...")
    patient_data = generate_sample_patient_data()
    ecg_features = generate_sample_ecg_features()
    
    print(f"Patient: {patient_data['patient_id']}, Age: {patient_data['age']}")
    print(f"ECG Findings: HR={ecg_features['heart_rate']} bpm, "
          f"QTc={ecg_features['qt_interval']} ms, "
          f"Arrhythmia={ecg_features['arrhythmia_type']}")
    
    # Calculate basic risk score
    print("\n2. Calculating basic risk score...")
    basic_score = risk_system.calculate_basic_risk_score(ecg_features)
    print(f"Basic Risk Score: {basic_score:.1f}/100")
    print(f"Risk Category: {risk_system._categorize_risk(basic_score/100)}")
    
    # Calculate advanced risk score
    print("\n3. Calculating advanced risk assessment...")
    risk_components = risk_system.calculate_advanced_risk_score(patient_data, ecg_features)
    
    print(f"Composite Risk Score: {risk_components.get('risk_score', 0):.1f}/100")
    print(f"Risk Category: {risk_components.get('risk_category', 'UNKNOWN')}")
    
    # Display component scores
    print("\nRisk Component Scores:")
    for comp in ['arrhythmia_risk', 'ischemia_risk', 'heart_failure_risk', 'scd_risk']:
        if comp in risk_components:
            score = risk_components[comp] * 100
            print(f"  {comp.replace('_', ' ').title()}: {score:.1f}/100")
    
    # Generate comprehensive report
    print("\n4. Generating risk stratification report...")
    report = risk_system.generate_risk_report(patient_data, ecg_features, risk_components)
    print(report)
    
    # Train ML model (if scikit-learn available)
    if SKLEARN_AVAILABLE:
        print("\n5. Training machine learning model...")
        print("-" * 40)
        
        # Generate training data
        X_train, y_train = generate_training_data(n_samples=500, n_features=15)
        print(f"Training data shape: {X_train.shape}")
        print(f"Target shape: {y_train.shape}")
        
        # Train model
        results = risk_system.train_ml_risk_model(X_train, y_train, model_type='random_forest')
        
        # Make prediction with ML model
        print("\n6. Making ML prediction...")
        sample_features = X_train[0:1]  # Use first sample as test
        ml_prediction = risk_system.predict_with_ml(sample_features, model_type='random_forest')
        
        if ml_prediction:
            print(f"Predicted Risk: {ml_prediction['predicted_risk']:.3f}")
            print(f"95% Confidence Interval: {ml_prediction['confidence_interval']}")
        
        # Save models
        print("\n7. Saving trained models...")
        risk_system.save_models(output_dir='risk_models')
    
    # Event probabilities
    print("\n8. Event Risk Probabilities:")
    print("-" * 40)
    
    if 'event_probabilities' in risk_components:
        probs = risk_components['event_probabilities']
        for event, horizons in probs.items():
            if '365_days' in horizons:
                print(f"{event.replace('_', ' ').title()}:")
                print(f"  1-year risk: {horizons['365_days']:.1%}")
    
    print("\n" + "=" * 80)
    print("RISK STRATIFICATION DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nKey Outputs:")
    print("• Comprehensive risk assessment report")
    print("• Risk component analysis")
    print("• Event probability estimates")
    print("• Clinical guideline recommendations")
    print("• ML-based risk prediction (if scikit-learn available)")
    print("\nNote: This is a demonstration system. For clinical use,")
    print("validate with prospectively collected clinical data.")

if __name__ == "__main__":
    main()
