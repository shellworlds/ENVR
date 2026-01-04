"""
ECG Data Augmentation System
Advanced data augmentation techniques for ECG machine learning
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

class ECGDataAugmentation:
    """Advanced ECG data augmentation for ML training"""
    
    def __init__(self, sampling_rate: int = 500):
        self.sampling_rate = sampling_rate
        self.augmentation_methods = {
            'noise_injection': self.add_noise,
            'time_warping': self.time_warp,
            'amplitude_scaling': self.amplitude_scale,
            'time_shift': self.time_shift,
            'frequency_warping': self.frequency_warp,
            'baseline_wander': self.add_baseline_wander,
            'powerline_noise': self.add_powerline_noise,
            'electrode_motion': self.add_electrode_motion,
            'muscle_artifact': self.add_muscle_artifact,
            'signal_dropout': self.add_signal_dropout,
            'beat_perturbation': self.perturb_beats,
            'lead_mixing': self.mix_leads,
            'st_segment_shift': self.shift_st_segment,
            't_wave_alteration': self.alter_t_wave
        }
    
    def augment_signal(self, ecg_signal: np.ndarray, 
                      methods: List[str] = None,
                      intensity: float = 0.5) -> np.ndarray:
        """Apply multiple augmentation methods"""
        if methods is None:
            methods = ['noise_injection', 'time_warping', 'amplitude_scaling']
        
        augmented = ecg_signal.copy()
        
        for method in methods:
            if method in self.augmentation_methods:
                augmented = self.augmentation_methods[method](
                    augmented, intensity=intensity
                )
        
        return augmented
    
    def add_noise(self, ecg_signal: np.ndarray, 
                 noise_type: str = 'gaussian',
                 intensity: float = 0.5) -> np.ndarray:
        """Add various types of noise to ECG signal"""
        signal_power = np.mean(ecg_signal ** 2)
        
        if noise_type == 'gaussian':
            # Gaussian white noise
            noise_level = intensity * 0.1 * np.sqrt(signal_power)
            noise = noise_level * np.random.randn(len(ecg_signal))
            
        elif noise_type == 'colored':
            # Colored noise (1/f spectrum)
            fft = np.fft.fft(ecg_signal)
            frequencies = np.fft.fftfreq(len(ecg_signal))
            colored_filter = 1 / (1 + np.abs(frequencies))
            colored_filter[0] = 0  # Remove DC
            
            noise_fft = np.fft.fft(np.random.randn(len(ecg_signal)))
            colored_noise_fft = noise_fft * colored_filter
            colored_noise = np.real(np.fft.ifft(colored_noise_fft))
            
            # Scale to desired intensity
            noise_power = np.mean(colored_noise ** 2)
            scale = intensity * 0.2 * np.sqrt(signal_power / (noise_power + 1e-10))
            noise = colored_noise * scale
            
        elif noise_type == 'impulse':
            # Impulse noise (spikes)
            noise = np.zeros_like(ecg_signal)
            n_spikes = int(intensity * 10)  # Up to 10 spikes
            spike_indices = np.random.choice(len(ecg_signal), n_spikes, replace=False)
            
            for idx in spike_indices:
                spike_amplitude = intensity * 2.0 * np.std(ecg_signal)
                spike_width = int(0.01 * self.sampling_rate)  # 10ms spikes
                start = max(0, idx - spike_width // 2)
                end = min(len(ecg_signal), idx + spike_width // 2)
                noise[start:end] += spike_amplitude * np.hanning(end - start)
        
        else:
            noise = np.zeros_like(ecg_signal)
        
        return ecg_signal + noise
    
    def time_warp(self, ecg_signal: np.ndarray,
                 intensity: float = 0.5) -> np.ndarray:
        """Apply time warping to ECG signal"""
        n_samples = len(ecg_signal)
        
        # Create warping function
        x = np.linspace(0, 1, n_samples)
        
        # Random smooth warping
        n_knots = 3 + int(intensity * 5)  # 3 to 8 knots
        knot_positions = np.sort(np.random.rand(n_knots))
        knot_values = np.random.randn(n_knots) * intensity * 0.3
        
        # Interpolate to create warping function
        from scipy import interpolate
        tck = interpolate.splrep(knot_positions, knot_values, s=0)
        warp = interpolate.splev(x, tck, der=0)
        
        # Apply warping
        warped_indices = np.clip(x + warp, 0, 1) * (n_samples - 1)
        
        # Interpolate to get warped signal
        from scipy import interpolate as interp
        interpolator = interp.interp1d(np.arange(n_samples), ecg_signal, 
                                      kind='cubic', fill_value='extrapolate')
        warped_signal = interpolator(warped_indices)
        
        return warped_signal
    
    def amplitude_scale(self, ecg_signal: np.ndarray,
                       intensity: float = 0.5) -> np.ndarray:
        """Scale signal amplitude with variations"""
        # Global scaling
        global_scale = 1.0 + (np.random.rand() - 0.5) * intensity * 0.5
        
        # Time-varying scaling
        n_samples = len(ecg_signal)
        time_points = np.linspace(0, 1, 5)  # 5 control points
        scale_values = 1.0 + (np.random.randn(5) * intensity * 0.3)
        
        # Interpolate scale function
        from scipy import interpolate
        tck = interpolate.splrep(time_points, scale_values, s=0)
        x = np.linspace(0, 1, n_samples)
        time_varying_scale = interpolate.splev(x, tck, der=0)
        
        # Combine global and time-varying scaling
        total_scale = global_scale * time_varying_scale
        
        return ecg_signal * total_scale
    
    def time_shift(self, ecg_signal: np.ndarray,
                  intensity: float = 0.5) -> np.ndarray:
        """Apply time shifting (circular shift)"""
        max_shift = int(intensity * 0.2 * len(ecg_signal))  # Up to 20% shift
        shift_amount = np.random.randint(-max_shift, max_shift)
        
        return np.roll(ecg_signal, shift_amount)
    
    def frequency_warp(self, ecg_signal: np.ndarray,
                      intensity: float = 0.5) -> np.ndarray:
        """Warp frequency content of signal"""
        from scipy import fftpack
        
        # Compute FFT
        fft_signal = fftpack.fft(ecg_signal)
        frequencies = fftpack.fftfreq(len(ecg_signal))
        
        # Create frequency warping function
        # Compress/expand frequency axis
        warp_factor = 1.0 + (np.random.rand() - 0.5) * intensity * 0.5
        
        # Warp frequencies
        warped_frequencies = frequencies * warp_factor
        
        # Interpolate FFT to warped frequencies
        from scipy import interpolate
        # Only warp positive frequencies
        pos_idx = frequencies >= 0
        pos_freq = frequencies[pos_idx]
        pos_fft = fft_signal[pos_idx]
        
        # Create interpolation function
        interpolator = interpolate.interp1d(
            pos_freq, 
            pos_fft, 
            kind='cubic',
            fill_value=0.0,
            bounds_error=False
        )
        
        # Get warped FFT
        warped_pos_fft = interpolator(pos_freq * warp_factor)
        
        # Reconstruct full spectrum (maintaining symmetry)
        warped_fft = np.zeros_like(fft_signal, dtype=complex)
        warped_fft[pos_idx] = warped_pos_fft
        warped_fft[~pos_idx] = np.conj(warped_pos_fft[::-1])
        
        # Inverse FFT
        warped_signal = np.real(fftpack.ifft(warped_fft))
        
        return warped_signal
    
    def add_baseline_wander(self, ecg_signal: np.ndarray,
                           intensity: float = 0.5) -> np.ndarray:
        """Add realistic baseline wander"""
        n_samples = len(ecg_signal)
        t = np.arange(n_samples) / self.sampling_rate
        
        # Respiratory-induced baseline wander (0.1-0.5 Hz)
        resp_freq = 0.2 + np.random.rand() * 0.3  # 0.2-0.5 Hz
        resp_amplitude = intensity * 0.3 * np.std(ecg_signal)
        baseline = resp_amplitude * np.sin(2 * np.pi * resp_freq * t)
        
        # Add slower drift (0.01-0.1 Hz)
        drift_freq = 0.05 + np.random.rand() * 0.05  # 0.05-0.1 Hz
        drift_amplitude = intensity * 0.15 * np.std(ecg_signal)
        baseline += drift_amplitude * np.sin(2 * np.pi * drift_freq * t + np.random.rand() * 2 * np.pi)
        
        # Add random low-frequency components
        for _ in range(3):
            freq = 0.01 + np.random.rand() * 0.09  # 0.01-0.1 Hz
            amp = intensity * 0.1 * np.random.rand() * np.std(ecg_signal)
            phase = np.random.rand() * 2 * np.pi
            baseline += amp * np.sin(2 * np.pi * freq * t + phase)
        
        return ecg_signal + baseline
    
    def add_powerline_noise(self, ecg_signal: np.ndarray,
                           intensity: float = 0.5) -> np.ndarray:
        """Add powerline interference (50/60 Hz)"""
        n_samples = len(ecg_signal)
        t = np.arange(n_samples) / self.sampling_rate
        
        # Main powerline frequency (50 or 60 Hz)
        powerline_freq = 50.0 if np.random.rand() > 0.5 else 60.0
        
        # Fundamental frequency
        amplitude = intensity * 0.1 * np.std(ecg_signal)
        phase = np.random.rand() * 2 * np.pi
        powerline = amplitude * np.sin(2 * np.pi * powerline_freq * t + phase)
        
        # Harmonics
        for harmonic in [2, 3]:  # 2nd and 3rd harmonics
            if powerline_freq * harmonic < self.sampling_rate / 2:
                harmonic_amp = amplitude * (0.3 / harmonic)
                harmonic_phase = np.random.rand() * 2 * np.pi
                powerline += harmonic_amp * np.sin(
                    2 * np.pi * powerline_freq * harmonic * t + harmonic_phase
                )
        
        # Add frequency drift (simulating unstable power grid)
        freq_drift = 0.1 * np.random.randn()  # Small frequency variation
        powerline *= (1 + 0.01 * np.sin(2 * np.pi * 0.5 * t))  # Amplitude modulation
        
        return ecg_signal + powerline
    
    def add_electrode_motion(self, ecg_signal: np.ndarray,
                            intensity: float = 0.5) -> np.ndarray:
        """Add electrode motion artifact"""
        n_samples = len(ecg_signal)
        
        # Create motion artifact as step changes + slow recovery
        artifact = np.zeros(n_samples)
        
        # Number of motion events
        n_events = int(1 + intensity * 4)  # 1-5 motion events
        
        for _ in range(n_events):
            # Random event timing
            event_start = np.random.randint(0, n_samples - int(0.1 * self.sampling_rate))
            event_duration = int((0.05 + np.random.rand() * 0.15) * self.sampling_rate)  # 50-200ms
            
            event_end = min(n_samples, event_start + event_duration)
            
            # Step change (sudden electrode movement)
            step_amplitude = intensity * 0.5 * np.std(ecg_signal) * np.random.randn()
            artifact[event_start:event_end] += step_amplitude
            
            # Exponential recovery after motion
            recovery_duration = event_duration * 2
            recovery_end = min(n_samples, event_end + recovery_duration)
            
            if recovery_end > event_end:
                recovery_samples = recovery_end - event_end
                recovery = step_amplitude * np.exp(-np.linspace(0, 5, recovery_samples))
                artifact[event_end:recovery_end] += recovery
        
        return ecg_signal + artifact
    
    def add_muscle_artifact(self, ecg_signal: np.ndarray,
                           intensity: float = 0.5) -> np.ndarray:
        """Add muscle (EMG) artifact"""
        n_samples = len(ecg_signal)
        
        # Generate EMG-like noise (high frequency, bursty)
        emg_noise = np.zeros(n_samples)
        
        # Number of EMG bursts
        n_bursts = int(3 + intensity * 7)  # 3-10 bursts
        
        for _ in range(n_bursts):
            # Random burst timing
            burst_start = np.random.randint(0, n_samples - int(0.2 * self.sampling_rate))
            burst_duration = int((0.02 + np.random.rand() * 0.08) * self.sampling_rate)  # 20-100ms
            
            burst_end = min(n_samples, burst_start + burst_duration)
            
            # Generate burst as band-limited noise (20-100 Hz)
            burst_samples = burst_end - burst_start
            burst_noise = np.random.randn(burst_samples)
            
            # Bandpass filter to EMG frequency range
            from scipy import signal
            nyquist = 0.5 * self.sampling_rate
            low = 20.0 / nyquist
            high = 100.0 / nyquist
            b, a = signal.butter(3, [low, high], btype='band')
            burst_noise = signal.filtfilt(b, a, burst_noise)
            
            # Scale amplitude
            burst_amplitude = intensity * 0.2 * np.std(ecg_signal)
            burst_noise *= burst_amplitude / (np.std(burst_noise) + 1e-10)
            
            # Apply Hanning window for smooth onset/offset
            window = np.hanning(burst_samples)
            burst_noise *= window
            
            emg_noise[burst_start:burst_end] += burst_noise
        
        return ecg_signal + emg_noise
    
    def add_signal_dropout(self, ecg_signal: np.ndarray,
                          intensity: float = 0.5) -> np.ndarray:
        """Add signal dropout (flatline segments)"""
        augmented = ecg_signal.copy()
        n_samples = len(ecg_signal)
        
        # Number of dropout events
        n_dropouts = int(intensity * 3)  # 0-3 dropout events
        
        for _ in range(n_dropouts):
            # Random dropout timing
            dropout_start = np.random.randint(0, n_samples - int(0.05 * self.sampling_rate))
            dropout_duration = int((0.01 + np.random.rand() * 0.04) * self.sampling_rate)  # 10-50ms
            
            dropout_end = min(n_samples, dropout_start + dropout_duration)
            
            # Create dropout (flatline at mean value)
            segment_mean = np.mean(augmented[dropout_start:dropout_end])
            augmented[dropout_start:dropout_end] = segment_mean
            
            # Add small transition slopes at edges
            transition_width = min(10, dropout_duration // 4)
            
            # Start transition
            if dropout_start > transition_width:
                for i in range(transition_width):
                    alpha = i / transition_width
                    idx = dropout_start - transition_width + i
                    augmented[idx] = alpha * augmented[idx] + (1 - alpha) * segment_mean
            
            # End transition
            if dropout_end + transition_width < n_samples:
                for i in range(transition_width):
                    alpha = (i + 1) / transition_width
                    idx = dropout_end + i
                    augmented[idx] = alpha * augmented[idx] + (1 - alpha) * segment_mean
        
        return augmented
    
    def perturb_beats(self, ecg_signal: np.ndarray,
                     intensity: float = 0.5) -> np.ndarray:
        """Perturb individual heart beats"""
        from scipy import signal
        
        # Detect R-peaks (simplified)
        diff_signal = np.diff(ecg_signal)
        squared = diff_signal ** 2
        
        # Moving window integration
        window_size = int(0.15 * self.sampling_rate)
        integrated = np.convolve(squared, np.ones(window_size)/window_size, mode='same')
        
        # Find peaks
        threshold = 0.5 * np.max(integrated)
        peaks, _ = signal.find_peaks(integrated, height=threshold, 
                                    distance=int(0.3 * self.sampling_rate))
        
        augmented = ecg_signal.copy()
        
        if len(peaks) < 2:
            return augmented
        
        # Perturb each beat with some probability
        perturb_probability = intensity * 0.7
        
        for peak in peaks:
            if np.random.rand() < perturb_probability:
                # Beat window (250ms before to 400ms after R-peak)
                window_before = int(0.25 * self.sampling_rate)
                window_after = int(0.4 * self.sampling_rate)
                
                beat_start = max(0, peak - window_before)
                beat_end = min(len(ecg_signal), peak + window_after)
                
                if beat_end - beat_start < window_before + window_after:
                    continue
                
                # Extract beat
                beat = augmented[beat_start:beat_end].copy()
                
                # Apply random perturbation
                perturbation_type = np.random.choice(['scale', 'shift', 'morph'])
                
                if perturbation_type == 'scale':
                    # Scale QRS complex
                    qrs_start = window_before - int(0.05 * self.sampling_rate)
                    qrs_end = window_before + int(0.05 * self.sampling_rate)
                    scale_factor = 1.0 + (np.random.rand() - 0.5) * intensity * 0.8
                    beat[qrs_start:qrs_end] *= scale_factor
                
                elif perturbation_type == 'shift':
                    # Time shift within beat
                    shift_amount = int((np.random.rand() - 0.5) * intensity * 0.1 * len(beat))
                    beat_shifted = np.roll(beat, shift_amount)
                    
                    # Handle edges
                    if shift_amount > 0:
                        beat_shifted[:shift_amount] = beat[0]
                    elif shift_amount < 0:
                        beat_shifted[shift_amount:] = beat[-1]
                    
                    beat = beat_shifted
                
                elif perturbation_type == 'morph':
                    # Morphological change (add small wavelets)
                    n_wavelets = 1 + int(np.random.rand() * 2)
                    for _ in range(n_wavelets):
                        wavelet_pos = np.random.randint(0, len(beat))
                        wavelet_width = int(0.02 * self.sampling_rate + np.random.rand() * 0.03 * self.sampling_rate)
                        wavelet_amp = intensity * 0.3 * np.std(beat) * np.random.randn()
                        
                        # Create Mexican hat wavelet
                        x = np.linspace(-3, 3, wavelet_width)
                        wavelet = wavelet_amp * (1 - x**2) * np.exp(-x**2 / 2)
                        
                        # Add wavelet to beat
                        w_start = max(0, wavelet_pos - wavelet_width // 2)
                        w_end = min(len(beat), wavelet_pos + wavelet_width // 2)
                        w_len = w_end - w_start
                        
                        if w_len > 0:
                            beat[w_start:w_end] += wavelet[:w_len]
                
                # Update augmented signal
                augmented[beat_start:beat_end] = beat
        
        return augmented
    
    def mix_leads(self, ecg_signal: np.ndarray,
                 intensity: float = 0.5) -> np.ndarray:
        """Simulate lead mixing/cross-talk"""
        # Create artificial second lead
        n_samples = len(ecg_signal)
        
        # Generate correlated signal (simulating another lead)
        from scipy import signal
        
        # Low-pass filter to get smoothed version
        nyquist = 0.5 * self.sampling_rate
        low = 40.0 / nyquist
        b, a = signal.butter(3, low, btype='low')
        smoothed = signal.filtfilt(b, a, ecg_signal)
        
        # Add phase shift
        phase_shift = int((np.random.rand() - 0.5) * intensity * 0.01 * self.sampling_rate)
        lead2 = np.roll(smoothed, phase_shift)
        
        # Scale differently
        scale2 = 0.3 + np.random.rand() * 0.4  # 0.3-0.7
        lead2 *= scale2
        
        # Add some independent noise
        noise = np.random.randn(n_samples) * 0.1 * np.std(ecg_signal)
        lead2 += noise
        
        # Mix leads
        mix_ratio = 0.7 + (np.random.rand() - 0.5) * intensity * 0.4  # 0.5-0.9
        mixed = mix_ratio * ecg_signal + (1 - mix_ratio) * lead2
        
        return mixed
    
    def shift_st_segment(self, ecg_signal: np.ndarray,
                        intensity: float = 0.5) -> np.ndarray:
        """Apply ST segment elevation/depression"""
        from scipy import signal
        
        # Detect R-peaks
        diff_signal = np.diff(ecg_signal)
        squared = diff_signal ** 2
        window_size = int(0.15 * self.sampling_rate)
        integrated = np.convolve(squared, np.ones(window_size)/window_size, mode='same')
        threshold = 0.5 * np.max(integrated)
        peaks, _ = signal.find_peaks(integrated, height=threshold, 
                                    distance=int(0.3 * self.sampling_rate))
        
        augmented = ecg_signal.copy()
        
        if len(peaks) < 2:
            return augmented
        
        # Apply ST shift to each beat
        for peak in peaks:
            if np.random.rand() < intensity * 0.5:
                # ST segment region (80-120ms after R-peak)
                st_start = peak + int(0.08 * self.sampling_rate)
                st_end = peak + int(0.12 * self.sampling_rate)
                
                # Ensure within bounds
                st_start = max(0, min(st_start, len(ecg_signal)))
                st_end = max(0, min(st_end, len(ecg_signal)))
                
                if st_end > st_start:
                    # Random ST shift (depression or elevation)
                    st_shift = (np.random.rand() - 0.5) * intensity * 0.5 * np.std(ecg_signal)
                    
                    # Apply smooth transition
                    st_length = st_end - st_start
                    transition = np.linspace(0, 1, st_length)
                    
                    # Add to ST segment
                    augmented[st_start:st_end] += st_shift * transition
        
        return augmented
    
    def alter_t_wave(self, ecg_signal: np.ndarray,
                    intensity: float = 0.5) -> np.ndarray:
        """Alter T-wave morphology"""
        from scipy import signal
        
        # Detect R-peaks
        diff_signal = np.diff(ecg_signal)
        squared = diff_signal ** 2
        window_size = int(0.15 * self.sampling_rate)
        integrated = np.convolve(squared, np.ones(window_size)/window_size, mode='same')
        threshold = 0.5 * np.max(integrated)
        peaks, _ = signal.find_peaks(integrated, height=threshold, 
                                    distance=int(0.3 * self.sampling_rate))
        
        augmented = ecg_signal.copy()
        
        if len(peaks) < 2:
            return augmented
        
        # Alter T-wave for each beat
        for peak in peaks:
            if np.random.rand() < intensity * 0.4:
                # T-wave region (200-400ms after R-peak)
                t_start = peak + int(0.2 * self.sampling_rate)
                t_end = peak + int(0.4 * self.sampling_rate)
                
                # Ensure within bounds
                t_start = max(0, min(t_start, len(ecg_signal)))
                t_end = max(0, min(t_end, len(ecg_signal)))
                
                if t_end > t_start:
                    t_length = t_end - t_start
                    
                    # Random T-wave alteration
                    alteration_type = np.random.choice(['invert', 'flatten', 'peaked'])
                    
                    if alteration_type == 'invert':
                        # T-wave inversion
                        t_wave = augmented[t_start:t_end]
                        inverted = -t_wave * (0.5 + np.random.rand() * 0.5)
                        augmented[t_start:t_end] = inverted
                    
                    elif alteration_type == 'flatten':
                        # Flatten T-wave
                        t_wave = augmented[t_start:t_end]
                        flattened = t_wave * (0.2 + np.random.rand() * 0.3)
                        augmented[t_start:t_end] = flattened
                    
                    elif alteration_type == 'peaked':
                        # Make T-wave more peaked
                        t_wave = augmented[t_start:t_end]
                        center = t_length // 2
                        x = np.linspace(-3, 3, t_length)
                        peak_enhancement = np.exp(-x**2 / (2 * (0.5 + np.random.rand())))
                        peak_enhancement = peak_enhancement / np.max(peak_enhancement)
                        peaked = t_wave * (1 + intensity * peak_enhancement)
                        augmented[t_start:t_end] = peaked
        
        return augmented
    
    def generate_augmented_dataset(self, original_signals: List[np.ndarray],
                                  n_augmented_per_signal: int = 5,
                                  augmentation_intensity: float = 0.5) -> List[np.ndarray]:
        """Generate augmented dataset from original signals"""
        augmented_dataset = []
        
        for signal in original_signals:
            # Keep original
            augmented_dataset.append(signal)
            
            # Generate augmented versions
            for i in range(n_augmented_per_signal):
                # Randomly select augmentation methods
                n_methods = np.random.randint(2, 5)
                methods = np.random.choice(
                    list(self.augmentation_methods.keys()),
                    size=n_methods,
                    replace=False
                )
                
                # Apply augmentations
                augmented = self.augment_signal(
                    signal,
                    methods=list(methods),
                    intensity=augmentation_intensity * (0.8 + np.random.rand() * 0.4)
                )
                
                augmented_dataset.append(augmented)
        
        return augmented_dataset
    
    def validate_augmentation(self, original_signal: np.ndarray,
                            augmented_signal: np.ndarray) -> Dict:
        """Validate that augmentation preserves key ECG characteristics"""
        metrics = {}
        
        # Basic statistics
        metrics['mean_difference'] = np.mean(augmented_signal) - np.mean(original_signal)
        metrics['std_difference'] = np.std(augmented_signal) - np.std(original_signal)
        
        # Correlation
        correlation = np.corrcoef(original_signal, augmented_signal)[0, 1]
        metrics['correlation'] = correlation
        
        # Frequency content similarity (using PSD)
        from scipy import signal
        f_orig, psd_orig = signal.welch(original_signal, fs=self.sampling_rate, nperseg=256)
        f_aug, psd_aug = signal.welch(augmented_signal, fs=self.sampling_rate, nperseg=256)
        
        # Interpolate to common frequencies
        from scipy import interpolate
        interp_psd_aug = interpolate.interp1d(f_aug, psd_aug, bounds_error=False, fill_value=0)
        psd_aug_interp = interp_psd_aug(f_orig)
        
        # Calculate spectral similarity
        valid_idx = (psd_orig > 0) & (psd_aug_interp > 0)
        if np.any(valid_idx):
            spectral_similarity = 1 - np.mean(
                np.abs(psd_orig[valid_idx] - psd_aug_interp[valid_idx]) / 
                (psd_orig[valid_idx] + psd_aug_interp[valid_idx])
            )
            metrics['spectral_similarity'] = spectral_similarity
        else:
            metrics['spectral_similarity'] = 0
        
        # Heart rate preservation (simplified)
        # Detect peaks in both signals
        diff_orig = np.diff(original_signal)
        squared_orig = diff_orig ** 2
        window_size = int(0.15 * self.sampling_rate)
        integrated_orig = np.convolve(squared_orig, np.ones(window_size)/window_size, mode='same')
        
        diff_aug = np.diff(augmented_signal)
        squared_aug = diff_aug ** 2
        integrated_aug = np.convolve(squared_aug, np.ones(window_size)/window_size, mode='same')
        
        # Simple peak count
        threshold_orig = 0.5 * np.max(integrated_orig)
        threshold_aug = 0.5 * np.max(integrated_aug)
        
        peaks_orig = signal.find_peaks(integrated_orig, height=threshold_orig, 
                                      distance=int(0.3 * self.sampling_rate))[0]
        peaks_aug = signal.find_peaks(integrated_aug, height=threshold_aug, 
                                     distance=int(0.3 * self.sampling_rate))[0]
        
        if len(peaks_orig) > 0 and len(peaks_aug) > 0:
            hr_orig = len(peaks_orig) / (len(original_signal) / self.sampling_rate) * 60
            hr_aug = len(peaks_aug) / (len(augmented_signal) / self.sampling_rate) * 60
            metrics['heart_rate_difference'] = abs(hr_aug - hr_orig)
            metrics['heart_rate_preserved'] = abs(hr_aug - hr_orig) < 10  # Within 10 bpm
        else:
            metrics['heart_rate_difference'] = float('inf')
            metrics['heart_rate_preserved'] = False
        
        # Overall validity score
        validity_score = 0.0
        if abs(metrics['mean_difference']) < 0.2 * np.std(original_signal):
            validity_score += 0.25
        if correlation > 0.7:
            validity_score += 0.25
        if 'spectral_similarity' in metrics and metrics['spectral_similarity'] > 0.6:
            validity_score += 0.25
        if metrics.get('heart_rate_preserved', False):
            validity_score += 0.25
        
        metrics['validity_score'] = validity_score
        metrics['is_valid'] = validity_score > 0.7
        
        return metrics

def generate_sample_ecg(sampling_rate: int = 500, duration: float = 10.0) -> np.ndarray:
    """Generate sample ECG signal for testing"""
    n_samples = int(sampling_rate * duration)
    t = np.linspace(0, duration, n_samples)
    
    # Create realistic ECG
    ecg = (
        0.5 * np.sin(2 * np.pi * 1.0 * t) +  # P wave / T wave
        1.0 * np.sin(2 * np.pi * 5.0 * t) * np.exp(-((t % 1.0) - 0.3)**2 / 0.02) +  # QRS
        0.1 * np.sin(2 * np.pi * 0.2 * t) +  # Baseline wander
        0.05 * np.sin(2 * np.pi * 50 * t) +  # Powerline
        0.03 * np.random.randn(n_samples)     # Noise
    )
    
    return ecg

def main():
    """Demonstration of ECG Data Augmentation System"""
    print("Initializing ECG Data Augmentation System...")
    print("=" * 80)
    
    # Create augmentation system
    augmenter = ECGDataAugmentation(sampling_rate=500)
    
    # Generate sample ECG
    print("\n1. Generating sample ECG signal...")
    original_ecg = generate_sample_ecg(sampling_rate=500, duration=5.0)
    print(f"Original signal: {len(original_ecg)} samples")
    print(f"Duration: {len(original_ecg)/500:.1f} seconds")
    
    # Test individual augmentation methods
    print("\n2. Testing augmentation methods...")
    print("-" * 40)
    
    test_methods = [
        'noise_injection',
        'time_warping', 
        'amplitude_scaling',
        'baseline_wander',
        'powerline_noise',
        'muscle_artifact'
    ]
    
    augmented_signals = {}
    
    for method in test_methods:
        print(f"Applying {method}...")
        augmented = augmenter.augment_signal(
            original_ecg, 
            methods=[method],
            intensity=0.5
        )
        augmented_signals[method] = augmented
        
        # Validate augmentation
        validation = augmenter.validate_augmentation(original_ecg, augmented)
        print(f"  Validity: {validation['validity_score']:.2f}, "
              f"Correlation: {validation['correlation']:.2f}")
    
    # Test combined augmentations
    print("\n3. Testing combined augmentations...")
    combined = augmenter.augment_signal(
        original_ecg,
        methods=['noise_injection', 'time_warping', 'baseline_wander'],
        intensity=0.6
    )
    
    validation = augmenter.validate_augmentation(original_ecg, combined)
    print(f"Combined augmentation validity: {validation['validity_score']:.2f}")
    print(f"Correlation with original: {validation['correlation']:.2f}")
    
    # Generate augmented dataset
    print("\n4. Generating augmented dataset...")
    original_signals = [original_ecg, original_ecg * 0.8]  # Two sample signals
    augmented_dataset = augmenter.generate_augmented_dataset(
        original_signals,
        n_augmented_per_signal=3,
        augmentation_intensity=0.5
    )
    
    print(f"Original dataset size: {len(original_signals)}")
    print(f"Augmented dataset size: {len(augmented_dataset)}")
    print(f"Augmentation factor: {len(augmented_dataset)/len(original_signals):.1f}x")
    
    # Validate all augmented signals
    print("\n5. Validating augmented signals...")
    print("-" * 40)
    
    valid_count = 0
    total_count = 0
    
    for i, aug_signal in enumerate(augmented_dataset):
        if i < len(original_signals):
            continue  # Skip original signals
        
        original_idx = i % len(original_signals)
        validation = augmenter.validate_augmentation(
            original_signals[original_idx],
            aug_signal
        )
        
        total_count += 1
        if validation['is_valid']:
            valid_count += 1
    
    print(f"Valid augmentations: {valid_count}/{total_count} ({valid_count/total_count*100:.1f}%)")
    
    # Test all augmentation methods
    print("\n6. Testing all augmentation methods...")
    print("-" * 40)
    
    method_results = {}
    for method_name, method_func in augmenter.augmentation_methods.items():
        try:
            augmented = method_func(original_ecg.copy(), intensity=0.5)
            validation = augmenter.validate_augmentation(original_ecg, augmented)
            method_results[method_name] = validation['validity_score']
            
            print(f"{method_name:20s}: validity = {validation['validity_score']:.2f}")
        except Exception as e:
            print(f"{method_name:20s}: ERROR - {str(e)}")
            method_results[method_name] = 0.0
    
    # Summary
    print("\n" + "=" * 80)
    print("AUGMENTATION SYSTEM SUMMARY")
    print("=" * 80)
    print(f"Total augmentation methods: {len(augmenter.augmentation_methods)}")
    print(f"Best method: {max(method_results, key=method_results.get)} "
          f"({max(method_results.values()):.2f} validity)")
    print(f"Worst method: {min(method_results, key=method_results.get)} "
          f"({min(method_results.values()):.2f} validity)")
    print(f"Average validity: {np.mean(list(method_results.values())):.2f}")
    
    print("\nRecommended augmentation pipeline:")
    print("1. Baseline wander + Powerline noise (realistic artifacts)")
    print("2. Time warping + Amplitude scaling (geometric transforms)")
    print("3. Noise injection + Muscle artifact (noise addition)")
    print("4. Beat perturbation (physiological variations)")
    
    print("\n" + "=" * 80)
    print("DATA AUGMENTATION DEMONSTRATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
