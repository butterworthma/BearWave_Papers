#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standardized Layout Enforcer for foF2 Analysis Charts
=====================================================

Enforces consistent positioning of data across all 2x2 charts:
- Top-Left (0,0):     Hourly Patterns (24h diurnal cycle) - ALWAYS
- Top-Right (0,1):    Statistical Distribution (box plots) - ALWAYS  
- Bottom-Left (1,0):  Temporal Progression (daily/period) - ALWAYS
- Bottom-Right (1,1): NVIS Frequency Bands - ALWAYS

Author: Research Team
License: MIT
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# Standardized layout configuration
STANDARD_LAYOUT = {
    'figure_size': (16, 12),
    'title_fontsize': 16,
    'subtitle_fontsize': 14,
    'label_fontsize': 12,
    'legend_fontsize': 10,
    'grid_alpha': 0.3,
    'colors': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
}

def create_standardized_chart(station_name, period_name, year_range):
    """Create standardized 2x2 chart with enforced positioning"""
    
    fig, axes = plt.subplots(2, 2, figsize=STANDARD_LAYOUT['figure_size'])
    
    # Standardized main title with proper spacing
    main_title = f'Ionospheric foF2 Critical Frequency Analysis\n{station_name} Station - {period_name} ({year_range})'
    fig.suptitle(main_title,
                fontsize=STANDARD_LAYOUT['title_fontsize'],
                fontweight='bold',
                y=0.98)
    
    return fig, axes

def plot_hourly_patterns(ax, df, year_columns, colors, title="Hourly Patterns (24h Diurnal Cycle)"):
    """POSITION: Top-Left (0,0) - ALWAYS hourly patterns"""
    
    # Add day/night shading first
    ax.axvspan(6, 18, alpha=0.15, color='yellow', label='Daylight')
    ax.axvspan(18, 24, alpha=0.15, color='gray', label='Night')
    ax.axvspan(0, 6, alpha=0.15, color='gray')
    
    # Plot hourly data for each year
    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Hour'] = df_year['DateTime'].dt.hour
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
        hourly_fof2 = df_year.groupby('Hour')['foF2_estimated'].mean()
        
        ax.plot(hourly_fof2.index, hourly_fof2.values,
                color=colors[i % len(colors)], marker='o', linewidth=2, markersize=4,
                label=f'{int(year)}')
    
    # Standardized formatting
    ax.set_title(title, fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel('Hour of Day (UTC)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_ylabel('Average foF2 (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.legend(loc='upper right', fontsize=STANDARD_LAYOUT['legend_fontsize'])
    ax.grid(True, alpha=STANDARD_LAYOUT['grid_alpha'])
    ax.set_xlim(0, 23)
    ax.set_xticks(range(0, 24, 6))

def plot_statistical_distribution(ax, df, year_columns, colors, title="foF2 Distribution by Year"):
    """POSITION: Top-Right (0,1) - ALWAYS statistical distribution"""
    
    fof2_data = []
    year_labels = []
    
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calculate_fof2_from_signal(df_year[year])
        fof2_data.append(fof2_values)
        year_labels.append(f'{int(year)}')
    
    # Create box plots
    bp = ax.boxplot(fof2_data, tick_labels=year_labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Standardized formatting
    ax.set_title(title, fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel('Year', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_ylabel('foF2 (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.grid(True, alpha=STANDARD_LAYOUT['grid_alpha'])

def plot_temporal_progression(ax, df, year_columns, colors, period_type="daily"):
    """POSITION: Bottom-Left (1,0) - ALWAYS temporal progression"""
    
    if period_type == "daily":
        # Daily progression for multi-day periods
        title = "Daily Average foF2 Progression"
        xlabel = "Day of Period"
        
        for i, year in enumerate(year_columns):
            df_year = df.dropna(subset=[year])
            df_year['Day'] = df_year['DateTime'].dt.day
            df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
            daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()
            
            ax.plot(daily_fof2.index, daily_fof2.values,
                    color=colors[i % len(colors)], marker='o', linewidth=2, markersize=4,
                    label=f'{int(year)}')
    
    elif period_type == "single_day":
        # 24-hour progression for single day analysis
        title = "24-hour foF2 Progression"
        xlabel = "Hour of Day"
        
        for i, year in enumerate(year_columns):
            df_year = df.dropna(subset=[year])
            df_year['Hour'] = df_year['DateTime'].dt.hour
            df_year['Minute'] = df_year['DateTime'].dt.minute
            df_year['HourDecimal'] = df_year['Hour'] + df_year['Minute'] / 60.0
            df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
            df_year = df_year.sort_values('HourDecimal')
            
            ax.plot(df_year['HourDecimal'], df_year['foF2_estimated'],
                    color=colors[i % len(colors)], marker='o', linewidth=2, markersize=3,
                    label=f'{int(year)}')
    
    elif period_type == "monthly":
        # Monthly progression for full month analysis
        title = "Daily Average foF2 Progression (Full Month)"
        xlabel = "Day of April"
        
        for i, year in enumerate(year_columns):
            df_year = df.dropna(subset=[year])
            df_year['Day'] = df_year['DateTime'].dt.day
            df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
            daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()
            
            ax.plot(daily_fof2.index, daily_fof2.values,
                    color=colors[i % len(colors)], marker='o', linewidth=2, markersize=4,
                    label=f'{int(year)}')
    
    # Standardized formatting
    ax.set_title(title, fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_ylabel('Average foF2 (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.legend(loc='upper right', fontsize=STANDARD_LAYOUT['legend_fontsize'])
    ax.grid(True, alpha=STANDARD_LAYOUT['grid_alpha'])

def plot_nvis_frequency_bands(ax, df, year_columns, title="foF2 vs NVIS Frequency Bands"):
    """POSITION: Bottom-Right (1,1) - ALWAYS NVIS frequency bands"""
    
    # Calculate overall average foF2
    all_fof2_combined = []
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calculate_fof2_from_signal(df_year[year])
        all_fof2_combined.extend(fof2_values)
    
    avg_fof2_combined = np.mean(all_fof2_combined)
    std_fof2_combined = np.std(all_fof2_combined)
    
    # Plot foF2 range
    ax.axhspan(avg_fof2_combined - std_fof2_combined, avg_fof2_combined + std_fof2_combined,
                alpha=0.3, color='blue', label=f'foF2: {avg_fof2_combined:.1f}±{std_fof2_combined:.1f} MHz')
    ax.axhline(y=avg_fof2_combined, color='blue', linewidth=2)
    
    # Add NVIS frequency bands
    ax.axhspan(2, 8, alpha=0.2, color='lightgray', label='Night NVIS (2-8 MHz)')
    ax.axhspan(8, 15, alpha=0.2, color='lightcoral', label='Day NVIS (8-15 MHz)')
    
    # Add DGFC frequencies
    ax.axhline(y=7.078, color='red', linewidth=2, linestyle='--', label='DGFC 7.078 MHz')
    ax.axhline(y=10.130, color='orange', linewidth=2, linestyle='--', label='DGFC 10.130 MHz')
    
    # Add MUF
    muf_combined = avg_fof2_combined * 3
    ax.axhline(y=muf_combined, color='purple', linewidth=2, linestyle=':',
               label=f'MUF: {muf_combined:.1f} MHz')
    
    # Standardized formatting
    ax.set_title(title, fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_ylabel('Frequency (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_xlabel('NVIS Analysis', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.legend(loc='upper left', fontsize=STANDARD_LAYOUT['legend_fontsize'])
    ax.grid(True, alpha=STANDARD_LAYOUT['grid_alpha'])
    ax.set_ylim(0, max(25, muf_combined + 5))
    ax.set_xlim(-0.5, 0.5)
    ax.set_xticks([])

def calculate_fof2_from_signal(signal_values, station="Guam", period="April"):
    """
    Calculate foF2 from signal strength values using station-specific parameters
    This matches the original script calculations exactly
    """
    fof2_values = []

    # Station-specific baselines (matching original scripts)
    if "Guam" in station:
        if "15th" in period:
            baseline_fof2 = 11.0  # Guam April 15th baseline
        else:
            baseline_fof2 = 11.2  # Guam April 15-28 baseline
        scale_factor = 10.0
        min_fof2, max_fof2 = 4.0, 18.0
    else:  # Darwin
        if "15-28" in period:
            baseline_fof2 = 9.2  # Darwin April 15-28 baseline
            scale_factor = 12.0
        else:
            baseline_fof2 = 8.5  # Darwin general baseline
            scale_factor = 10.0
        min_fof2, max_fof2 = 3.0, 15.0

    for signal in signal_values:
        if pd.notna(signal):
            # Use original calculation method
            signal_factor = signal / scale_factor
            estimated_fof2 = baseline_fof2 + signal_factor

            # Clamp to reasonable foF2 range
            estimated_fof2 = np.clip(estimated_fof2, min_fof2, max_fof2)
            fof2_values.append(estimated_fof2)

    return fof2_values

def apply_standardized_layout(fig):
    """Apply final standardized layout adjustments"""
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, hspace=0.4, wspace=0.3)

def save_standardized_chart(fig, filename):
    """Save chart with new_standard prefix and standardized settings to desktop/test folder"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    chart_filename = f"new_standard_{filename}_{timestamp}.png"

    # Create test folder on desktop if it doesn't exist
    desktop_path = "output"
    test_folder = os.path.join(desktop_path, "test")

    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
        print(f"📁 Created test folder: {test_folder}")

    # Save to desktop/test folder
    full_path = os.path.join(test_folder, chart_filename)

    plt.savefig(full_path, dpi=160, bbox_inches='tight')
    print(f"✅ Saved standardized chart to test folder: {chart_filename}")
    print(f"📁 Full path: {full_path}")

def create_standardized_filename(station, period, analysis_type):
    """Create standardized filename with new_standard prefix"""
    # Clean up the inputs for filename
    station_clean = station.replace(" ", "_")
    period_clean = period.replace(" ", "_").replace("-", "_")
    analysis_clean = analysis_type.replace(" ", "_")

    base_filename = f"{station_clean}_{period_clean}_{analysis_clean}"
    return base_filename

# Import pandas for data handling
try:
    import pandas as pd
except ImportError:
    print("⚠️ pandas not available - some functions may not work")

def main():
    """Example usage of standardized layout enforcer"""
    print("🎯 STANDARDIZED LAYOUT ENFORCER")
    print("="*40)
    print("ENFORCED POSITIONS:")
    print("  Top-Left (0,0):     Hourly Patterns (24h diurnal cycle)")
    print("  Top-Right (0,1):    Statistical Distribution (box plots)")
    print("  Bottom-Left (1,0):  Temporal Progression (daily/period)")
    print("  Bottom-Right (1,1): NVIS Frequency Bands")
    print()
    print("This ensures ALL charts show the same type of data")
    print("in the same position, with different data only when")
    print("the standard data type is not available.")

if __name__ == "__main__":
    main()
