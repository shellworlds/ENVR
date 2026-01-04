"""
ECG Clinical Decision Support System
Evidence-based clinical decision support for ECG interpretation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

class ClinicalDecisionSupport:
    """Evidence-based clinical decision support system for ECG interpretation"""
    
    def __init__(self):
        self.clinical_guidelines = {
            'aha_2023': self._aha_2023_guidelines,
            'esc_2022': self._esc_2022_guidelines,
            'acc_2023': self._acc_2023_guidelines
        }
        
        self.diagnostic_criteria = self._load_diagnostic_criteria()
        self.treatment_recommendations = self._load_treatment_guidelines()
        self.risk_stratification = self._load_risk_stratification()
        
    def _aha_2023_guidelines(self):
        """American Heart Association 2023 ECG guidelines"""
        return {
            'qtc_normal': {'male': 350, 'female': 360},
            'qtc_prolonged': 450,
            'qtc_severe': 500,
            'bradycardia': 50,
            'tachycardia': 100,
            'st_elevation': 0.1,
            'st_depression': 0.05
        }
    
    def _esc_2022_guidelines(self):
        """European Society of Cardiology 2022 guidelines"""
        return {
            'afib_management': ['Rate control', 'Rhythm control', 'Anticoagulation'],
            'vt_management': ['Antiarrhythmics', 'ICD', 'Ablation'],
            'heart_failure': ['ACE inhibitors', 'Beta blockers', 'Diuretics']
        }
    
    def _acc_2023_guidelines(self):
        """American College of Cardiology 2023 guidelines"""
        return {
            'risk_categories': ['Low', 'Intermediate', 'High', 'Very High'],
            'followup_intervals': {'Low': 12, 'Intermediate': 6, 'High': 3, 'Very High': 1}
        }
    
    def _load_diagnostic_criteria(self):
        """Load diagnostic criteria for various ECG abnormalities"""
        return {
            'atrial_fibrillation': {
                'criteria': ['Irregularly irregular rhythm', 'No P waves', 'Variable R-R intervals'],
                'confidence': 0.95
            },
            'ventricular_tachycardia': {
                'criteria': ['Wide QRS (>120ms)', 'AV dissociation', 'Fusion beats'],
                'confidence': 0.90
            },
            'myocardial_infarction': {
                'criteria': ['ST elevation >1mm in 2 contiguous leads', 'New Q waves', 'T wave inversion'],
                'confidence': 0.85
            }
        }
    
    def analyze_ecg(self, ecg_data: Dict, patient_info: Dict = None) -> Dict:
        """
        Analyze ECG data and provide clinical recommendations
        
        Args:
            ecg_data: Dictionary containing ECG features
            patient_info: Optional patient demographic information
            
        Returns:
            Dictionary with analysis results and recommendations
        """
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'findings': [],
            'diagnoses': [],
            'recommendations': [],
            'risk_level': 'Unknown',
            'urgency': 'Routine'
        }
        
        # Basic rhythm analysis
        if 'heart_rate' in ecg_data:
            hr = ecg_data['heart_rate']
            if hr < 50:
                analysis['findings'].append('Bradycardia')
                analysis['urgency'] = 'Urgent' if hr < 40 else 'Semi-urgent'
            elif hr > 100:
                analysis['findings'].append('Tachycardia')
                analysis['urgency'] = 'Urgent' if hr > 150 else 'Semi-urgent'
        
        # QTc analysis
        if 'qtc' in ecg_data:
            qtc = ecg_data['qtc']
            if qtc > 450:
                analysis['findings'].append('QTc prolongation')
                if qtc > 500:
                    analysis['diagnoses'].append('Long QT Syndrome')
                    analysis['urgency'] = 'Emergent'
        
        # Generate recommendations
        self._generate_recommendations(analysis, patient_info)
        
        # Calculate risk level
        analysis['risk_level'] = self._calculate_risk_level(analysis)
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict, patient_info: Dict):
        """Generate clinical recommendations based on findings"""
        recommendations = []
        
        if 'Bradycardia' in analysis['findings']:
            recommendations.append('Consider 24-hour Holter monitoring')
            recommendations.append('Check thyroid function tests')
            recommendations.append('Review medications for bradycardic agents')
        
        if 'Tachycardia' in analysis['findings']:
            recommendations.append('Consider stress testing')
            recommendations.append('Evaluate for anemia or infection')
            recommendations.append('Check electrolytes')
        
        if 'QTc prolongation' in analysis['findings']:
            recommendations.append('Discontinue QT-prolonging medications')
            recommendations.append('Check potassium and magnesium levels')
            recommendations.append('Consider cardiology referral')
        
        analysis['recommendations'] = recommendations
    
    def _calculate_risk_level(self, analysis: Dict) -> str:
        """Calculate overall risk level"""
        urgency_map = {
            'Emergent': 'Very High',
            'Urgent': 'High',
            'Semi-urgent': 'Intermediate',
            'Routine': 'Low'
        }
        return urgency_map.get(analysis['urgency'], 'Unknown')
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a clinical report from analysis"""
        report = f"CLINICAL ECG REPORT\n"
        report += f"Generated: {analysis['timestamp']}\n"
        report += f"Urgency: {analysis['urgency']}\n"
        report += f"Risk Level: {analysis['risk_level']}\n\n"
        
        if analysis['findings']:
            report += "FINDINGS:\n"
            for finding in analysis['findings']:
                report += f"  • {finding}\n"
        
        if analysis['diagnoses']:
            report += "\nDIAGNOSES:\n"
            for diagnosis in analysis['diagnoses']:
                report += f"  • {diagnosis}\n"
        
        if analysis['recommendations']:
            report += "\nRECOMMENDATIONS:\n"
            for rec in analysis['recommendations']:
                report += f"  • {rec}\n"
        
        return report

# Example usage
if __name__ == "__main__":
    cds = ClinicalDecisionSupport()
    
    # Sample ECG data
    sample_ecg = {
        'heart_rate': 45,
        'qtc': 480,
        'rhythm': 'Sinus bradycardia',
        'pr_interval': 200,
        'qrs_duration': 90
    }
    
    sample_patient = {
        'age': 65,
        'gender': 'Male',
        'medications': ['Metoprolol', 'Lisinopril']
    }
    
    analysis = cds.analyze_ecg(sample_ecg, sample_patient)
    report = cds.generate_report(analysis)
    print(report)
