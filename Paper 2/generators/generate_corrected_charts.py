#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Corrected Charts with Proper foF2 Calculations
=======================================================

This script generates charts using the CORRECT foF2 calculation methods
that match the original scripts exactly, ensuring data consistency.

Saves to ~/Desktop/test/test2/corrected/

Author: Research Team
License: MIT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import sys

# Configuration
NVIS_DATA_FILE = "data/NVIS_data.xlsx"

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

def calculate_fof2_from_signal_correct(signal_values, station="Guam", period="April"):
    """
    Calculate foF2 using the EXACT same methods as original scripts
    """
    fof2_values = []
    
    # Station and period specific parameters (matching original scripts exactly)
    if "Guam" in station:
        if "15th" in period:
            baseline_fof2 = 11.0  # From guam_april15_fof2_7years.py
            scale_factor = 10.0
        elif "15-28" in period:
            baseline_fof2 = 11.2  # From guam_april15-28_fof2_7years.py
            scale_factor = 10.0
        else:  # Full April
            baseline_fof2 = 11.0  # From guam_fof2_april.py
            scale_factor = 10.0
        min_fof2, max_fof2 = 4.0, 18.0
    else:  # Darwin
        if "15-28" in period:
            baseline_fof2 = 9.2   # From darwin_april15-28_fof2_7years.py
            scale_factor = 12.0
        elif "15th" in period:
            baseline_fof2 = 9.0   # From darwin_april15_fof2_7years.py
            scale_factor = 10.0
        else:  # Full April
            baseline_fof2 = 8.5   # From darwin_fof2_april.py
            scale_factor = 10.0
        min_fof2, max_fof2 = 3.0, 15.0
    
    for signal in signal_values:
        if pd.notna(signal):
            # Use EXACT original calculation method
            signal_factor = signal / scale_factor
            estimated_fof2 = baseline_fof2 + signal_factor
            
            # Clamp to reasonable foF2 range
            estimated_fof2 = np.clip(estimated_fof2, min_fof2, max_fof2)
            fof2_values.append(estimated_fof2)
    
    return fof2_values

def create_corrected_chart(station_name, period_name, year_range):
    """Create standardized 2x2 chart with corrected foF2 calculations"""
    
    fig, axes = plt.subplots(2, 2, figsize=STANDARD_LAYOUT['figure_size'])
    
    # Standardized main title with proper spacing
    main_title = f'Ionospheric foF2 Critical Frequency Analysis\n{station_name} Station - {period_name} ({year_range})'
    fig.suptitle(main_title,
                fontsize=STANDARD_LAYOUT['title_fontsize'],
                fontweight='bold',
                y=0.98)
    
    return fig, axes

def plot_corrected_hourly_patterns(ax, df, year_columns, colors, station, period):
    """Plot hourly patterns with correct foF2 calculations"""
    
    # Add day/night shading
    ax.axvspan(6, 18, alpha=0.15, color='yellow', label='Daylight')
    ax.axvspan(18, 24, alpha=0.15, color='gray', label='Night')
    ax.axvspan(0, 6, alpha=0.15, color='gray')
    
    # Plot hourly data for each year
    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year]).copy()
        df_year['Hour'] = df_year['DateTime'].dt.hour
        df_year['foF2_estimated'] = calculate_fof2_from_signal_correct(df_year[year], station, period)
        hourly_fof2 = df_year.groupby('Hour')['foF2_estimated'].mean()
        
        ax.plot(hourly_fof2.index, hourly_fof2.values,
                color=colors[i % len(colors)], marker='o', linewidth=2, markersize=4,
                label=f'{int(year)}')
    
    # Formatting
    ax.set_title("Hourly Patterns (24h Diurnal Cycle)",
                fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel('Hour of Day (UTC)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_ylabel('Average foF2 (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.legend(loc='upper right', fontsize=STANDARD_LAYOUT['legend_fontsize'])
    ax.grid(True, alpha=STANDARD_LAYOUT['grid_alpha'])
    ax.set_xlim(0, 23)
    ax.set_xticks(range(0, 24, 6))

def plot_corrected_statistical_distribution(ax, df, year_columns, colors, station, period):
    """Plot statistical distribution with correct foF2 calculations"""
    
    fof2_data = []
    year_labels = []
    
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calculate_fof2_from_signal_correct(df_year[year], station, period)
        fof2_data.append(fof2_values)
        year_labels.append(f'{int(year)}')
    
    # Create box plots
    bp = ax.boxplot(fof2_data, tick_labels=year_labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Formatting
    ax.set_title("foF2 Distribution by Year",
                fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel('Year', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_ylabel('foF2 (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.grid(True, alpha=STANDARD_LAYOUT['grid_alpha'])

def plot_corrected_temporal_progression(ax, df, year_columns, colors, station, period, period_type="daily"):
    """Plot temporal progression with correct foF2 calculations"""
    
    if period_type == "single_day":
        # 24-hour progression for single day analysis
        title = "24-hour foF2 Progression"
        xlabel = "Hour of Day"
        
        for i, year in enumerate(year_columns):
            df_year = df.dropna(subset=[year]).copy()
            df_year['Hour'] = df_year['DateTime'].dt.hour
            df_year['Minute'] = df_year['DateTime'].dt.minute
            df_year['HourDecimal'] = df_year['Hour'] + df_year['Minute'] / 60.0
            df_year['foF2_estimated'] = calculate_fof2_from_signal_correct(df_year[year], station, period)
            df_year = df_year.sort_values('HourDecimal')
            
            ax.plot(df_year['HourDecimal'], df_year['foF2_estimated'],
                    color=colors[i % len(colors)], marker='o', linewidth=2, markersize=3,
                    label=f'{int(year)}')
    
    elif period_type == "daily":
        # Daily progression for period analysis
        title = "Daily Average foF2 Progression"
        xlabel = "Day of Period"
        
        for i, year in enumerate(year_columns):
            df_year = df.dropna(subset=[year]).copy()
            df_year['Day'] = df_year['DateTime'].dt.day
            df_year['foF2_estimated'] = calculate_fof2_from_signal_correct(df_year[year], station, period)
            daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()
            
            ax.plot(daily_fof2.index, daily_fof2.values,
                    color=colors[i % len(colors)], marker='o', linewidth=2, markersize=4,
                    label=f'{int(year)}')
    
    else:  # monthly
        # Monthly progression for full month analysis
        title = "Daily Average foF2 Progression (Full Month)"
        xlabel = "Day of April"
        
        for i, year in enumerate(year_columns):
            df_year = df.dropna(subset=[year]).copy()
            df_year['Day'] = df_year['DateTime'].dt.day
            df_year['foF2_estimated'] = calculate_fof2_from_signal_correct(df_year[year], station, period)
            daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()
            
            ax.plot(daily_fof2.index, daily_fof2.values,
                    color=colors[i % len(colors)], marker='o', linewidth=2, markersize=4,
                    label=f'{int(year)}')
    
    # Formatting
    ax.set_title(title, fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_ylabel('foF2 (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.legend(loc='upper right', fontsize=STANDARD_LAYOUT['legend_fontsize'])
    ax.grid(True, alpha=STANDARD_LAYOUT['grid_alpha'])

def plot_corrected_nvis_frequency_bands(ax, df, year_columns, station, period):
    """Plot NVIS frequency bands with correct foF2 calculations"""
    
    # Calculate average foF2 across all years and data
    all_fof2_values = []
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calculate_fof2_from_signal_correct(df_year[year], station, period)
        all_fof2_values.extend(fof2_values)
    
    if all_fof2_values:
        avg_fof2 = np.mean(all_fof2_values)
        std_fof2 = np.std(all_fof2_values)
        muf = avg_fof2 * 3.0  # Maximum Usable Frequency
    else:
        avg_fof2, std_fof2, muf = 10.0, 2.0, 30.0
    
    # DGFC frequencies
    dgfc_frequencies = [5.0, 7.078, 10.130]
    
    # Plot frequency bands
    ax.axhspan(0, avg_fof2, alpha=0.3, color='green', label=f'Below foF2 ({avg_fof2:.1f} MHz)')
    ax.axhspan(avg_fof2, muf, alpha=0.3, color='gray', label=f'NVIS Range ({avg_fof2:.1f}-{muf:.1f} MHz)')
    ax.axhspan(muf, max(25, muf + 5), alpha=0.3, color='red', label=f'Above MUF (>{muf:.1f} MHz)')
    
    # Mark DGFC frequencies
    for freq in dgfc_frequencies:
        ax.axhline(y=freq, color='blue', linestyle='--', linewidth=2, alpha=0.8)
        ax.text(0.02, freq + 0.5, f'DGFC: {freq} MHz', fontsize=10, color='blue', fontweight='bold')
    
    # Formatting
    ax.set_title("NVIS Frequency Bands vs DGFC",
                fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_ylabel('Frequency (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_xlabel('NVIS Frequency Bands', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.legend(loc='upper right', fontsize=STANDARD_LAYOUT['legend_fontsize'])
    ax.grid(True, alpha=STANDARD_LAYOUT['grid_alpha'])
    ax.set_ylim(0, max(25, muf + 5))
    ax.set_xticks([])

def load_station_data(station_name, period_filter="April 15-28"):
    """Load data for specific station with period filtering"""
    
    print(f"📊 Loading {station_name} data for {period_filter}...")
    
    if not os.path.exists(NVIS_DATA_FILE):
        print("⚠️ NVIS data file not found")
        return None
    
    try:
        # Load real data
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name=station_name, header=None)
        
        # Find header row
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            raise Exception("Header row not found")
        
        # Read with proper header
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name=station_name, header=header_row)
        df = df.dropna(how='all')
        
        # Create DateTime column
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Apply period filtering
        if "15th" in period_filter:
            df = df[(df['DateTime'].dt.month == 4) & (df['DateTime'].dt.day == 15)]
        elif "15-28" in period_filter:
            df = df[(df['DateTime'].dt.month == 4) & 
                    (df['DateTime'].dt.day >= 15) & 
                    (df['DateTime'].dt.day <= 28)]
        else:  # Full April
            df = df[df['DateTime'].dt.month == 4]
        
        # Find year columns
        year_columns = []
        for col in df.columns:
            if str(col).isdigit() and 2017 <= int(col) <= 2023:
                year_columns.append(int(col))
        
        print(f"✅ Loaded {station_name} {period_filter} data: {len(df)} records, years: {year_columns}")
        
        return {
            'data': df,
            'year_columns': year_columns,
            'source': 'real'
        }
        
    except Exception as e:
        print(f"⚠️ Error loading {station_name} data: {e}")
        return None

def main():
    """Generate corrected charts with proper foF2 calculations"""
    
    print("🔧 CORRECTED CHART GENERATOR")
    print("="*35)
    print("This generates charts with the CORRECT foF2 calculations")
    print("that match the original scripts exactly.")
    print("Saves to ~/Desktop/test/test2/corrected/")
    print()
    
    # Create corrected folder
    corrected_folder = "output/corrected"
    if not os.path.exists(corrected_folder):
        os.makedirs(corrected_folder)
        print(f"📁 Created corrected folder: {corrected_folder}")
    
    # Chart configurations with correct period names - ALL 6 CHARTS
    chart_configs = [
        {
            'station': 'Guam',
            'period': 'April 15-28',
            'period_type': 'daily',
            'filename': 'Guam_April_15_28_CORRECTED'
        },
        {
            'station': 'Guam',
            'period': 'April 15th',
            'period_type': 'single_day',
            'filename': 'Guam_April_15th_CORRECTED'
        },
        {
            'station': 'Guam',
            'period': 'Full April',
            'period_type': 'monthly',
            'filename': 'Guam_Full_April_CORRECTED'
        },
        {
            'station': 'Darwin',
            'period': 'April 15-28',
            'period_type': 'daily',
            'filename': 'Darwin_April_15_28_CORRECTED'
        },
        {
            'station': 'Darwin',
            'period': 'April 15th',
            'period_type': 'single_day',
            'filename': 'Darwin_April_15th_CORRECTED'
        },
        {
            'station': 'Darwin',
            'period': 'Full April',
            'period_type': 'monthly',
            'filename': 'Darwin_Full_April_CORRECTED'
        }
    ]

    # Generate each chart
    for i, config in enumerate(chart_configs, 1):
        print(f"\n[{i}/6] {config['station']} - {config['period']}")
        
        # Load data
        data = load_station_data(config['station'], config['period'])
        if not data:
            print(f"❌ Failed to load data for {config['station']} {config['period']}")
            continue
        
        df = data['data']
        year_columns = data['year_columns']
        colors = STANDARD_LAYOUT['colors']
        
        # Create chart
        fig, axes = create_corrected_chart(config['station'], config['period'], "2017-2023")
        
        # Plot each panel with correct calculations
        plot_corrected_hourly_patterns(axes[0, 0], df, year_columns, colors, config['station'], config['period'])
        plot_corrected_statistical_distribution(axes[0, 1], df, year_columns, colors, config['station'], config['period'])
        plot_corrected_temporal_progression(axes[1, 0], df, year_columns, colors, config['station'], config['period'], config['period_type'])
        plot_corrected_nvis_frequency_bands(axes[1, 1], df, year_columns, config['station'], config['period'])
        
        # Apply layout and save
        plt.tight_layout()
        plt.subplots_adjust(top=0.88, hspace=0.4, wspace=0.3)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"new_standard_{config['filename']}_{timestamp}.png"
        full_path = os.path.join(corrected_folder, filename)
        
        plt.savefig(full_path, dpi=160, bbox_inches='tight')
        print(f"✅ Saved corrected chart: {filename}")
        
        plt.close()
    
    print(f"\n🎉 ALL 6 CORRECTED CHARTS GENERATED!")
    print("="*40)
    print(f"📁 Location: {corrected_folder}")
    print("🔧 These charts use the EXACT same foF2 calculations as the original scripts")
    print("📊 Data should now match the original individual charts perfectly")

    # Check results
    png_files = [f for f in os.listdir(corrected_folder) if f.endswith('.png')]
    print(f"\n📊 Generated {len(png_files)} corrected charts:")
    for file in sorted(png_files):
        file_path = os.path.join(corrected_folder, file)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        print(f"  • {file} ({file_size:.1f} MB)")

if __name__ == "__main__":
    main()
