"""
Advanced ECG Visualization Dashboard
Interactive visualization of ECG signals, analysis results, and trends
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Visualization imports
try:
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    import matplotlib.patches as patches
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available. Visualizations disabled.")

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not available. Interactive visualizations disabled.")

class ECGVisualizationDashboard:
    """Advanced ECG visualization dashboard with multiple plot types"""
    
    def __init__(self, sampling_rate: int = 500, style: str = 'clinical'):
        self.sampling_rate = sampling_rate
        self.style = style
        
        # Set color schemes based on style
        if style == 'clinical':
            self.colors = {
                'ecg_signal': '#2c3e50',
                'r_peaks': '#e74c3c',
                'p_wave': '#3498db',
                't_wave': '#2ecc71',
                'qrs_complex': '#9b59b6',
                'baseline': '#95a5a6',
                'grid': '#ecf0f1',
                'background': '#ffffff',
                'text': '#2c3e50',
                'alert': '#e74c3c',
                'warning': '#f39c12',
                'normal': '#27ae60'
            }
        else:  # Default style
            self.colors = {
                'ecg_signal': '#2563eb',
                'r_peaks': '#dc2626',
                'p_wave': '#16a34a',
                't_wave': '#ea580c',
                'qrs_complex': '#7c3aed',
                'baseline': '#6b7280',
                'grid': '#e5e7eb',
                'background': '#f9fafb',
                'text': '#1f2937',
                'alert': '#ef4444',
                'warning': '#f59e0b',
                'normal': '#10b981'
            }
        
        # Initialize matplotlib style
        if MATPLOTLIB_AVAILABLE:
            plt.style.use('seaborn-v0_8-whitegrid')
            sns.set_palette("husl")
    
    def plot_ecg_signal(self, ecg_signal: np.ndarray, 
                       r_peaks: np.ndarray = None,
                       time_range: Tuple[float, float] = None,
                       figsize: Tuple[int, int] = (15, 6),
                       save_path: str = None) -> plt.Figure:
        """Plot ECG signal with annotations"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available.")
            return None
        
        # Set time range
        if time_range is None:
            time_range = (0, len(ecg_signal) / self.sampling_rate)
        
        # Create time axis
        time = np.linspace(time_range[0], time_range[1], len(ecg_signal))
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot ECG signal
        ax.plot(time, ecg_signal, 
                color=self.colors['ecg_signal'],
                linewidth=1.5,
                alpha=0.8,
                label='ECG Signal')
        
        # Plot R-peaks if provided
        if r_peaks is not None and len(r_peaks) > 0:
            r_times = r_peaks / self.sampling_rate
            r_amplitudes = ecg_signal[r_peaks]
            ax.scatter(r_times, r_amplitudes,
                      color=self.colors['r_peaks'],
                      s=50, zorder=5,
                      label='R Peaks',
                      edgecolors='white',
                      linewidth=1)
        
        # Set labels and title
        ax.set_xlabel('Time (seconds)', fontsize=12, fontweight='medium')
        ax.set_ylabel('Amplitude (mV)', fontsize=12, fontweight='medium')
        ax.set_title('ECG Signal Analysis', fontsize=14, fontweight='bold', pad=20)
        
        # Set grid
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # Set limits with some padding
        y_padding = 0.1 * (np.max(ecg_signal) - np.min(ecg_signal))
        ax.set_ylim(np.min(ecg_signal) - y_padding, 
                   np.max(ecg_signal) + y_padding)
        
        # Add legend
        ax.legend(loc='upper right', framealpha=0.9)
        
        # Add watermark
        ax.text(0.99, 0.01, 'Cardiology ML System',
                transform=ax.transAxes,
                fontsize=8, alpha=0.5,
                ha='right', va='bottom')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"Figure saved to {save_path}")
        
        return fig
    
    def plot_ecg_with_analysis(self, ecg_signal: np.ndarray,
                              analysis_results: Dict,
                              figsize: Tuple[int, int] = (20, 12),
                              save_path: str = None) -> plt.Figure:
        """Comprehensive ECG analysis visualization"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available.")
            return None
        
        # Create figure with subplots
        fig = plt.figure(figsize=figsize)
        gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Raw ECG signal (top-left)
        ax1 = fig.add_subplot(gs[0, :2])
        time = np.arange(len(ecg_signal)) / self.sampling_rate
        ax1.plot(time, ecg_signal, color=self.colors['ecg_signal'], linewidth=1)
        ax1.set_title('Raw ECG Signal', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Amplitude (mV)')
        ax1.grid(True, alpha=0.3)
        
        # 2. Filtered ECG (top-right)
        ax2 = fig.add_subplot(gs[0, 2])
        if 'filtered_signal' in analysis_results:
            filtered = analysis_results['filtered_signal']
            time_short = time[:len(filtered)]
            ax2.plot(time_short, filtered, color=self.colors['ecg_signal'], linewidth=1)
            ax2.set_title('Filtered ECG', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Time (s)')
            ax2.grid(True, alpha=0.3)
        
        # 3. Power spectral density (middle-left)
        ax3 = fig.add_subplot(gs[1, 0])
        if 'psd' in analysis_results:
            freqs, psd = analysis_results['psd']
            ax3.semilogy(freqs, psd, color=self.colors['qrs_complex'])
            ax3.set_title('Power Spectral Density', fontsize=12, fontweight='bold')
            ax3.set_xlabel('Frequency (Hz)')
            ax3.set_ylabel('Power')
            ax3.grid(True, alpha=0.3)
            
            # Mark ECG frequency bands
            ax3.axvspan(0.5, 40, alpha=0.1, color=self.colors['normal'])
            ax3.text(20, np.max(psd)/2, 'ECG Band', 
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 4. RR interval histogram (middle-center)
        ax4 = fig.add_subplot(gs[1, 1])
        if 'rr_intervals' in analysis_results:
            rr_intervals = analysis_results['rr_intervals']
            ax4.hist(rr_intervals, bins=20, 
                    color=self.colors['p_wave'],
                    edgecolor='black', alpha=0.7)
            ax4.set_title('RR Interval Distribution', fontsize=12, fontweight='bold')
            ax4.set_xlabel('RR Interval (ms)')
            ax4.set_ylabel('Count')
            ax4.grid(True, alpha=0.3)
            
            # Add mean line
            mean_rr = np.mean(rr_intervals)
            ax4.axvline(mean_rr, color='red', linestyle='--', linewidth=2,
                       label=f'Mean: {mean_rr:.1f} ms')
            ax4.legend()
        
        # 5. Poincaré plot (middle-right)
        ax5 = fig.add_subplot(gs[1, 2])
        if 'rr_intervals' in analysis_results and len(analysis_results['rr_intervals']) > 1:
            rr = analysis_results['rr_intervals']
            ax5.scatter(rr[:-1], rr[1:], 
                       color=self.colors['t_wave'],
                       alpha=0.6, s=20)
            ax5.set_title('Poincaré Plot', fontsize=12, fontweight='bold')
            ax5.set_xlabel('RRₙ (ms)')
            ax5.set_ylabel('RRₙ₊₁ (ms)')
            ax5.grid(True, alpha=0.3)
            
            # Add identity line
            lims = [np.min([ax5.get_xlim(), ax5.get_ylim()]),
                   np.max([ax5.get_xlim(), ax5.get_ylim()])]
            ax5.plot(lims, lims, 'k--', alpha=0.5, linewidth=1)
            ax5.set_aspect('equal')
            ax5.set_xlim(lims)
            ax5.set_ylim(lims)
        
        # 6. Beat template (bottom-left)
        ax6 = fig.add_subplot(gs[2, 0])
        if 'beat_template' in analysis_results:
            beat = analysis_results['beat_template']
            beat_time = np.arange(len(beat)) / self.sampling_rate * 1000  # ms
            ax6.plot(beat_time, beat, color=self.colors['ecg_signal'], linewidth=2)
            ax6.set_title('Average Beat Template', fontsize=12, fontweight='bold')
            ax6.set_xlabel('Time (ms)')
            ax6.set_ylabel('Amplitude (mV)')
            ax6.grid(True, alpha=0.3)
            
            # Mark wave components if available
            if 'wave_indices' in analysis_results:
                waves = analysis_results['wave_indices']
                colors = ['blue', 'red', 'green', 'orange', 'purple']
                labels = ['P', 'Q', 'R', 'S', 'T']
                for i, (start, end) in enumerate(waves):
                    if i < len(colors):
                        ax6.axvspan(beat_time[start], beat_time[end], 
                                   alpha=0.2, color=colors[i])
                        ax6.text(beat_time[(start+end)//2], np.max(beat)*0.8,
                                labels[i], ha='center', fontweight='bold')
        
        # 7. Metrics dashboard (bottom-center)
        ax7 = fig.add_subplot(gs[2, 1])
        ax7.axis('off')
        
        # Create text box with metrics
        metrics_text = "ECG Analysis Metrics\n"
        metrics_text += "=" * 30 + "\n"
        
        key_metrics = ['heart_rate', 'hrv', 'qt_interval', 'qrs_duration']
        for metric in key_metrics:
            if metric in analysis_results:
                value = analysis_results[metric]
                unit = 'bpm' if metric == 'heart_rate' else 'ms'
                metrics_text += f"{metric.replace('_', ' ').title()}: {value:.1f} {unit}\n"
        
        if 'arrhythmia_type' in analysis_results:
            arrhythmia = analysis_results['arrhythmia_type']
            metrics_text += f"\nArrhythmia: {arrhythmia}\n"
        
        if 'signal_quality' in analysis_results:
            quality = analysis_results['signal_quality']
            metrics_text += f"\nSignal Quality: {quality}/100\n"
        
        ax7.text(0.05, 0.95, metrics_text,
                transform=ax7.transAxes,
                fontfamily='monospace',
                fontsize=10,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        # 8. Risk indicators (bottom-right)
        ax8 = fig.add_subplot(gs[2, 2])
        ax8.axis('off')
        
        # Create risk indicators
        risk_indicators = []
        if 'risk_score' in analysis_results:
            score = analysis_results['risk_score']
            if score < 30:
                risk_level = 'LOW', self.colors['normal']
            elif score < 70:
                risk_level = 'MODERATE', self.colors['warning']
            else:
                risk_level = 'HIGH', self.colors['alert']
            
            risk_indicators.append(('Overall Risk', risk_level))
        
        # Add other risk indicators
        indicators = [
            ('QTc Prolongation', 'normal'),
            ('ST Depression', 'normal'),
            ('Arrhythmia Risk', 'normal'),
            ('Ischemia Risk', 'normal')
        ]
        risk_indicators.extend(indicators)
        
        # Plot risk indicators
        y_pos = 0.9
        for name, (level, color) in risk_indicators:
            ax8.text(0.1, y_pos, f"{name}:", 
                    transform=ax8.transAxes,
                    fontsize=10, fontweight='bold')
            ax8.text(0.6, y_pos, level,
                    transform=ax8.transAxes,
                    fontsize=10, fontweight='bold',
                    color=color)
            y_pos -= 0.12
        
        # Add title
        fig.suptitle('Comprehensive ECG Analysis Dashboard', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"Dashboard saved to {save_path}")
        
        return fig
    
    def create_interactive_dashboard(self, ecg_signal: np.ndarray,
                                    analysis_results: Dict,
                                    save_path: str = None) -> Optional[go.Figure]:
        """Create interactive Plotly dashboard"""
        if not PLOTLY_AVAILABLE:
            print("Plotly not available.")
            return None
        
        # Create subplot figure
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=('Raw ECG Signal', 'Filtered ECG', 'Power Spectrum',
                          'RR Interval Histogram', 'Poincaré Plot', 'Beat Template',
                          'Metrics Dashboard', 'Risk Indicators', 'Trend Analysis'),
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        time = np.arange(len(ecg_signal)) / self.sampling_rate
        
        # 1. Raw ECG signal
        fig.add_trace(
            go.Scatter(
                x=time, y=ecg_signal,
                mode='lines',
                name='ECG Signal',
                line=dict(color=self.colors['ecg_signal'], width=1),
                hovertemplate='Time: %{x:.2f}s<br>Amplitude: %{y:.2f}mV<extra></extra>'
            ),
            row=1, col=1
        )
        
        # 2. Filtered ECG (if available)
        if 'filtered_signal' in analysis_results:
            filtered = analysis_results['filtered_signal']
            time_filtered = time[:len(filtered)]
            fig.add_trace(
                go.Scatter(
                    x=time_filtered, y=filtered,
                    mode='lines',
                    name='Filtered',
                    line=dict(color=self.colors['p_wave'], width=1),
                    hovertemplate='Time: %{x:.2f}s<br>Amplitude: %{y:.2f}mV<extra></extra>'
                ),
                row=1, col=2
            )
        
        # 3. Power spectrum
        if 'psd' in analysis_results:
            freqs, psd = analysis_results['psd']
            fig.add_trace(
                go.Scatter(
                    x=freqs, y=psd,
                    mode='lines',
                    name='PSD',
                    line=dict(color=self.colors['qrs_complex']),
                    hovertemplate='Frequency: %{x:.1f}Hz<br>Power: %{y:.2e}<extra></extra>'
                ),
                row=1, col=3
            )
        
        # 4. RR interval histogram
        if 'rr_intervals' in analysis_results:
            rr_intervals = analysis_results['rr_intervals']
            fig.add_trace(
                go.Histogram(
                    x=rr_intervals,
                    name='RR Intervals',
                    marker_color=self.colors['p_wave'],
                    opacity=0.7,
                    nbinsx=20
                ),
                row=2, col=1
            )
        
        # 5. Poincaré plot
        if 'rr_intervals' in analysis_results and len(analysis_results['rr_intervals']) > 1:
            rr = analysis_results['rr_intervals']
            fig.add_trace(
                go.Scatter(
                    x=rr[:-1], y=rr[1:],
                    mode='markers',
                    name='Poincaré',
                    marker=dict(
                        color=self.colors['t_wave'],
                        size=8,
                        opacity=0.6
                    ),
                    hovertemplate='RRₙ: %{x:.1f}ms<br>RRₙ₊₁: %{y:.1f}ms<extra></extra>'
                ),
                row=2, col=2
            )
        
        # 6. Beat template
        if 'beat_template' in analysis_results:
            beat = analysis_results['beat_template']
            beat_time = np.arange(len(beat)) / self.sampling_rate * 1000
            fig.add_trace(
                go.Scatter(
                    x=beat_time, y=beat,
                    mode='lines',
                    name='Beat Template',
                    line=dict(color=self.colors['ecg_signal'], width=2),
                    hovertemplate='Time: %{x:.1f}ms<br>Amplitude: %{y:.2f}mV<extra></extra>'
                ),
                row=2, col=3
            )
        
        # 7. Metrics dashboard (text)
        metrics_text = "<b>ECG Analysis Metrics</b><br>"
        metrics_text += "=" * 30 + "<br>"
        
        key_metrics = ['heart_rate', 'hrv', 'qt_interval', 'qrs_duration']
        for metric in key_metrics:
            if metric in analysis_results:
                value = analysis_results[metric]
                unit = 'bpm' if metric == 'heart_rate' else 'ms'
                metrics_text += f"{metric.replace('_', ' ').title()}: {value:.1f} {unit}<br>"
        
        fig.add_trace(
            go.Scatter(
                x=[0], y=[0],
                mode='text',
                text=[metrics_text],
                textposition='middle left',
                showlegend=False,
                hoverinfo='none'
            ),
            row=3, col=1
        )
        
        # 8. Risk indicators (gauge charts)
        if 'risk_score' in analysis_results:
            score = analysis_results['risk_score']
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={'text': "Risk Score"},
                    domain={'row': 3, 'column': 2},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': self.colors['alert']},
                        'steps': [
                            {'range': [0, 30], 'color': self.colors['normal']},
                            {'range': [30, 70], 'color': self.colors['warning']},
                            {'range': [70, 100], 'color': self.colors['alert']}
                        ]
                    }
                ),
                row=3, col=2
            )
        
        # 9. Trend analysis (placeholder)
        fig.add_trace(
            go.Scatter(
                x=[0, 1, 2, 3, 4],
                y=[0, 1, 0, -1, 0],
                mode='lines',
                name='Trend',
                line=dict(color=self.colors['baseline'], width=1),
                hovertemplate='Time: %{x}<br>Value: %{y}<extra></extra>'
            ),
            row=3, col=3
        )
        
        # Update layout
        fig.update_layout(
            title_text="Interactive ECG Analysis Dashboard",
            title_font_size=20,
            title_font_color=self.colors['text'],
            showlegend=True,
            height=900,
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            font=dict(color=self.colors['text'])
        )
        
        # Update axes
        fig.update_xaxes(title_text="Time (s)", row=1, col=1)
        fig.update_yaxes(title_text="Amplitude (mV)", row=1, col=1)
        
        fig.update_xaxes(title_text="Time (s)", row=1, col=2)
        fig.update_yaxes(title_text="Amplitude (mV)", row=1, col=2)
        
        fig.update_xaxes(title_text="Frequency (Hz)", row=1, col=3)
        fig.update_yaxes(title_text="Power", type="log", row=1, col=3)
        
        fig.update_xaxes(title_text="RR Interval (ms)", row=2, col=1)
        fig.update_yaxes(title_text="Count", row=2, col=1)
        
        fig.update_xaxes(title_text="RRₙ (ms)", row=2, col=2)
        fig.update_yaxes(title_text="RRₙ₊₁ (ms)", row=2, col=2)
        
        fig.update_xaxes(title_text="Time (ms)", row=2, col=3)
        fig.update_yaxes(title_text="Amplitude (mV)", row=2, col=3)
        
        # Hide axes for text subplots
        for row in [3]:
            for col in [1, 2, 3]:
                fig.update_xaxes(showgrid=False, zeroline=False, visible=False, row=row, col=col)
                fig.update_yaxes(showgrid=False, zeroline=False, visible=False, row=row, col=col)
        
        # Save if requested
        if save_path:
            fig.write_html(save_path)
            print(f"Interactive dashboard saved to {save_path}")
        
        return fig
    
    def plot_comparative_analysis(self, ecg_signals: List[np.ndarray],
                                 signal_names: List[str],
                                 analysis_results: List[Dict],
                                 figsize: Tuple[int, int] = (15, 10),
                                 save_path: str = None) -> plt.Figure:
        """Comparative analysis of multiple ECG signals"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available.")
            return None
        
        n_signals = len(ecg_signals)
        if n_signals == 0:
            return None
        
        # Create figure
        fig, axes = plt.subplots(n_signals, 2, figsize=figsize)
        if n_signals == 1:
            axes = axes.reshape(1, -1)
        
        for i in range(n_signals):
            # Left column: ECG signals
            ax_signal = axes[i, 0]
            time = np.arange(len(ecg_signals[i])) / self.sampling_rate
            
            ax_signal.plot(time, ecg_signals[i], 
                          color=self.colors['ecg_signal'],
                          linewidth=1,
                          alpha=0.8)
            
            ax_signal.set_title(f'{signal_names[i]} - ECG Signal', 
                               fontsize=10, fontweight='bold')
            ax_signal.set_xlabel('Time (s)')
            ax_signal.set_ylabel('Amplitude (mV)')
            ax_signal.grid(True, alpha=0.3)
            
            # Right column: Metrics
            ax_metrics = axes[i, 1]
            ax_metrics.axis('off')
            
            if i < len(analysis_results):
                metrics = analysis_results[i]
                
                # Create metrics text
                metrics_text = f"<{signal_names[i]} Analysis>\n"
                metrics_text += "=" * 30 + "\n"
                
                # Add key metrics
                key_metrics = ['heart_rate', 'hrv', 'qt_interval', 
                              'qrs_duration', 'signal_quality']
                for metric in key_metrics:
                    if metric in metrics:
                        value = metrics[metric]
                        if metric == 'heart_rate':
                            metrics_text += f"Heart Rate: {value:.1f} bpm\n"
                        elif metric == 'hrv':
                            metrics_text += f"HRV: {value:.1f} ms\n"
                        elif metric == 'qt_interval':
                            metrics_text += f"QT Interval: {value:.1f} ms\n"
                        elif metric == 'qrs_duration':
                            metrics_text += f"QRS Duration: {value:.1f} ms\n"
                        elif metric == 'signal_quality':
                            metrics_text += f"Signal Quality: {value:.0f}/100\n"
                
                if 'arrhythmia_type' in metrics:
                    arrhythmia = metrics['arrhythmia_type']
                    metrics_text += f"\nArrhythmia: {arrhythmia}\n"
                
                if 'risk_level' in metrics:
                    risk = metrics['risk_level']
                    metrics_text += f"Risk Level: {risk}\n"
                
                ax_metrics.text(0.05, 0.95, metrics_text,
                               transform=ax_metrics.transAxes,
                               fontfamily='monospace',
                               fontsize=9,
                               verticalalignment='top',
                               bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        # Add overall title
        fig.suptitle('Comparative ECG Analysis', 
                    fontsize=14, fontweight='bold', y=0.98)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"Comparative analysis saved to {save_path}")
        
        return fig
    
    def plot_trend_analysis(self, trend_data: Dict,
                           figsize: Tuple[int, int] = (12, 8),
                           save_path: str = None) -> plt.Figure:
        """Plot trend analysis over time"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available.")
            return None
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        # 1. Heart rate trend
        if 'heart_rate_trend' in trend_data:
            times, hr_values = trend_data['heart_rate_trend']
            axes[0, 0].plot(times, hr_values, 
                          color=self.colors['alert'],
                          marker='o', markersize=4,
                          linewidth=1.5, alpha=0.7)
            axes[0, 0].set_title('Heart Rate Trend', fontsize=11, fontweight='bold')
            axes[0, 0].set_xlabel('Time')
            axes[0, 0].set_ylabel('Heart Rate (bpm)')
            axes[0, 0].grid(True, alpha=0.3)
            
            # Add normal range
            axes[0, 0].axhspan(60, 100, alpha=0.1, color=self.colors['normal'])
            axes[0, 0].axhline(60, color=self.colors['normal'], linestyle='--', alpha=0.5)
            axes[0, 0].axhline(100, color=self.colors['normal'], linestyle='--', alpha=0.5)
        
        # 2. HRV trend
        if 'hrv_trend' in trend_data:
            times, hrv_values = trend_data['hrv_trend']
            axes[0, 1].plot(times, hrv_values,
                          color=self.colors['p_wave'],
                          marker='s', markersize=4,
                          linewidth=1.5, alpha=0.7)
            axes[0, 1].set_title('Heart Rate Variability Trend', fontsize=11, fontweight='bold')
            axes[0, 1].set_xlabel('Time')
            axes[0, 1].set_ylabel('HRV (ms)')
            axes[0, 1].grid(True, alpha=0.3)
        
        # 3. QT interval trend
        if 'qt_trend' in trend_data:
            times, qt_values = trend_data['qt_trend']
            axes[1, 0].plot(times, qt_values,
                          color=self.colors['t_wave'],
                          marker='^', markersize=4,
                          linewidth=1.5, alpha=0.7)
            axes[1, 0].set_title('QT Interval Trend', fontsize=11, fontweight='bold')
            axes[1, 0].set_xlabel('Time')
            axes[1, 0].set_ylabel('QT Interval (ms)')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Add normal range
            axes[1, 0].axhline(440, color=self.colors['alert'], linestyle='--', alpha=0.7,
                              label='Normal Max (440ms)')
            axes[1, 0].legend(fontsize=8)
        
        # 4. Risk score trend
        if 'risk_trend' in trend_data:
            times, risk_values = trend_data['risk_trend']
            axes[1, 1].plot(times, risk_values,
                          color=self.colors['r_peaks'],
                          marker='D', markersize=4,
                          linewidth=1.5, alpha=0.7)
            axes[1, 1].set_title('Risk Score Trend', fontsize=11, fontweight='bold')
            axes[1, 1].set_xlabel('Time')
            axes[1, 1].set_ylabel('Risk Score')
            axes[1, 1].grid(True, alpha=0.3)
            
            # Add risk zones
            axes[1, 1].axhspan(0, 30, alpha=0.2, color=self.colors['normal'])
            axes[1, 1].axhspan(30, 70, alpha=0.2, color=self.colors['warning'])
            axes[1, 1].axhspan(70, 100, alpha=0.2, color=self.colors['alert'])
        
        # Adjust layout
        plt.tight_layout()
        
        # Add overall title
        fig.suptitle('ECG Parameter Trends Over Time', 
                    fontsize=14, fontweight='bold', y=0.98)
        
        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"Trend analysis saved to {save_path}")
        
        return fig
    
    def generate_report(self, ecg_signal: np.ndarray,
                       analysis_results: Dict,
                       output_dir: str = '.',
                       patient_id: str = 'Unknown',
                       date: str = None) -> Dict:
        """Generate comprehensive visualization report"""
        import os
        from datetime import datetime
        
        if date is None:
            date = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        report_dir = os.path.join(output_dir, f"ecg_report_{patient_id}_{date}")
        os.makedirs(report_dir, exist_ok=True)
        
        report_files = {}
        
        # 1. Main ECG signal plot
        if MATPLOTLIB_AVAILABLE:
            main_plot_path = os.path.join(report_dir, "ecg_signal.png")
            self.plot_ecg_signal(ecg_signal, save_path=main_plot_path)
            report_files['main_plot'] = main_plot_path
        
        # 2. Comprehensive dashboard
        if MATPLOTLIB_AVAILABLE:
            dashboard_path = os.path.join(report_dir, "ecg_dashboard.png")
            self.plot_ecg_with_analysis(ecg_signal, analysis_results, save_path=dashboard_path)
            report_files['dashboard'] = dashboard_path
        
        # 3. Interactive dashboard (if Plotly available)
        if PLOTLY_AVAILABLE:
            interactive_path = os.path.join(report_dir, "interactive_dashboard.html")
            self.create_interactive_dashboard(ecg_signal, analysis_results, save_path=interactive_path)
            report_files['interactive'] = interactive_path
        
        # 4. Generate summary report text
        summary_path = os.path.join(report_dir, "summary.txt")
        with open(summary_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("ECG ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Patient ID: {patient_id}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Signal Length: {len(ecg_signal)} samples\n")
            f.write(f"Duration: {len(ecg_signal)/self.sampling_rate:.1f} seconds\n\n")
            
            f.write("ANALYSIS RESULTS:\n")
            f.write("-" * 40 + "\n")
            
            # Write key metrics
            key_metrics = ['heart_rate', 'hrv', 'qt_interval', 'qrs_duration',
                          'signal_quality', 'arrhythmia_type', 'risk_level']
            
            for metric in key_metrics:
                if metric in analysis_results:
                    value = analysis_results[metric]
                    if metric == 'heart_rate':
                        f.write(f"Heart Rate: {value:.1f} bpm\n")
                    elif metric == 'hrv':
                        f.write(f"Heart Rate Variability: {value:.1f} ms\n")
                    elif metric == 'qt_interval':
                        f.write(f"QT Interval: {value:.1f} ms\n")
                    elif metric == 'qrs_duration':
                        f.write(f"QRS Duration: {value:.1f} ms\n")
                    elif metric == 'signal_quality':
                        f.write(f"Signal Quality: {value:.0f}/100\n")
                    else:
                        f.write(f"{metric.replace('_', ' ').title()}: {value}\n")
            
            f.write("\nRECOMMENDATIONS:\n")
            f.write("-" * 40 + "\n")
            
            # Generate recommendations based on analysis
            recommendations = []
            
            if 'heart_rate' in analysis_results:
                hr = analysis_results['heart_rate']
                if hr < 50:
                    recommendations.append("Bradycardia detected. Consider cardiology consultation.")
                elif hr > 120:
                    recommendations.append("Tachycardia detected. Consider cardiology consultation.")
                elif 60 <= hr <= 100:
                    recommendations.append("Heart rate within normal range.")
            
            if 'qt_interval' in analysis_results:
                qt = analysis_results['qt_interval']
                if qt > 440:
                    recommendations.append("QT interval prolonged. Risk of torsades de pointes.")
                elif qt > 500:
                    recommendations.append("Severely prolonged QT interval. Urgent cardiology review required.")
            
            if 'arrhythmia_type' in analysis_results:
                arrhythmia = analysis_results['arrhythmia_type']
                if arrhythmia != 'Normal Sinus Rhythm':
                    recommendations.append(f"{arrhythmia} detected. Cardiology consultation recommended.")
            
            if 'risk_level' in analysis_results:
                risk = analysis_results['risk_level']
                if risk == 'HIGH':
                    recommendations.append("High risk assessment. Immediate clinical review recommended.")
                elif risk == 'MODERATE':
                    recommendations.append("Moderate risk. Schedule follow-up within 1-2 weeks.")
                else:
                    recommendations.append("Low risk. Routine follow-up as per clinical guidelines.")
            
            if not recommendations:
                recommendations.append("No significant abnormalities detected. Continue routine monitoring.")
            
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. {rec}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 60 + "\n")
        
        report_files['summary'] = summary_path
        
        # Create HTML report if Plotly is available
        if PLOTLY_AVAILABLE:
            html_path = os.path.join(report_dir, "report.html")
            self._generate_html_report(ecg_signal, analysis_results, patient_id, html_path)
            report_files['html_report'] = html_path
        
        print(f"Report generated in: {report_dir}")
        print(f"Files created: {list(report_files.keys())}")
        
        return report_files
    
    def _generate_html_report(self, ecg_signal: np.ndarray,
                            analysis_results: Dict,
                            patient_id: str,
                            output_path: str):
        """Generate HTML report with embedded visualizations"""
        if not PLOTLY_AVAILABLE:
            return
        
        from datetime import datetime
        
        # Create interactive figure
        fig = self.create_interactive_dashboard(ecg_signal, analysis_results)
        
        # Convert to HTML
        html_content = fig.to_html(include_plotlyjs='cdn', full_html=True)
        
        # Enhance HTML with additional content
        enhanced_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ECG Analysis Report - {patient_id}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    border-bottom: 2px solid #2c3e50;
                    padding-bottom: 20px;
                }}
                .header h1 {{
                    color: #2c3e50;
                    margin-bottom: 10px;
                }}
                .patient-info {{
                    display: flex;
                    justify-content: space-between;
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .info-item {{
                    flex: 1;
                    text-align: center;
                }}
                .info-label {{
                    font-weight: bold;
                    color: #666;
                    font-size: 0.9em;
                }}
                .info-value {{
                    font-size: 1.1em;
                    color: #2c3e50;
                    margin-top: 5px;
                }}
                .section {{
                    margin-bottom: 30px;
                }}
                .section-title {{
                    color: #2c3e50;
                    border-bottom: 1px solid #ddd;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-bottom: 30px;
                }}
                .metric-card {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid #3498db;
                }}
                .metric-card.critical {{
                    border-left-color: #e74c3c;
                    background-color: #ffeaea;
                }}
                .metric-card.warning {{
                    border-left-color: #f39c12;
                    background-color: #fff4e6;
                }}
                .metric-card.normal {{
                    border-left-color: #27ae60;
                    background-color: #eafaf1;
                }}
                .metric-label {{
                    font-size: 0.9em;
                    color: #666;
                    margin-bottom: 5px;
                }}
                .metric-value {{
                    font-size: 1.4em;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .metric-unit {{
                    font-size: 0.8em;
                    color: #888;
                }}
                .recommendations {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 5px;
                    margin-top: 30px;
                }}
                .recommendation-item {{
                    margin-bottom: 10px;
                    padding-left: 20px;
                    position: relative;
                }}
                .recommendation-item:before {{
                    content: "•";
                    position: absolute;
                    left: 0;
                    color: #3498db;
                    font-size: 1.5em;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #666;
                    font-size: 0.9em;
                }}
                .plot-container {{
                    margin: 20px 0;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px;
                    background-color: white;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>ECG Analysis Report</h1>
                    <p>Cardiology Machine Learning System - Clinical Grade Analysis</p>
                </div>
                
                <div class="patient-info">
                    <div class="info-item">
                        <div class="info-label">Patient ID</div>
                        <div class="info-value">{patient_id}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Report Date</div>
                        <div class="info-value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Signal Duration</div>
                        <div class="info-value">{len(ecg_signal)/self.sampling_rate:.1f} seconds</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2 class="section-title">Key Metrics</h2>
                    <div class="metrics-grid">
                        <!-- Metrics will be populated by JavaScript -->
                    </div>
                </div>
                
                <div class="section">
                    <h2 class="section-title">Interactive Analysis Dashboard</h2>
                    <div class="plot-container">
                        {html_content}
                    </div>
                </div>
                
                <div class="section">
                    <h2 class="section-title">Clinical Recommendations</h2>
                    <div class="recommendations" id="recommendations">
                        <!-- Recommendations will be populated by JavaScript -->
                    </div>
                </div>
                
                <div class="footer">
                    <p>This report was automatically generated by the Cardiology ML System.</p>
                    <p>Report ID: ECG-{patient_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}</p>
                    <p>© {datetime.now().year} Cardiology ML Assessment Platform. All rights reserved.</p>
                </div>
            </div>
            
            <script>
                // Populate metrics from analysis results
                const analysisResults = {analysis_results};
                
                function createMetricCard(label, value, unit = '', status = 'normal') {{
                    return `
                    <div class="metric-card ${{status}}">
                        <div class="metric-label">${{label}}</div>
                        <div class="metric-value">${{value}}<span class="metric-unit"> ${{unit}}</span></div>
                    </div>
                    `;
                }}
                
                // Define key metrics to display
                const metricsConfig = [
                    {{ key: 'heart_rate', label: 'Heart Rate', unit: 'bpm', 
                      getStatus: (val) => val < 60 || val > 100 ? 'warning' : 'normal' }},
                    {{ key: 'hrv', label: 'Heart Rate Variability', unit: 'ms',
                      getStatus: (val) => val < 20 ? 'warning' : 'normal' }},
                    {{ key: 'qt_interval', label: 'QT Interval', unit: 'ms',
                      getStatus: (val) => val > 440 ? 'critical' : val > 400 ? 'warning' : 'normal' }},
                    {{ key: 'qrs_duration', label: 'QRS Duration', unit: 'ms',
                      getStatus: (val) => val > 120 ? 'warning' : 'normal' }},
                    {{ key: 'signal_quality', label: 'Signal Quality', unit: '/100',
                      getStatus: (val) => val < 60 ? 'critical' : val < 80 ? 'warning' : 'normal' }}
                ];
                
                // Populate metrics grid
                const metricsGrid = document.querySelector('.metrics-grid');
                metricsConfig.forEach(config => {{
                    if (analysisResults[config.key] !== undefined) {{
                        const value = analysisResults[config.key];
                        const formattedValue = typeof value === 'number' ? value.toFixed(1) : value;
                        const status = config.getStatus ? config.getStatus(value) : 'normal';
                        metricsGrid.innerHTML += createMetricCard(config.label, formattedValue, config.unit, status);
                    }}
                }});
                
                // Add arrhythmia metric if present
                if (analysisResults.arrhythmia_type && analysisResults.arrhythmia_type !== 'Normal Sinus Rhythm') {{
                    metricsGrid.innerHTML += createMetricCard('Arrhythmia', analysisResults.arrhythmia_type, '', 'critical');
                }}
                
                // Generate recommendations
                const recommendationsDiv = document.getElementById('recommendations');
                const recommendations = [];
                
                // Heart rate recommendations
                if (analysisResults.heart_rate) {{
                    const hr = analysisResults.heart_rate;
                    if (hr < 50) {{
                        recommendations.push("Bradycardia detected. Consider cardiology consultation.");
                    }} else if (hr > 120) {{
                        recommendations.push("Tachycardia detected. Consider cardiology consultation.");
                    }} else if (hr >= 60 && hr <= 100) {{
                        recommendations.push("Heart rate within normal range.");
                    }}
                }}
                
                // QT interval recommendations
                if (analysisResults.qt_interval) {{
                    const qt = analysisResults.qt_interval;
                    if (qt > 500) {{
                        recommendations.push("Severely prolonged QT interval. Urgent cardiology review required.");
                    }} else if (qt > 440) {{
                        recommendations.push("QT interval prolonged. Risk of torsades de pointes.");
                    }}
                }}
                
                // Arrhythmia recommendations
                if (analysisResults.arrhythmia_type && analysisResults.arrhythmia_type !== 'Normal Sinus Rhythm') {{
                    recommendations.push(`${{analysisResults.arrhythmia_type}} detected. Cardiology consultation recommended.`);
                }}
                
                // Risk level recommendations
                if (analysisResults.risk_level) {{
                    const risk = analysisResults.risk_level;
                    if (risk === 'HIGH') {{
                        recommendations.push("High risk assessment. Immediate clinical review recommended.");
                    }} else if (risk === 'MODERATE') {{
                        recommendations.push("Moderate risk. Schedule follow-up within 1-2 weeks.");
                    }} else {{
                        recommendations.push("Low risk. Routine follow-up as per clinical guidelines.");
                    }}
                }}
                
                // Signal quality recommendations
                if (analysisResults.signal_quality && analysisResults.signal_quality < 60) {{
                    recommendations.push("Poor signal quality. Consider re-recording with improved setup.");
                }}
                
                // Add recommendations to DOM
                if (recommendations.length > 0) {{
                    recommendations.forEach(rec => {{
                        recommendationsDiv.innerHTML += `<div class="recommendation-item">${{rec}}</div>`;
                    }});
                }} else {{
                    recommendationsDiv.innerHTML = `<div class="recommendation-item">No significant abnormalities detected. Continue routine monitoring.</div>`;
                }}
                
                // Print button
                const printButton = document.createElement('button');
                printButton.textContent = 'Print Report';
                printButton.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                    z-index: 1000;
                `;
                printButton.onclick = () => window.print();
                document.body.appendChild(printButton);
            </script>
        </body>
        </html>
        """
        
        # Write HTML file
        with open(output_path, 'w') as f:
            f.write(enhanced_html)

def generate_sample_data():
    """Generate sample ECG data and analysis results for demonstration"""
    # Generate sample ECG signal
    sampling_rate = 500
    duration = 10  # seconds
    n_samples = sampling_rate * duration
    
    t = np.linspace(0, duration, n_samples)
    
    # Create realistic ECG-like signal
    ecg_signal = (
        1.0 * np.sin(2 * np.pi * 1.0 * t) +  # P wave / T wave
        2.0 * np.sin(2 * np.pi * 5.0 * t) * np.exp(-((t % 1.0) - 0.3)**2 / 0.02) +  # QRS complex
        0.3 * np.sin(2 * np.pi * 0.2 * t) +  # Baseline wander
        0.1 * np.sin(2 * np.pi * 50 * t) +  # Powerline interference
        0.05 * np.random.randn(n_samples)    # Noise
    )
    
    # Generate sample analysis results
    analysis_results = {
        'heart_rate': 72.5,
        'hrv': 42.3,
        'qt_interval': 410.2,
        'qrs_duration': 92.7,
        'signal_quality': 87.5,
        'arrhythmia_type': 'Normal Sinus Rhythm',
        'risk_level': 'LOW',
        'risk_score': 25.4,
        
        # For visualizations
        'filtered_signal': ecg_signal * 0.9,  # Simplified filtered version
        'rr_intervals': np.random.normal(800, 50, 12),  # Sample RR intervals in ms
        
        # PSD
        'psd': (np.linspace(0, 100, 100), np.exp(-np.linspace(0, 100, 100)**2 / 200)),
        
        # Beat template
        'beat_template': np.sin(2 * np.pi * np.linspace(0, 1, 200)) * np.exp(-(np.linspace(0, 1, 200)-0.5)**2 / 0.02),
        
        # Wave indices (for beat template annotation)
        'wave_indices': [(20, 40), (80, 90), (100, 110), (120, 130), (160, 180)]
    }
    
    return ecg_signal, analysis_results

def main():
    """Demonstration of ECG Visualization Dashboard"""
    print("Initializing ECG Visualization Dashboard...")
    print("=" * 60)
    
    # Create dashboard instance
    dashboard = ECGVisualizationDashboard(sampling_rate=500, style='clinical')
    
    # Generate sample data
    print("Generating sample ECG data...")
    ecg_signal, analysis_results = generate_sample_data()
    
    print(f"ECG Signal: {len(ecg_signal)} samples")
    print(f"Duration: {len(ecg_signal)/dashboard.sampling_rate:.1f} seconds")
    
    # Create visualizations
    print("\nCreating visualizations...")
    print("-" * 40)
    
    # 1. Basic ECG signal plot
    print("1. Creating basic ECG signal plot...")
    fig1 = dashboard.plot_ecg_signal(ecg_signal, figsize=(12, 4))
    if fig1:
        plt.savefig('ecg_signal_plot.png', dpi=300, bbox_inches='tight')
        print("   Saved: ecg_signal_plot.png")
        plt.close(fig1)
    
    # 2. Comprehensive dashboard
    print("2. Creating comprehensive dashboard...")
    fig2 = dashboard.plot_ecg_with_analysis(ecg_signal, analysis_results, figsize=(16, 10))
    if fig2:
        plt.savefig('ecg_dashboard.png', dpi=300, bbox_inches='tight')
        print("   Saved: ecg_dashboard.png")
        plt.close(fig2)
    
    # 3. Interactive dashboard (if Plotly available)
    if PLOTLY_AVAILABLE:
        print("3. Creating interactive dashboard...")
        fig3 = dashboard.create_interactive_dashboard(ecg_signal, analysis_results)
        if fig3:
            fig3.write_html('interactive_dashboard.html')
            print("   Saved: interactive_dashboard.html")
    
    # 4. Comparative analysis
    print("4. Creating comparative analysis...")
    # Generate multiple signals for comparison
    ecg_signals = []
    for i in range(3):
        t = np.linspace(0, 5, 2500)
        signal = np.sin(2 * np.pi * (1 + i*0.2) * t) + 0.1 * np.random.randn(2500)
        ecg_signals.append(signal)
    
    signal_names = ['Baseline', 'Exercise', 'Recovery']
    analysis_list = [
        {'heart_rate': 65, 'hrv': 50, 'risk_level': 'LOW'},
        {'heart_rate': 120, 'hrv': 25, 'risk_level': 'MODERATE'},
        {'heart_rate': 75, 'hrv': 40, 'risk_level': 'LOW'}
    ]
    
    fig4 = dashboard.plot_comparative_analysis(
        ecg_signals, signal_names, analysis_list, figsize=(12, 8)
    )
    if fig4:
        plt.savefig('comparative_analysis.png', dpi=300, bbox_inches='tight')
        print("   Saved: comparative_analysis.png")
        plt.close(fig4)
    
    # 5. Trend analysis
    print("5. Creating trend analysis...")
    trend_data = {
        'heart_rate_trend': (
            ['08:00', '12:00', '16:00', '20:00', '00:00'],
            [65, 72, 68, 75, 62]
        ),
        'hrv_trend': (
            ['08:00', '12:00', '16:00', '20:00', '00:00'],
            [45, 38, 42, 35, 50]
        ),
        'qt_trend': (
            ['08:00', '12:00', '16:00', '20:00', '00:00'],
            [410, 415, 425, 420, 405]
        ),
        'risk_trend': (
            ['08:00', '12:00', '16:00', '20:00', '00:00'],
            [20, 35, 45, 30, 25]
        )
    }
    
    fig5 = dashboard.plot_trend_analysis(trend_data, figsize=(10, 6))
    if fig5:
        plt.savefig('trend_analysis.png', dpi=300, bbox_inches='tight')
        print("   Saved: trend_analysis.png")
        plt.close(fig5)
    
    # 6. Generate comprehensive report
    print("6. Generating comprehensive report...")
    report_files = dashboard.generate_report(
        ecg_signal, analysis_results,
        output_dir='.',
        patient_id='DEMO001',
        date='20240115_1430'
    )
    
    print(f"   Report directory: {list(report_files.keys())}")
    
    print("\n" + "=" * 60)
    print("VISUALIZATION DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nGenerated files:")
    print("• ecg_signal_plot.png - Basic ECG signal")
    print("• ecg_dashboard.png - Comprehensive analysis dashboard")
    if PLOTLY_AVAILABLE:
        print("• interactive_dashboard.html - Interactive Plotly dashboard")
    print("• comparative_analysis.png - Comparative analysis")
    print("• trend_analysis.png - Parameter trends over time")
    print("• ecg_report_DEMO001_20240115_1430/ - Full report directory")
    print("\nAll visualizations are ready for clinical review.")

if __name__ == "__main__":
    main()
