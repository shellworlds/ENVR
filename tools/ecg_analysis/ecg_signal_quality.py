"""
ECG Signal Quality Assessment Tool
Evaluates ECG signal quality using multiple metrics
"""

import numpy as np
from scipy import signal, stats
import pandas as pd
from typing import Dict, Tuple, List

class ECGSignalQualityAssessor:
    """Comprehensive ECG signal quality assessment"""
    
    def __init__(self, sampling_rate: int = 500):
        self.sampling_rate = sampling_rate
        self.quality_thresholds = {
            'snr_db': 20,          # Minimum SNR in dB
            'baseline_wander': 0.1, # Maximum baseline wander (mV)
            'powerline_noise': 0.05, # Maximum powerline noise
            'missing_data': 0.01,   # Maximum missing data percentage
            'clipping': 0.02,       # Maximum clipping percentage
            'saturation': 0.01      # Maximum saturation percentage
        }
    
    def assess_signal_quality(self, ecg_signal: np.ndarray) -> Dict:
        """Comprehensive signal quality assessment"""
        quality_metrics = {}
        
        # Basic statistics
        quality_metrics.update(self._calculate_basic_stats(ecg_signal))
        
        # Signal-to-Noise Ratio
        quality_metrics.update(self._calculate_snr(ecg_signal))
        
        # Baseline wander assessment
        quality_metrics.update(self._assess_baseline_wander(ecg_signal))
        
        # Powerline interference
        quality_metrics.update(self._detect_powerline_noise(ecg_signal))
        
        # Missing data detection
        quality_metrics.update(self._detect_missing_data(ecg_signal))
        
        # Clipping detection
        quality_metrics.update(self._detect_clipping(ecg_signal))
        
        # Saturation detection
        quality_metrics.update(self._detect_saturation(ecg_signal))
        
        # Overall quality score
        quality_metrics['overall_quality_score'] = self._calculate_overall_score(quality_metrics)
        quality_metrics['quality_category'] = self._categorize_quality(quality_metrics['overall_quality_score'])
        
        return quality_metrics
    
    def _calculate_basic_stats(self, ecg_signal: np.ndarray) -> Dict:
        """Calculate basic signal statistics"""
        stats_dict = {
            'mean': float(np.mean(ecg_signal)),
            'std': float(np.std(ecg_signal)),
            'min': float(np.min(ecg_signal)),
            'max': float(np.max(ecg_signal)),
            'range': float(np.ptp(ecg_signal)),
            'rms': float(np.sqrt(np.mean(np.square(ecg_signal)))),
            'skewness': float(stats.skew(ecg_signal)),
            'kurtosis': float(stats.kurtosis(ecg_signal))
        }
        return stats_dict
    
    def _calculate_snr(self, ecg_signal: np.ndarray) -> Dict:
        """Calculate Signal-to-Noise Ratio"""
        # Bandpass filter to isolate ECG frequency band
        nyquist = 0.5 * self.sampling_rate
        low = 0.5 / nyquist
        high = 40.0 / nyquist
        b, a = signal.butter(3, [low, high], btype='band')
        ecg_filtered = signal.filtfilt(b, a, ecg_signal)
        
        # Noise is the difference between original and filtered
        noise = ecg_signal - ecg_filtered
        
        # Calculate power
        signal_power = np.mean(ecg_filtered ** 2)
        noise_power = np.mean(noise ** 2)
        
        # Avoid division by zero
        if noise_power == 0:
            snr_db = 100  # Very high SNR
        else:
            snr_db = 10 * np.log10(signal_power / noise_power)
        
        return {
            'snr_db': snr_db,
            'signal_power': signal_power,
            'noise_power': noise_power,
            'snr_adequate': snr_db >= self.quality_thresholds['snr_db']
        }
    
    def _assess_baseline_wander(self, ecg_signal: np.ndarray) -> Dict:
        """Assess baseline wander using low-frequency components"""
        # Low-pass filter for baseline
        nyquist = 0.5 * self.sampling_rate
        low = 0.5 / nyquist  # 0.5 Hz cutoff
        b, a = signal.butter(2, low, btype='low')
        baseline = signal.filtfilt(b, a, ecg_signal)
        
        # Calculate wander metrics
        wander_amplitude = np.max(np.abs(baseline - np.mean(baseline)))
        wander_frequency = self._estimate_dominant_frequency(baseline, max_freq=2)
        
        return {
            'baseline_wander_amplitude': wander_amplitude,
            'baseline_wander_frequency': wander_frequency,
            'baseline_wander_acceptable': wander_amplitude <= self.quality_thresholds['baseline_wander']
        }
    
    def _detect_powerline_noise(self, ecg_signal: np.ndarray) -> Dict:
        """Detect powerline interference (50/60 Hz)"""
        # Compute power spectrum
        frequencies, power_spectrum = signal.welch(
            ecg_signal, 
            fs=self.sampling_rate, 
            nperseg=min(1024, len(ecg_signal))
        )
        
        # Check for 50Hz and 60Hz peaks
        freq_50_idx = np.argmin(np.abs(frequencies - 50))
        freq_60_idx = np.argmin(np.abs(frequencies - 60))
        
        # Calculate powerline noise ratio
        total_power = np.sum(power_spectrum)
        powerline_power = power_spectrum[freq_50_idx] + power_spectrum[freq_60_idx]
        powerline_ratio = powerline_power / total_power if total_power > 0 else 0
        
        return {
            'powerline_noise_50hz': float(power_spectrum[freq_50_idx]),
            'powerline_noise_60hz': float(power_spectrum[freq_60_idx]),
            'powerline_noise_ratio': powerline_ratio,
            'powerline_interference': powerline_ratio > self.quality_thresholds['powerline_noise']
        }
    
    def _detect_missing_data(self, ecg_signal: np.ndarray) -> Dict:
        """Detect missing or invalid data points"""
        # Check for NaN or infinite values
        nan_count = np.sum(np.isnan(ecg_signal))
        inf_count = np.sum(np.isinf(ecg_signal))
        
        # Check for flatline segments
        diff_signal = np.diff(ecg_signal)
        zero_diff_indices = np.where(np.abs(diff_signal) < 1e-10)[0]
        flatline_segments = self._find_consecutive(zero_diff_indices)
        
        missing_percentage = (nan_count + inf_count) / len(ecg_signal)
        
        return {
            'nan_count': int(nan_count),
            'inf_count': int(inf_count),
            'flatline_segments': len(flatline_segments),
            'missing_data_percentage': missing_percentage,
            'has_missing_data': missing_percentage > self.quality_thresholds['missing_data']
        }
    
    def _detect_clipping(self, ecg_signal: np.ndarray) -> Dict:
        """Detect signal clipping"""
        # Assume normal ECG range is ±5 mV
        normal_max = 5.0
        normal_min = -5.0
        
        clipped_high = np.sum(ecg_signal > normal_max)
        clipped_low = np.sum(ecg_signal < normal_min)
        total_clipped = clipped_high + clipped_low
        
        clipping_percentage = total_clipped / len(ecg_signal)
        
        return {
            'clipped_high_count': int(clipped_high),
            'clipped_low_count': int(clipped_low),
            'clipping_percentage': clipping_percentage,
            'has_clipping': clipping_percentage > self.quality_thresholds['clipping']
        }
    
    def _detect_saturation(self, ecg_signal: np.ndarray) -> Dict:
        """Detect ADC saturation"""
        # Check for maximum/minimum possible values (assuming 16-bit ADC)
        adc_max = 32767  # For 16-bit signed
        adc_min = -32768
        
        # Normalize signal first
        normalized = (ecg_signal - np.mean(ecg_signal)) / np.std(ecg_signal)
        
        # Scale to ADC range
        scaled = normalized * 1000  # Scale to typical ADC range
        
        saturated_high = np.sum(scaled >= adc_max * 0.95)
        saturated_low = np.sum(scaled <= adc_min * 0.95)
        total_saturated = saturated_high + saturated_low
        
        saturation_percentage = total_saturated / len(ecg_signal)
        
        return {
            'saturation_high_count': int(saturated_high),
            'saturation_low_count': int(saturated_low),
            'saturation_percentage': saturation_percentage,
            'has_saturation': saturation_percentage > self.quality_thresholds['saturation']
        }
    
    def _find_consecutive(self, indices: np.ndarray) -> List[np.ndarray]:
        """Find consecutive indices"""
        if len(indices) == 0:
            return []
        
        segments = []
        current_segment = [indices[0]]
        
        for i in range(1, len(indices)):
            if indices[i] == indices[i-1] + 1:
                current_segment.append(indices[i])
            else:
                if len(current_segment) > 1:
                    segments.append(np.array(current_segment))
                current_segment = [indices[i]]
        
        if len(current_segment) > 1:
            segments.append(np.array(current_segment))
        
        return segments
    
    def _estimate_dominant_frequency(self, signal_data: np.ndarray, max_freq: float = 10) -> float:
        """Estimate dominant frequency using FFT"""
        n = len(signal_data)
        frequencies = np.fft.rfftfreq(n, d=1/self.sampling_rate)
        fft_values = np.abs(np.fft.rfft(signal_data))
        
        # Only consider frequencies up to max_freq
        valid_idx = frequencies <= max_freq
        if np.sum(valid_idx) == 0:
            return 0.0
        
        dominant_idx = np.argmax(fft_values[valid_idx])
        return float(frequencies[valid_idx][dominant_idx])
    
    def _calculate_overall_score(self, metrics: Dict) -> float:
        """Calculate overall quality score (0-100)"""
        score = 100.0
        
        # Deductions based on quality issues
        if not metrics.get('snr_adequate', True):
            score -= 20
        
        if not metrics.get('baseline_wander_acceptable', True):
            score -= 15
        
        if metrics.get('powerline_interference', False):
            score -= 10
        
        if metrics.get('has_missing_data', False):
            score -= 20
        
        if metrics.get('has_clipping', False):
            score -= 15
        
        if metrics.get('has_saturation', False):
            score -= 20
        
        return max(0.0, score)
    
    def _categorize_quality(self, score: float) -> str:
        """Categorize signal quality based on score"""
        if score >= 90:
            return "EXCELLENT"
        elif score >= 75:
            return "GOOD"
        elif score >= 60:
            return "FAIR"
        elif score >= 40:
            return "POOR"
        else:
            return "UNACCEPTABLE"
    
    def generate_quality_report(self, metrics: Dict) -> str:
        """Generate comprehensive quality report"""
        report = []
        report.append("=" * 70)
        report.append("ECG SIGNAL QUALITY ASSESSMENT REPORT")
        report.append("=" * 70)
        report.append(f"Overall Quality: {metrics['quality_category']}")
        report.append(f"Quality Score: {metrics['overall_quality_score']:.1f}/100")
        report.append("")
        report.append("Detailed Metrics:")
        report.append(f"  SNR: {metrics.get('snr_db', 0):.1f} dB "
                     f"{'(Adequate)' if metrics.get('snr_adequate', False) else '(Inadequate)'}")
        report.append(f"  Baseline Wander: {metrics.get('baseline_wander_amplitude', 0):.3f} mV "
                     f"{'(Acceptable)' if metrics.get('baseline_wander_acceptable', False) else '(Excessive)'}")
        report.append(f"  Powerline Noise: {metrics.get('powerline_noise_ratio', 0):.3%} "
                     f"{'(Acceptable)' if not metrics.get('powerline_interference', False) else '(Excessive)'}")
        report.append(f"  Missing Data: {metrics.get('missing_data_percentage', 0):.3%} "
                     f"{'(Acceptable)' if not metrics.get('has_missing_data', False) else '(Excessive)'}")
        report.append(f"  Clipping: {metrics.get('clipping_percentage', 0):.3%} "
                     f"{'(Acceptable)' if not metrics.get('has_clipping', False) else '(Excessive)'}")
        report.append(f"  Saturation: {metrics.get('saturation_percentage', 0):.3%} "
                     f"{'(Acceptable)' if not metrics.get('has_saturation', False) else '(Excessive)'}")
        report.append("")
        report.append("Recommendations:")
        
        recommendations = []
        if metrics['overall_quality_score'] < 60:
            recommendations.append("Signal quality is insufficient for clinical analysis.")
            recommendations.append("Consider re-recording with proper electrode placement.")
        
        if metrics.get('powerline_interference', False):
            recommendations.append("Powerline interference detected. Check grounding.")
        
        if metrics.get('has_missing_data', False):
            recommendations.append("Missing data detected. Check electrode connections.")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                report.append(f"  {i}. {rec}")
        else:
            report.append("  Signal quality is acceptable for clinical analysis.")
        
        report.append("=" * 70)
        return "\n".join(report)

def main():
    """Example usage of ECG Signal Quality Assessor"""
    print("Initializing ECG Signal Quality Assessor...")
    assessor = ECGSignalQualityAssessor(sampling_rate=500)
    
    # Generate synthetic ECG for testing
    t = np.linspace(0, 10, 5000)
    clean_ecg = np.sin(2 * np.pi * 1 * t) + 0.5 * np.sin(2 * np.pi * 5 * t)
    
    # Add some noise and artifacts
    noisy_ecg = clean_ecg + 0.1 * np.random.randn(len(t))  # Gaussian noise
    noisy_ecg += 0.05 * np.sin(2 * np.pi * 50 * t)  # Powerline noise
    noisy_ecg[:100] = 0  # Missing data at start
    
    print("Assessing signal quality...")
    quality_metrics = assessor.assess_signal_quality(noisy_ecg)
    
    report = assessor.generate_quality_report(quality_metrics)
    print(report)

if __name__ == "__main__":
    main()
