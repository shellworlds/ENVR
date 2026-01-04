"""
ECG Artifact Detection and Removal Tool
Detects and classifies common ECG artifacts
"""

import numpy as np
from scipy import signal, stats
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class ECGArtifactDetector:
    """Advanced ECG artifact detection and classification"""
    
    def __init__(self, sampling_rate: int = 500):
        self.sampling_rate = sampling_rate
        self.artifact_types = {
            'motion': {'freq_range': (0.1, 10), 'amplitude_threshold': 0.5},
            'electrode_pop': {'duration_max': 0.1, 'amplitude_min': 1.0},
            'muscle_noise': {'freq_range': (20, 100), 'amplitude_threshold': 0.2},
            'baseline_wander': {'freq_range': (0, 0.5), 'amplitude_threshold': 0.3},
            'powerline': {'frequencies': [50, 60], 'amplitude_threshold': 0.1},
            'electrosurgical': {'freq_range': (100, 1000), 'amplitude_threshold': 1.0}
        }
    
    def detect_artifacts(self, ecg_signal: np.ndarray) -> Dict:
        """Comprehensive artifact detection"""
        artifacts = {
            'motion_artifacts': self._detect_motion_artifacts(ecg_signal),
            'electrode_pops': self._detect_electrode_pops(ecg_signal),
            'muscle_noise': self._detect_muscle_noise(ecg_signal),
            'baseline_wander': self._detect_baseline_wander(ecg_signal),
            'powerline_interference': self._detect_powerline_interference(ecg_signal),
            'electrosurgical_noise': self._detect_electrosurgical_noise(ecg_signal)
        }
        
        # Summary statistics
        total_artifacts = sum(len(art['indices']) for art in artifacts.values() if 'indices' in art)
        artifact_duration = total_artifacts / self.sampling_rate
        
        artifacts['summary'] = {
            'total_artifacts': total_artifacts,
            'artifact_duration_seconds': artifact_duration,
            'signal_quality_percentage': max(0, 100 * (1 - artifact_duration / (len(ecg_signal) / self.sampling_rate))),
            'primary_artifact': self._identify_primary_artifact(artifacts)
        }
        
        return artifacts
    
    def _detect_motion_artifacts(self, ecg_signal: np.ndarray) -> Dict:
        """Detect motion artifacts (0.1-10 Hz)"""
        # Bandpass filter for motion artifact frequencies
        nyquist = 0.5 * self.sampling_rate
        low = 0.1 / nyquist
        high = 10.0 / nyquist
        b, a = signal.butter(3, [low, high], btype='band')
        motion_signal = signal.filtfilt(b, a, ecg_signal)
        
        # Detect high-amplitude segments
        threshold = self.artifact_types['motion']['amplitude_threshold']
        motion_indices = np.where(np.abs(motion_signal) > threshold)[0]
        
        # Group consecutive indices
        motion_segments = self._group_consecutive_indices(motion_indices)
        
        return {
            'indices': motion_indices,
            'segments': motion_segments,
            'count': len(motion_segments),
            'total_duration': len(motion_indices) / self.sampling_rate,
            'amplitude_mean': float(np.mean(np.abs(motion_signal[motion_indices])) if len(motion_indices) > 0 else 0)
        }
    
    def _detect_electrode_pops(self, ecg_signal: np.ndarray) -> Dict:
        """Detect electrode pops (sudden spikes)"""
        # Calculate derivative to find rapid changes
        derivative = np.diff(ecg_signal)
        
        # Detect spikes (rapid changes exceeding threshold)
        spike_threshold = 5.0 * np.std(derivative)
        spike_indices = np.where(np.abs(derivative) > spike_threshold)[0]
        
        # Ensure spikes are sufficiently separated
        min_gap = int(0.05 * self.sampling_rate)  # 50ms minimum gap
        if len(spike_indices) > 0:
            filtered_indices = [spike_indices[0]]
            for idx in spike_indices[1:]:
                if idx - filtered_indices[-1] > min_gap:
                    filtered_indices.append(idx)
            spike_indices = np.array(filtered_indices)
        
        return {
            'indices': spike_indices,
            'count': len(spike_indices),
            'amplitude_mean': float(np.mean(np.abs(derivative[spike_indices])) if len(spike_indices) > 0 else 0),
            'rate_per_minute': len(spike_indices) / (len(ecg_signal) / self.sampling_rate) * 60
        }
    
    def _detect_muscle_noise(self, ecg_signal: np.ndarray) -> Dict:
        """Detect muscle noise/EMG artifacts (20-100 Hz)"""
        # Bandpass filter for muscle noise frequencies
        nyquist = 0.5 * self.sampling_rate
        low = 20.0 / nyquist
        high = 100.0 / nyquist
        b, a = signal.butter(3, [low, high], btype='band')
        muscle_signal = signal.filtfilt(b, a, ecg_signal)
        
        # Calculate RMS in sliding windows
        window_size = int(0.1 * self.sampling_rate)  # 100ms windows
        rms_values = np.zeros(len(muscle_signal))
        for i in range(len(muscle_signal) - window_size):
            rms_values[i] = np.sqrt(np.mean(muscle_signal[i:i+window_size] ** 2))
        
        # Detect high-RMS segments
        threshold = self.artifact_types['muscle_noise']['amplitude_threshold']
        noise_indices = np.where(rms_values > threshold)[0]
        noise_segments = self._group_consecutive_indices(noise_indices)
        
        return {
            'indices': noise_indices,
            'segments': noise_segments,
            'count': len(noise_segments),
            'total_duration': len(noise_indices) / self.sampling_rate,
            'rms_mean': float(np.mean(rms_values[noise_indices]) if len(noise_indices) > 0 else 0)
        }
    
    def _detect_baseline_wander(self, ecg_signal: np.ndarray) -> Dict:
        """Detect baseline wander (<0.5 Hz)"""
        # Low-pass filter for baseline
        nyquist = 0.5 * self.sampling_rate
        low = 0.5 / nyquist
        b, a = signal.butter(2, low, btype='low')
        baseline = signal.filtfilt(b, a, ecg_signal)
        
        # Calculate wander amplitude
        wander_amplitude = np.max(baseline) - np.min(baseline)
        
        # Detect excessive wander
        threshold = self.artifact_types['baseline_wander']['amplitude_threshold']
        has_excessive_wander = wander_amplitude > threshold
        
        return {
            'amplitude': wander_amplitude,
            'has_excessive_wander': has_excessive_wander,
            'frequency_components': self._analyze_baseline_frequencies(baseline)
        }
    
    def _detect_powerline_interference(self, ecg_signal: np.ndarray) -> Dict:
        """Detect 50/60 Hz powerline interference"""
        frequencies, power_spectrum = signal.welch(
            ecg_signal, 
            fs=self.sampling_rate, 
            nperseg=min(1024, len(ecg_signal))
        )
        
        # Check for 50Hz and 60Hz peaks
        powerline_data = {}
        for freq in self.artifact_types['powerline']['frequencies']:
            freq_idx = np.argmin(np.abs(frequencies - freq))
            power_at_freq = power_spectrum[freq_idx]
            
            # Calculate signal-to-powerline ratio
            total_power = np.sum(power_spectrum)
            pl_ratio = power_at_freq / total_power if total_power > 0 else 0
            
            powerline_data[f'{freq}_hz'] = {
                'power': float(power_at_freq),
                'ratio': float(pl_ratio),
                'interference': pl_ratio > self.artifact_types['powerline']['amplitude_threshold']
            }
        
        return powerline_data
    
    def _detect_electrosurgical_noise(self, ecg_signal: np.ndarray) -> Dict:
        """Detect electrosurgical noise (100-1000 Hz)"""
        # High-pass filter for electrosurgical frequencies
        nyquist = 0.5 * self.sampling_rate
        low = 100.0 / nyquist
        b, a = signal.butter(3, low, btype='high')
        es_signal = signal.filtfilt(b, a, ecg_signal)
        
        # Calculate power in high-frequency band
        es_power = np.mean(es_signal ** 2)
        
        # Compare with total power
        total_power = np.mean(ecg_signal ** 2)
        es_ratio = es_power / total_power if total_power > 0 else 0
        
        return {
            'power': es_power,
            'ratio': es_ratio,
            'has_electrosurgical_noise': es_ratio > self.artifact_types['electrosurgical']['amplitude_threshold']
        }
    
    def _group_consecutive_indices(self, indices: np.ndarray, max_gap: int = None) -> List[np.ndarray]:
        """Group consecutive indices into segments"""
        if len(indices) == 0:
            return []
        
        if max_gap is None:
            max_gap = int(0.02 * self.sampling_rate)  # 20ms default
        
        segments = []
        current_segment = [indices[0]]
        
        for i in range(1, len(indices)):
            if indices[i] - indices[i-1] <= max_gap:
                current_segment.append(indices[i])
            else:
                segments.append(np.array(current_segment))
                current_segment = [indices[i]]
        
        segments.append(np.array(current_segment))
        return segments
    
    def _analyze_baseline_frequencies(self, baseline_signal: np.ndarray) -> Dict:
        """Analyze frequency components of baseline wander"""
        frequencies, power_spectrum = signal.welch(
            baseline_signal, 
            fs=self.sampling_rate, 
            nperseg=min(512, len(baseline_signal))
        )
        
        # Find dominant frequency below 0.5 Hz
        low_freq_idx = frequencies <= 0.5
        if np.any(low_freq_idx):
            dominant_idx = np.argmax(power_spectrum[low_freq_idx])
            dominant_freq = frequencies[low_freq_idx][dominant_idx]
            dominant_power = power_spectrum[low_freq_idx][dominant_idx]
        else:
            dominant_freq = 0.0
            dominant_power = 0.0
        
        return {
            'dominant_frequency': dominant_freq,
            'dominant_power': dominant_power,
            'total_power': float(np.sum(power_spectrum[low_freq_idx]) if np.any(low_freq_idx) else 0)
        }
    
    def _identify_primary_artifact(self, artifacts: Dict) -> str:
        """Identify the most significant artifact"""
        artifact_scores = {}
        
        # Score motion artifacts
        motion = artifacts['motion_artifacts']
        artifact_scores['motion'] = motion['count'] * 10 + motion['total_duration'] * 5
        
        # Score electrode pops
        pops = artifacts['electrode_pops']
        artifact_scores['electrode_pops'] = pops['count'] * 15
        
        # Score muscle noise
        muscle = artifacts['muscle_noise']
        artifact_scores['muscle_noise'] = muscle['total_duration'] * 8
        
        # Score baseline wander
        wander = artifacts['baseline_wander']
        artifact_scores['baseline_wander'] = wander['amplitude'] * 20 if wander['has_excessive_wander'] else 0
        
        # Score powerline interference
        powerline = artifacts['powerline_interference']
        pl_score = 0
        for freq_data in powerline.values():
            if isinstance(freq_data, dict) and freq_data.get('interference', False):
                pl_score += 25
        artifact_scores['powerline'] = pl_score
        
        # Score electrosurgical noise
        es = artifacts['electrosurgical_noise']
        artifact_scores['electrosurgical'] = 30 if es['has_electrosurgical_noise'] else 0
        
        # Find primary artifact
        if not artifact_scores:
            return "NONE"
        
        primary = max(artifact_scores.items(), key=lambda x: x[1])
        return primary[0] if primary[1] > 0 else "NONE"
    
    def remove_artifacts(self, ecg_signal: np.ndarray, artifacts: Dict) -> np.ndarray:
        """Apply artifact removal techniques"""
        cleaned_signal = ecg_signal.copy()
        
        # Remove motion artifacts (median filtering)
        motion_indices = artifacts['motion_artifacts']['indices']
        if len(motion_indices) > 0:
            window_size = int(0.1 * self.sampling_rate)  # 100ms window
            for idx in motion_indices:
                start = max(0, idx - window_size // 2)
                end = min(len(cleaned_signal), idx + window_size // 2)
                if end > start:
                    cleaned_signal[idx] = np.median(cleaned_signal[start:end])
        
        # Remove electrode pops (spike removal)
        pop_indices = artifacts['electrode_pops']['indices']
        if len(pop_indices) > 0:
            for idx in pop_indices:
                if 0 < idx < len(cleaned_signal) - 1:
                    # Replace spike with linear interpolation
                    cleaned_signal[idx] = (cleaned_signal[idx-1] + cleaned_signal[idx+1]) / 2
        
        # Remove baseline wander
        if artifacts['baseline_wander']['has_excessive_wander']:
            # High-pass filter to remove low-frequency wander
            nyquist = 0.5 * self.sampling_rate
            highpass_cutoff = 0.5 / nyquist
            b, a = signal.butter(3, highpass_cutoff, btype='high')
            cleaned_signal = signal.filtfilt(b, a, cleaned_signal)
        
        return cleaned_signal
    
    def generate_artifact_report(self, artifacts: Dict) -> str:
        """Generate comprehensive artifact report"""
        report = []
        report.append("=" * 70)
        report.append("ECG ARTIFACT DETECTION REPORT")
        report.append("=" * 70)
        
        summary = artifacts['summary']
        report.append(f"Signal Quality: {summary['signal_quality_percentage']:.1f}%")
        report.append(f"Primary Artifact: {summary['primary_artifact'].upper()}")
        report.append(f"Total Artifact Duration: {summary['artifact_duration_seconds']:.2f} seconds")
        report.append("")
        report.append("Detailed Artifact Analysis:")
        report.append("")
        
        # Motion artifacts
        motion = artifacts['motion_artifacts']
        report.append("1. MOTION ARTIFACTS:")
        report.append(f"   Count: {motion['count']}")
        report.append(f"   Duration: {motion['total_duration']:.2f} seconds")
        report.append(f"   Mean Amplitude: {motion['amplitude_mean']:.3f} mV")
        
        # Electrode pops
        pops = artifacts['electrode_pops']
        report.append("")
        report.append("2. ELECTRODE POPS:")
        report.append(f"   Count: {pops['count']}")
        report.append(f"   Rate: {pops['rate_per_minute']:.1f} per minute")
        report.append(f"   Mean Amplitude: {pops['amplitude_mean']:.3f} mV/ms")
        
        # Muscle noise
        muscle = artifacts['muscle_noise']
        report.append("")
        report.append("3. MUSCLE NOISE:")
        report.append(f"   Segments: {muscle['count']}")
        report.append(f"   Duration: {muscle['total_duration']:.2f} seconds")
        report.append(f"   Mean RMS: {muscle['rms_mean']:.3f} mV")
        
        # Baseline wander
        wander = artifacts['baseline_wander']
        report.append("")
        report.append("4. BASELINE WANDER:")
        report.append(f"   Amplitude: {wander['amplitude']:.3f} mV")
        report.append(f"   Excessive: {'YES' if wander['has_excessive_wander'] else 'NO'}")
        if wander['frequency_components']['dominant_frequency'] > 0:
            report.append(f"   Dominant Frequency: {wander['frequency_components']['dominant_frequency']:.2f} Hz")
        
        # Powerline interference
        powerline = artifacts['powerline_interference']
        report.append("")
        report.append("5. POWERLINE INTERFERENCE:")
        for freq, data in powerline.items():
            if isinstance(data, dict):
                report.append(f"   {freq}: {data['power']:.3e} (Ratio: {data['ratio']:.3%})")
                if data['interference']:
                    report.append("        ⚠️  SIGNIFICANT INTERFERENCE DETECTED")
        
        # Electrosurgical noise
        es = artifacts['electrosurgical_noise']
        report.append("")
        report.append("6. ELECTROSURGICAL NOISE:")
        report.append(f"   Power Ratio: {es['ratio']:.3%}")
        report.append(f"   Detected: {'YES' if es['has_electrosurgical_noise'] else 'NO'}")
        
        report.append("")
        report.append("RECOMMENDATIONS:")
        
        recommendations = []
        if summary['primary_artifact'] == 'motion':
            recommendations.append("• Ensure patient is still during recording")
            recommendations.append("• Check electrode adhesion")
        elif summary['primary_artifact'] == 'electrode_pops':
            recommendations.append("• Check electrode connections")
            recommendations.append("• Ensure proper skin preparation")
        elif summary['primary_artifact'] == 'muscle_noise':
            recommendations.append("• Ask patient to relax muscles")
            recommendations.append("• Ensure comfortable positioning")
        elif summary['primary_artifact'] == 'baseline_wander':
            recommendations.append("• Check for respiratory interference")
            recommendations.append("• Ensure stable electrode contact")
        elif summary['primary_artifact'] == 'powerline':
            recommendations.append("• Check equipment grounding")
            recommendations.append("• Use proper shielding")
        elif summary['primary_artifact'] == 'electrosurgical':
            recommendations.append("• Move away from electrosurgical equipment")
            recommendations.append("• Use proper filtering")
        
        if summary['signal_quality_percentage'] < 80:
            recommendations.append("• Consider re-recording with improved setup")
        
        for i, rec in enumerate(recommendations, 1):
            report.append(f"   {i}. {rec}")
        
        if not recommendations:
            report.append("   Signal quality is acceptable for clinical analysis.")
        
        report.append("=" * 70)
        return "\n".join(report)

def main():
    """Example usage of ECG Artifact Detector"""
    print("Initializing ECG Artifact Detector...")
    detector = ECGArtifactDetector(sampling_rate=500)
    
    # Generate synthetic ECG with artifacts
    t = np.linspace(0, 10, 5000)
    clean_ecg = np.sin(2 * np.pi * 1 * t) + 0.5 * np.sin(2 * np.pi * 5 * t)
    
    # Add artifacts
    noisy_ecg = clean_ecg.copy()
    
    # Add motion artifact (segment of increased amplitude)
    motion_start = 1000
    motion_end = 1500
    noisy_ecg[motion_start:motion_end] += 0.8 * np.random.randn(motion_end - motion_start)
    
    # Add electrode pops
    pop_indices = [500, 1500, 2500]
    for idx in pop_indices:
        noisy_ecg[idx] += 2.0
    
    # Add baseline wander
    noisy_ecg += 0.3 * np.sin(2 * np.pi * 0.2 * t)
    
    # Add powerline interference
    noisy_ecg += 0.1 * np.sin(2 * np.pi * 50 * t)
    
    print("Detecting artifacts...")
    artifacts = detector.detect_artifacts(noisy_ecg)
    
    report = detector.generate_artifact_report(artifacts)
    print(report)
    
    print("\nCleaning signal...")
    cleaned_ecg = detector.remove_artifacts(noisy_ecg, artifacts)
    
    print(f"Original signal std: {np.std(noisy_ecg):.3f}")
    print(f"Cleaned signal std: {np.std(cleaned_ecg):.3f}")
    print(f"Noise reduction: {100 * (1 - np.std(cleaned_ecg) / np.std(noisy_ecg)):.1f}%")

if __name__ == "__main__":
    main()
