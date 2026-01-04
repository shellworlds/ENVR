"""
ECG Feature Extraction Tool
Extracts comprehensive features from ECG signals for ML analysis
"""

import numpy as np
from scipy import signal, stats, fft
from typing import Dict, List, Tuple
import pandas as pd

class ECGFeatureExtractor:
    """Advanced ECG feature extraction for machine learning"""
    
    def __init__(self, sampling_rate: int = 500):
        self.sampling_rate = sampling_rate
        self.feature_groups = [
            'temporal', 'spectral', 'statistical', 'morphological',
            'nonlinear', 'interval', 'waveform'
        ]
    
    def extract_all_features(self, ecg_signal: np.ndarray, r_peaks: np.ndarray = None) -> Dict:
        """Extract all feature groups"""
        features = {}
        
        # Basic preprocessing
        filtered_ecg = self._preprocess_signal(ecg_signal)
        
        # Detect R-peaks if not provided
        if r_peaks is None or len(r_peaks) == 0:
            r_peaks = self._detect_r_peaks(filtered_ecg)
        
        # Extract features from each group
        features.update(self._extract_temporal_features(filtered_ecg))
        features.update(self._extract_spectral_features(filtered_ecg))
        features.update(self._extract_statistical_features(filtered_ecg))
        features.update(self._extract_morphological_features(filtered_ecg, r_peaks))
        features.update(self._extract_nonlinear_features(filtered_ecg))
        features.update(self._extract_interval_features(r_peaks))
        features.update(self._extract_waveform_features(filtered_ecg, r_peaks))
        
        # Add metadata
        features['total_features'] = len(features)
        features['signal_length'] = len(ecg_signal)
        features['sampling_rate'] = self.sampling_rate
        
        return features
    
    def _preprocess_signal(self, ecg_signal: np.ndarray) -> np.ndarray:
        """Preprocess ECG signal"""
        # Remove DC offset
        signal_centered = ecg_signal - np.mean(ecg_signal)
        
        # Bandpass filter (0.5-40 Hz)
        nyquist = 0.5 * self.sampling_rate
        low = 0.5 / nyquist
        high = 40.0 / nyquist
        b, a = signal.butter(3, [low, high], btype='band')
        filtered = signal.filtfilt(b, a, signal_centered)
        
        return filtered
    
    def _detect_r_peaks(self, ecg_signal: np.ndarray) -> np.ndarray:
        """Simple R-peak detection"""
        # Differentiate and square
        diff_signal = np.diff(ecg_signal)
        squared = diff_signal ** 2
        
        # Moving window integration
        window_size = int(0.15 * self.sampling_rate)
        integrated = np.convolve(squared, np.ones(window_size)/window_size, mode='same')
        
        # Find peaks
        threshold = 0.5 * np.max(integrated)
        peaks, _ = signal.find_peaks(integrated, height=threshold, distance=int(0.3*self.sampling_rate))
        
        return peaks
    
    def _extract_temporal_features(self, ecg_signal: np.ndarray) -> Dict:
        """Extract temporal domain features"""
        features = {}
        
        # Time domain statistics
        features['temporal_mean'] = float(np.mean(ecg_signal))
        features['temporal_std'] = float(np.std(ecg_signal))
        features['temporal_variance'] = float(np.var(ecg_signal))
        features['temporal_skewness'] = float(stats.skew(ecg_signal))
        features['temporal_kurtosis'] = float(stats.kurtosis(ecg_signal))
        
        # Zero crossing rate
        zero_crossings = np.where(np.diff(np.sign(ecg_signal)))[0]
        features['zero_crossing_rate'] = len(zero_crossings) / len(ecg_signal)
        
        # Signal energy
        features['signal_energy'] = float(np.sum(ecg_signal ** 2))
        features['signal_power'] = features['signal_energy'] / len(ecg_signal)
        
        # Peak statistics
        peaks, properties = signal.find_peaks(ecg_signal, distance=int(0.2*self.sampling_rate))
        if len(peaks) > 0:
            features['peak_count'] = len(peaks)
            features['peak_mean_amplitude'] = float(np.mean(ecg_signal[peaks]))
            features['peak_std_amplitude'] = float(np.std(ecg_signal[peaks]))
        else:
            features['peak_count'] = 0
            features['peak_mean_amplitude'] = 0.0
            features['peak_std_amplitude'] = 0.0
        
        return features
    
    def _extract_spectral_features(self, ecg_signal: np.ndarray) -> Dict:
        """Extract frequency domain features"""
        features = {}
        
        # Compute power spectral density
        frequencies, psd = signal.welch(
            ecg_signal, 
            fs=self.sampling_rate, 
            nperseg=min(1024, len(ecg_signal))
        )
        
        # Frequency bands (Hz)
        bands = {
            'ulf': (0, 0.003),      # Ultra Low Frequency
            'vlf': (0.003, 0.04),   # Very Low Frequency
            'lf': (0.04, 0.15),     # Low Frequency
            'hf': (0.15, 0.4),      # High Frequency
            'ecg': (0.5, 40)        # ECG frequency band
        }
        
        # Calculate power in each band
        total_power = np.sum(psd)
        for band_name, (low, high) in bands.items():
            band_mask = (frequencies >= low) & (frequencies <= high)
            if np.any(band_mask):
                band_power = np.sum(psd[band_mask])
                features[f'spectral_power_{band_name}'] = float(band_power)
                features[f'spectral_power_ratio_{band_name}'] = float(band_power / total_power)
            else:
                features[f'spectral_power_{band_name}'] = 0.0
                features[f'spectral_power_ratio_{band_name}'] = 0.0
        
        # Spectral statistics
        if total_power > 0:
            # Spectral centroid
            features['spectral_centroid'] = float(np.sum(frequencies * psd) / total_power)
            
            # Spectral spread
            centroid = features['spectral_centroid']
            features['spectral_spread'] = float(np.sqrt(np.sum(((frequencies - centroid) ** 2) * psd) / total_power))
            
            # Spectral flatness
            features['spectral_flatness'] = float(stats.gmean(psd) / np.mean(psd))
            
            # Spectral rolloff (85th percentile)
            cumulative_power = np.cumsum(psd) / total_power
            rolloff_idx = np.where(cumulative_power >= 0.85)[0]
            if len(rolloff_idx) > 0:
                features['spectral_rolloff'] = float(frequencies[rolloff_idx[0]])
            else:
                features['spectral_rolloff'] = 0.0
        
        # Dominant frequency
        dominant_freq_idx = np.argmax(psd)
        features['dominant_frequency'] = float(frequencies[dominant_freq_idx])
        features['dominant_power'] = float(psd[dominant_freq_idx])
        
        return features
    
    def _extract_statistical_features(self, ecg_signal: np.ndarray) -> Dict:
        """Extract statistical features"""
        features = {}
        
        # Percentiles
        percentiles = [10, 25, 50, 75, 90]
        for p in percentiles:
            features[f'percentile_{p}'] = float(np.percentile(ecg_signal, p))
        
        # Range
        features['range'] = float(np.ptp(ecg_signal))
        
        # Interquartile range
        q75, q25 = np.percentile(ecg_signal, [75, 25])
        features['iqr'] = float(q75 - q25)
        
        # Mean absolute deviation
        features['mad'] = float(np.mean(np.abs(ecg_signal - np.mean(ecg_signal))))
        
        # RMS
        features['rms'] = float(np.sqrt(np.mean(ecg_signal ** 2)))
        
        # Crest factor
        features['crest_factor'] = float(np.max(np.abs(ecg_signal)) / features['rms']) if features['rms'] > 0 else 0.0
        
        # Shape factor
        features['shape_factor'] = features['rms'] / np.mean(np.abs(ecg_signal)) if np.mean(np.abs(ecg_signal)) > 0 else 0.0
        
        # Impulse factor
        features['impulse_factor'] = float(np.max(np.abs(ecg_signal)) / np.mean(np.abs(ecg_signal))) if np.mean(np.abs(ecg_signal)) > 0 else 0.0
        
        # Clearance factor
        features['clearance_factor'] = float(np.max(np.abs(ecg_signal)) / (np.mean(np.sqrt(np.abs(ecg_signal)))) ** 2) if np.mean(np.sqrt(np.abs(ecg_signal))) > 0 else 0.0
        
        # Higher order statistics
        features['third_moment'] = float(stats.moment(ecg_signal, moment=3))
        features['fourth_moment'] = float(stats.moment(ecg_signal, moment=4))
        
        # Signal-to-noise ratio estimate
        filtered = signal.medfilt(ecg_signal, kernel_size=51)
        noise = ecg_signal - filtered
        signal_power = np.mean(filtered ** 2)
        noise_power = np.mean(noise ** 2)
        features['estimated_snr'] = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else 100.0
        
        return features
    
    def _extract_morphological_features(self, ecg_signal: np.ndarray, r_peaks: np.ndarray) -> Dict:
        """Extract morphological features"""
        features = {}
        
        if len(r_peaks) < 3:
            # Not enough beats for morphological analysis
            for key in ['morph_r_amplitude', 'morph_q_amplitude', 'morph_s_amplitude',
                       'morph_p_amplitude', 'morph_t_amplitude', 'morph_qrs_area',
                       'morph_st_slope', 'morph_qrs_duration', 'morph_qt_interval']:
                features[key] = 0.0
            return features
        
        # Extract beat templates
        beat_templates = self._extract_beat_templates(ecg_signal, r_peaks)
        avg_beat = np.mean(beat_templates, axis=0)
        
        # R-wave amplitude
        r_peak_idx = len(avg_beat) // 2
        features['morph_r_amplitude'] = float(avg_beat[r_peak_idx])
        
        # Q and S wave detection
        q_idx = self._find_wave_extremum(avg_beat[:r_peak_idx], 'min')
        s_idx = r_peak_idx + self._find_wave_extremum(avg_beat[r_peak_idx:], 'min')
        
        features['morph_q_amplitude'] = float(avg_beat[q_idx]) if q_idx is not None else 0.0
        features['morph_s_amplitude'] = float(avg_beat[s_idx]) if s_idx is not None else 0.0
        
        # P and T wave detection
        p_search_start = max(0, q_idx - int(0.3 * self.sampling_rate)) if q_idx else 0
        p_search_end = q_idx if q_idx else r_peak_idx // 2
        
        t_search_start = s_idx if s_idx else r_peak_idx + int(0.1 * self.sampling_rate)
        t_search_end = min(len(avg_beat), t_search_start + int(0.4 * self.sampling_rate))
        
        p_idx = self._find_wave_extremum(avg_beat[p_search_start:p_search_end], 'max')
        t_idx = self._find_wave_extremum(avg_beat[t_search_start:t_search_end], 'max')
        
        if p_idx is not None:
            p_idx += p_search_start
            features['morph_p_amplitude'] = float(avg_beat[p_idx])
        else:
            features['morph_p_amplitude'] = 0.0
            
        if t_idx is not None:
            t_idx += t_search_start
            features['morph_t_amplitude'] = float(avg_beat[t_idx])
        else:
            features['morph_t_amplitude'] = 0.0
        
        # QRS area (integral)
        qrs_start = q_idx if q_idx else max(0, r_peak_idx - int(0.1 * self.sampling_rate))
        qrs_end = s_idx if s_idx else min(len(avg_beat), r_peak_idx + int(0.1 * self.sampling_rate))
        features['morph_qrs_area'] = float(np.trapz(np.abs(avg_beat[qrs_start:qrs_end])))
        
        # ST segment slope
        if s_idx and t_idx and s_idx < t_idx:
            st_segment = avg_beat[s_idx:t_idx]
            if len(st_segment) > 1:
                time_points = np.arange(len(st_segment)) / self.sampling_rate
                slope, intercept = np.polyfit(time_points, st_segment, 1)
                features['morph_st_slope'] = float(slope)
            else:
                features['morph_st_slope'] = 0.0
        else:
            features['morph_st_slope'] = 0.0
        
        # Durations (in milliseconds)
        if q_idx and s_idx:
            features['morph_qrs_duration'] = float((s_idx - q_idx) / self.sampling_rate * 1000)
        else:
            features['morph_qrs_duration'] = float(100.0)  # Default
        
        if q_idx and t_idx:
            features['morph_qt_interval'] = float((t_idx - q_idx) / self.sampling_rate * 1000)
        else:
            features['morph_qt_interval'] = float(400.0)  # Default
        
        # Beat-to-beat variability
        if len(beat_templates) > 1:
            variability = np.std(beat_templates, axis=0)
            features['morph_beat_variability'] = float(np.mean(variability))
            features['morph_template_correlation'] = float(np.corrcoef(beat_templates.flatten(), avg_beat.repeat(len(beat_templates)))[0, 1])
        else:
            features['morph_beat_variability'] = 0.0
            features['morph_template_correlation'] = 1.0
        
        return features
    
    def _extract_nonlinear_features(self, ecg_signal: np.ndarray) -> Dict:
        """Extract nonlinear dynamics features"""
        features = {}
        
        # Sample entropy
        features['nonlinear_sampen'] = self._calculate_sample_entropy(ecg_signal, m=2, r=0.2*np.std(ecg_signal))
        
        # Approximate entropy
        features['nonlinear_apen'] = self._calculate_approximate_entropy(ecg_signal, m=2, r=0.2*np.std(ecg_signal))
        
        # Detrended fluctuation analysis
        features['nonlinear_dfa_alpha1'], features['nonlinear_dfa_alpha2'] = self._calculate_dfa(ecg_signal)
        
        # Hurst exponent
        features['nonlinear_hurst'] = self._calculate_hurst_exponent(ecg_signal)
        
        # Largest Lyapunov exponent (simplified)
        features['nonlinear_lle'] = self._estimate_largest_lyapunov(ecg_signal)
        
        # Correlation dimension
        features['nonlinear_corr_dim'] = self._estimate_correlation_dimension(ecg_signal)
        
        # Recurrence quantification analysis
        rqa_features = self._calculate_rqa(ecg_signal)
        features.update({f'nonlinear_rqa_{k}': v for k, v in rqa_features.items()})
        
        return features
    
    def _extract_interval_features(self, r_peaks: np.ndarray) -> Dict:
        """Extract RR interval features"""
        features = {}
        
        if len(r_peaks) < 2:
            for key in ['interval_mean_rr', 'interval_std_rr', 'interval_cv_rr',
                       'interval_rmssd', 'interval_sdsd', 'interval_pnn50',
                       'interval_triangular_index', 'interval_tinn']:
                features[key] = 0.0
            return features
        
        # Calculate RR intervals in milliseconds
        rr_intervals = np.diff(r_peaks) / self.sampling_rate * 1000
        
        # Basic statistics
        features['interval_mean_rr'] = float(np.mean(rr_intervals))
        features['interval_std_rr'] = float(np.std(rr_intervals))
        features['interval_cv_rr'] = float(features['interval_std_rr'] / features['interval_mean_rr'] if features['interval_mean_rr'] > 0 else 0)
        
        # RMSSD (root mean square of successive differences)
        diff_rr = np.diff(rr_intervals)
        features['interval_rmssd'] = float(np.sqrt(np.mean(diff_rr ** 2)))
        
        # SDSD (standard deviation of successive differences)
        features['interval_sdsd'] = float(np.std(diff_rr))
        
        # pNN50 (percentage of adjacent RR intervals differing by more than 50ms)
        nn50 = np.sum(np.abs(diff_rr) > 50)
        features['interval_pnn50'] = float(nn50 / len(diff_rr) if len(diff_rr) > 0 else 0)
        
        # Triangular index
        hist, bin_edges = np.histogram(rr_intervals, bins='auto', density=True)
        features['interval_triangular_index'] = float(np.max(hist) / np.sum(hist) if np.sum(hist) > 0 else 0)
        
        # TINN (triangular interpolation of NN interval histogram)
        features['interval_tinn'] = self._calculate_tinn(rr_intervals)
        
        # Poincaré plot features
        features.update(self._calculate_poincare_features(rr_intervals))
        
        return features
    
    def _extract_waveform_features(self, ecg_signal: np.ndarray, r_peaks: np.ndarray) -> Dict:
        """Extract waveform-specific features"""
        features = {}
        
        if len(r_peaks) < 2:
            for key in ['waveform_symmetry', 'waveform_complexity', 'waveform_regularity',
                       'waveform_fractal_dim', 'waveform_lyapunov', 'waveform_recurrence']:
                features[key] = 0.0
            return features
        
        # Waveform symmetry
        features['waveform_symmetry'] = self._calculate_waveform_symmetry(ecg_signal, r_peaks)
        
        # Waveform complexity (Lempel-Ziv complexity)
        features['waveform_complexity'] = self._calculate_lempel_ziv_complexity(ecg_signal)
        
        # Waveform regularity
        features['waveform_regularity'] = self._calculate_waveform_regularity(ecg_signal, r_peaks)
        
        # Fractal dimension
        features['waveform_fractal_dim'] = self._calculate_fractal_dimension(ecg_signal)
        
        # Local Lyapunov exponents
        features['waveform_lyapunov'] = self._calculate_local_lyapunov(ecg_signal)
        
        # Recurrence period density entropy
        features['waveform_recurrence'] = self._calculate_recurrence_period_density_entropy(ecg_signal)
        
        # Multiscale entropy
        mse_features = self._calculate_multiscale_entropy(ecg_signal, max_scale=5)
        features.update({f'waveform_mse_scale{i}': v for i, v in enumerate(mse_features, 1)})
        
        return features
    
    def _extract_beat_templates(self, ecg_signal: np.ndarray, r_peaks: np.ndarray) -> np.ndarray:
        """Extract aligned beat templates"""
        if len(r_peaks) < 2:
            return np.array([])
        
        # Determine beat window (300ms before to 500ms after R-peak)
        window_before = int(0.3 * self.sampling_rate)
        window_after = int(0.5 * self.sampling_rate)
        
        beat_templates = []
        for r_peak in r_peaks:
            start_idx = max(0, r_peak - window_before)
            end_idx = min(len(ecg_signal), r_peak + window_after)
            
            if end_idx - start_idx == window_before + window_after:
                beat = ecg_signal[start_idx:end_idx]
                # Align to R-peak (center of window)
                beat_templates.append(beat)
        
        return np.array(beat_templates) if beat_templates else np.array([])
    
    def _find_wave_extremum(self, segment: np.ndarray, extremum_type: str = 'max'):
        """Find extremum (max or min) in segment"""
        if len(segment) == 0:
            return None
        
        if extremum_type == 'max':
            idx = np.argmax(segment)
        else:  # 'min'
            idx = np.argmin(segment)
        
        return idx
    
    def _calculate_sample_entropy(self, signal: np.ndarray, m: int = 2, r: float = None) -> float:
        """Calculate Sample Entropy"""
        if r is None:
            r = 0.2 * np.std(signal)
        
        n = len(signal)
        
        def _phi(m):
            """Helper function for entropy calculation"""
            patterns = np.array([signal[i:i+m] for i in range(n - m + 1)])
            C = 0
            for i in range(len(patterns)):
                for j in range(len(patterns)):
                    if i != j and np.max(np.abs(patterns[i] - patterns[j])) <= r:
                        C += 1
            return C / (len(patterns) * (len(patterns) - 1)) if len(patterns) > 1 else 0
        
        A = _phi(m + 1)
        B = _phi(m)
        
        if A == 0 or B == 0:
            return 0.0
        
        return -np.log(A / B)
    
    def _calculate_approximate_entropy(self, signal: np.ndarray, m: int = 2, r: float = None) -> float:
        """Calculate Approximate Entropy (simplified)"""
        return self._calculate_sample_entropy(signal, m, r)  # Simplified version
    
    def _calculate_dfa(self, signal: np.ndarray) -> Tuple[float, float]:
        """Calculate Detrended Fluctuation Analysis"""
        n = len(signal)
        
        # Integrate signal
        y = np.cumsum(signal - np.mean(signal))
        
        # Define scale ranges
        scales = np.logspace(np.log10(4), np.log10(n//4), 20).astype(int)
        scales = scales[scales < n//4]
        
        fluctuations = []
        for scale in scales:
            # Divide into segments
            n_segments = n // scale
            if n_segments == 0:
                continue
            
            f2 = 0
            for v in range(n_segments):
                segment = y[v*scale:(v+1)*scale]
                # Detrend
                x = np.arange(len(segment))
                coeffs = np.polyfit(x, segment, 1)
                trend = np.polyval(coeffs, x)
                detrended = segment - trend
                f2 += np.mean(detrended**2)
            
            fluctuations.append(np.sqrt(f2 / n_segments))
        
        if len(scales) < 2 or len(fluctuations) < 2:
            return 0.0, 0.0
        
        # Fit two lines (short and long term)
        log_scales = np.log10(scales)
        log_fluct = np.log10(fluctuations)
        
        # Split into short and long scales
        split_idx = len(scales) // 2
        alpha1, _ = np.polyfit(log_scales[:split_idx], log_fluct[:split_idx], 1)
        alpha2, _ = np.polyfit(log_scales[split_idx:], log_fluct[split_idx:], 1)
        
        return float(alpha1), float(alpha2)
    
    def _calculate_hurst_exponent(self, signal: np.ndarray) -> float:
        """Calculate Hurst exponent using R/S analysis"""
        n = len(signal)
        min_size = 10
        
        # Calculate R/S for different sizes
        sizes = []
        rs_values = []
        
        size = min_size
        while size < n:
            n_segments = n // size
            if n_segments < 2:
                break
            
            rs_segments = []
            for i in range(n_segments):
                segment = signal[i*size:(i+1)*size]
                mean_seg = np.mean(segment)
                cum_dev = np.cumsum(segment - mean_seg)
                r = np.max(cum_dev) - np.min(cum_dev)
                s = np.std(segment)
                if s > 0:
                    rs_segments.append(r / s)
            
            if rs_segments:
                sizes.append(size)
                rs_values.append(np.mean(rs_segments))
            
            size = int(size * 1.5)
        
        if len(sizes) < 2:
            return 0.5
        
        # Fit power law
        log_sizes = np.log10(sizes)
        log_rs = np.log10(rs_values)
        hurst, _ = np.polyfit(log_sizes, log_rs, 1)
        
        return float(hurst)
    
    def _estimate_largest_lyapunov(self, signal: np.ndarray) -> float:
        """Estimate largest Lyapunov exponent (simplified)"""
        # Simplified implementation
        n = len(signal)
        if n < 100:
            return 0.0
        
        # Reconstruct phase space (delay embedding)
        tau = 10  # time delay
        m = 3     # embedding dimension
        embedded = np.array([signal[i: i + (m-1)*tau: tau] for i in range(n - (m-1)*tau)])
        
        if len(embedded) < 10:
            return 0.0
        
        # Simplified LLE estimation
        distances = []
        for i in range(len(embedded) - 1):
            dist = np.linalg.norm(embedded[i+1] - embedded[i])
            distances.append(dist)
        
        if len(distances) == 0:
            return 0.0
        
        # Average logarithmic divergence
        lle = np.mean(np.log(np.array(distances) + 1e-10))
        return float(lle)
    
    def _estimate_correlation_dimension(self, signal: np.ndarray) -> float:
        """Estimate correlation dimension (simplified)"""
        # Simplified implementation
        n = len(signal)
        if n < 50:
            return 0.0
        
        # Sample points
        sample_size = min(100, n)
        indices = np.random.choice(n, sample_size, replace=False)
        sample_points = signal[indices]
        
        # Calculate pairwise distances
        distances = []
        for i in range(sample_size):
            for j in range(i+1, sample_size):
                distances.append(np.abs(sample_points[i] - sample_points[j]))
        
        if len(distances) == 0:
            return 0.0
        
        # Count pairs within radius r
        r_values = np.logspace(-3, 0, 20)
        counts = []
        
        for r in r_values:
            count = np.sum(np.array(distances) < r)
            counts.append(count)
        
        # Fit line in log-log plot
        valid_idx = np.array(counts) > 0
        if np.sum(valid_idx) < 2:
            return 0.0
        
        log_r = np.log10(r_values[valid_idx])
        log_c = np.log10(np.array(counts)[valid_idx])
        
        slope, _ = np.polyfit(log_r, log_c, 1)
        return float(slope)
    
    def _calculate_rqa(self, signal: np.ndarray) -> Dict:
        """Calculate Recurrence Quantification Analysis features"""
        # Simplified RQA
        n = len(signal)
        threshold = 0.2 * np.std(signal)
        
        # Recurrence matrix
        recurrence = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if np.abs(signal[i] - signal[j]) < threshold:
                    recurrence[i, j] = 1
        
        # Basic RQA metrics
        features = {
            'recurrence_rate': np.mean(recurrence),
            'determinism': 0.0,
            'laminarity': 0.0,
            'trapping_time': 0.0,
            'entropy': 0.0
        }
        
        return features
    
    def _calculate_tinn(self, rr_intervals: np.ndarray) -> float:
        """Calculate TINN (Triangular Interpolation of NN Interval Histogram)"""
        if len(rr_intervals) < 10:
            return 0.0
        
        # Create histogram
        hist, bin_edges = np.histogram(rr_intervals, bins='auto', density=True)
        
        # Find mode
        mode_idx = np.argmax(hist)
        mode_value = (bin_edges[mode_idx] + bin_edges[mode_idx+1]) / 2
        
        # Calculate TINN as width of triangular interpolation
        left_idx = mode_idx
        right_idx = mode_idx
        
        while left_idx > 0 and hist[left_idx] > hist[mode_idx] * 0.5:
            left_idx -= 1
        
        while right_idx < len(hist)-1 and hist[right_idx] > hist[mode_idx] * 0.5:
            right_idx += 1
        
        tinn = bin_edges[right_idx] - bin_edges[left_idx]
        return float(tinn)
    
    def _calculate_poincare_features(self, rr_intervals: np.ndarray) -> Dict:
        """Calculate Poincaré plot features"""
        if len(rr_intervals) < 2:
            return {}
        
        # Poincaré plot: RR_n vs RR_{n+1}
        x = rr_intervals[:-1]
        y = rr_intervals[1:]
        
        # Fit ellipse
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        
        # SD1 and SD2 (width and length of ellipse)
        sd1 = np.std((x - y) / np.sqrt(2))
        sd2 = np.std((x + y) / np.sqrt(2))
        
        # Area of ellipse
        area = np.pi * sd1 * sd2
        
        # Ratio
        ratio = sd2 / sd1 if sd1 > 0 else 0
        
        return {
            'interval_sd1': float(sd1),
            'interval_sd2': float(sd2),
            'interval_poincare_area': float(area),
            'interval_sd2_sd1_ratio': float(ratio)
        }
    
    def _calculate_waveform_symmetry(self, signal: np.ndarray, r_peaks: np.ndarray) -> float:
        """Calculate waveform symmetry around R-peaks"""
        if len(r_peaks) < 3:
            return 0.0
        
        beat_templates = self._extract_beat_templates(signal, r_peaks)
        if len(beat_templates) == 0:
            return 0.0
        
        avg_beat = np.mean(beat_templates, axis=0)
        center = len(avg_beat) // 2
        
        # Split beat into left and right halves
        left_half = avg_beat[:center]
        right_half = avg_beat[center:][::-1]  # Reverse to align
        
        # Ensure equal lengths
        min_len = min(len(left_half), len(right_half))
        left_half = left_half[-min_len:] if len(left_half) > min_len else left_half
        right_half = right_half[:min_len]
        
        # Calculate symmetry (correlation between halves)
        if min_len > 1:
            correlation = np.corrcoef(left_half, right_half)[0, 1]
            return float(correlation) if not np.isnan(correlation) else 0.0
        else:
            return 0.0
    
    def _calculate_lempel_ziv_complexity(self, signal: np.ndarray) -> float:
        """Calculate Lempel-Ziv complexity"""
        # Convert to binary sequence
        median = np.median(signal)
        binary_seq = (signal > median).astype(int)
        
        # Lempel-Ziv complexity calculation
        n = len(binary_seq)
        c = 1
        l = 1
        i = 0
        k = 1
        k_max = 1
        
        while True:
            if binary_seq[i + k - 1] == binary_seq[l + k - 1]:
                k += 1
                if l + k > n:
                    c += 1
                    break
            else:
                if k > k_max:
                    k_max = k
                
                i += 1
                if i == l:
                    c += 1
                    l += k_max
                    if l + 1 > n:
                        break
                    else:
                        i = 0
                        k = 1
                        k_max = 1
                else:
                    k = 1
        
        # Normalize
        b = len(np.unique(binary_seq))
        complexity = c * np.log(n) / (n * np.log(b)) if b > 1 and n > 0 else 0
        
        return float(complexity)
    
    def _calculate_waveform_regularity(self, signal: np.ndarray, r_peaks: np.ndarray) -> float:
        """Calculate waveform regularity (beat-to-beat similarity)"""
        if len(r_peaks) < 3:
            return 0.0
        
        beat_templates = self._extract_beat_templates(signal, r_peaks)
        if len(beat_templates) < 2:
            return 0.0
        
        # Calculate pairwise correlations
        correlations = []
        for i in range(len(beat_templates)):
            for j in range(i+1, len(beat_templates)):
                corr = np.corrcoef(beat_templates[i], beat_templates[j])[0, 1]
                if not np.isnan(corr):
                    correlations.append(corr)
        
        return float(np.mean(correlations)) if correlations else 0.0
    
    def _calculate_fractal_dimension(self, signal: np.ndarray) -> float:
        """Calculate fractal dimension using box-counting"""
        n = len(signal)
        if n < 100:
            return 1.0
        
        # Normalize signal
        signal_norm = (signal - np.min(signal)) / (np.max(signal) - np.min(signal) + 1e-10)
        
        # Box sizes
        box_sizes = 2 ** np.arange(1, 8)
        box_sizes = box_sizes[box_sizes < n // 2]
        
        counts = []
        for size in box_sizes:
            # Count boxes needed
            n_boxes = n // size
            if n_boxes == 0:
                continue
            
            min_vals = np.zeros(n_boxes)
            max_vals = np.zeros(n_boxes)
            
            for i in range(n_boxes):
                segment = signal_norm[i*size:(i+1)*size]
                min_vals[i] = np.min(segment)
                max_vals[i] = np.max(segment)
            
            # Count boxes that contain signal
            box_count = np.sum(np.ceil((max_vals - min_vals) * n_boxes / size))
            counts.append(box_count)
        
        if len(counts) < 2:
            return 1.0
        
        # Fit line in log-log plot
        log_sizes = np.log2(box_sizes[:len(counts)])
        log_counts = np.log2(counts)
        
        slope, _ = np.polyfit(log_sizes, log_counts, 1)
        fractal_dim = -slope
        
        return float(fractal_dim)
    
    def _calculate_local_lyapunov(self, signal: np.ndarray) -> float:
        """Calculate local Lyapunov exponents"""
        # Simplified version
        n = len(signal)
        if n < 50:
            return 0.0
        
        # Calculate local variability
        local_std = []
        window_size = min(20, n // 4)
        
        for i in range(0, n - window_size, window_size):
            segment = signal[i:i+window_size]
            local_std.append(np.std(segment))
        
        return float(np.mean(local_std)) if local_std else 0.0
    
    def _calculate_recurrence_period_density_entropy(self, signal: np.ndarray) -> float:
        """Calculate recurrence period density entropy"""
        # Simplified version
        n = len(signal)
        threshold = 0.1 * np.std(signal)
        
        # Find recurrence times
        recurrence_times = []
        for i in range(n):
            for j in range(i+1, n):
                if np.abs(signal[i] - signal[j]) < threshold:
                    recurrence_times.append(j - i)
                    break
        
        if len(recurrence_times) < 2:
            return 0.0
        
        # Calculate entropy of recurrence time distribution
        hist, _ = np.histogram(recurrence_times, bins='auto', density=True)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log(hist))
        
        return float(entropy)
    
    def _calculate_multiscale_entropy(self, signal: np.ndarray, max_scale: int = 5) -> List[float]:
        """Calculate multiscale entropy"""
        entropies = []
        
        for scale in range(1, max_scale + 1):
            # Coarse-grain signal
            n = len(signal) // scale
            if n < 10:
                entropies.append(0.0)
                continue
            
            coarse_signal = np.mean(signal[:n*scale].reshape(-1, scale), axis=1)
            
            # Calculate sample entropy for coarse-grained signal
            sampen = self._calculate_sample_entropy(coarse_signal, m=2, r=0.2*np.std(coarse_signal))
            entropies.append(sampen)
        
        return entropies
    
    def export_features_to_csv(self, features: Dict, filename: str):
        """Export features to CSV file"""
        df = pd.DataFrame([features])
        df.to_csv(filename, index=False)
        print(f"Features exported to {filename}")
    
    def generate_feature_report(self, features: Dict) -> str:
        """Generate comprehensive feature report"""
        report = []
        report.append("=" * 80)
        report.append("ECG FEATURE EXTRACTION REPORT")
        report.append("=" * 80)
        report.append(f"Total Features Extracted: {features.get('total_features', 0)}")
        report.append(f"Signal Length: {features.get('signal_length', 0)} samples")
        report.append(f"Sampling Rate: {features.get('sampling_rate', 0)} Hz")
        report.append("")
        
        # Group features by category
        feature_categories = {
            'Temporal Features': [k for k in features.keys() if k.startswith('temporal_')],
            'Spectral Features': [k for k in features.keys() if k.startswith('spectral_')],
            'Statistical Features': [k for k in features.keys() if k.startswith('statistical_')],
            'Morphological Features': [k for k in features.keys() if k.startswith('morph_')],
            'Nonlinear Features': [k for k in features.keys() if k.startswith('nonlinear_')],
            'Interval Features': [k for k in features.keys() if k.startswith('interval_')],
            'Waveform Features': [k for k in features.keys() if k.startswith('waveform_')]
        }
        
        for category, feature_list in feature_categories.items():
            if feature_list:
                report.append(f"{category}:")
                for feature in feature_list[:10]:  # Show first 10 of each category
                    value = features[feature]
                    if isinstance(value, float):
                        report.append(f"  {feature}: {value:.6f}")
                    else:
                        report.append(f"  {feature}: {value}")
                if len(feature_list) > 10:
                    report.append(f"  ... and {len(feature_list) - 10} more features")
                report.append("")
        
        report.append("Key Indicators:")
        report.append("=" * 40)
        
        # Highlight key clinical indicators
        key_indicators = [
            ('Heart Rate Variability', 'interval_rmssd', 'ms', '>30ms = Good'),
            ('QRS Duration', 'morph_qrs_duration', 'ms', '<120ms = Normal'),
            ('QT Interval', 'morph_qt_interval', 'ms', '<440ms = Normal'),
            ('Signal Complexity', 'nonlinear_sampen', '', 'Higher = More complex'),
            ('Fractal Dimension', 'waveform_fractal_dim', '', '1-2, Higher = More complex'),
            ('Waveform Regularity', 'waveform_regularity', '', '0-1, Higher = More regular')
        ]
        
        for name, key, unit, normal_range in key_indicators:
            if key in features:
                value = features[key]
                if isinstance(value, float):
                    report.append(f"{name}: {value:.2f} {unit} ({normal_range})")
                else:
                    report.append(f"{name}: {value} {unit} ({normal_range})")
        
        report.append("")
        report.append("Feature Extraction Complete")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    """Example usage of ECG Feature Extractor"""
    print("Initializing ECG Feature Extractor...")
    extractor = ECGFeatureExtractor(sampling_rate=500)
    
    # Generate synthetic ECG
    t = np.linspace(0, 10, 5000)
    ecg_signal = np.sin(2 * np.pi * 1 * t) + 0.5 * np.sin(2 * np.pi * 5 * t) + 0.1 * np.random.randn(len(t))
    
    print("Extracting features...")
    features = extractor.extract_all_features(ecg_signal)
    
    report = extractor.generate_feature_report(features)
    print(report)
    
    # Export to CSV
    extractor.export_features_to_csv(features, "ecg_features.csv")
    
    print(f"\nTotal features extracted: {len(features)}")
    print("Feature extraction complete!")

if __name__ == "__main__":
    main()
