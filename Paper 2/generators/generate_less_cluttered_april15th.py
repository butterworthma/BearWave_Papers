#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Less Cluttered April 15th Charts
=========================================

Creates Guam and Darwin April 15th charts with less cluttered 24-hour
foF2 progression while keeping other plots the same.
Saves to ~/Desktop/test/test2/

Author: Research Team
License: MIT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import sys

# Import the standardized layout enforcer
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from standardized_layout_enforcer import *

# Configuration
NVIS_DATA_FILE = "data/NVIS_data.xlsx"

def plot_less_cluttered_temporal_progression(ax, df, year_columns, colors, title="24-hour foF2 Progression"):
    """
    POSITION: Bottom-Left (1,0) - Less cluttered 24-hour progression for April 15th
    
    Options for less cluttered display:
    1. Show only every other year
    2. Use different line styles
    3. Show hourly averages instead of all data points
    4. Use transparency
    """
    
    ax.set_title(title, fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel('Hour of Day', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_ylabel('foF2 (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.grid(True, alpha=STANDARD_LAYOUT['grid_alpha'])
    
    # Option 1: Show only selected years to reduce clutter
    selected_years = [year_columns[0], year_columns[2], year_columns[4], year_columns[6]]  # Every other year
    line_styles = ['-', '--', '-.', ':']
    
    for i, year in enumerate(selected_years):
        if year in year_columns:
            df_year = df.dropna(subset=[year]).copy()
            df_year['Hour'] = df_year['DateTime'].dt.hour
            df_year['Minute'] = df_year['DateTime'].dt.minute
            df_year['HourDecimal'] = df_year['Hour'] + df_year['Minute'] / 60.0
            df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
            
            # Group by hour and take mean to reduce data points
            hourly_data = df_year.groupby('Hour')['foF2_estimated'].agg(['mean', 'std']).reset_index()
            
            # Plot with error bars for variability
            ax.errorbar(hourly_data['Hour'], hourly_data['mean'], 
                       yerr=hourly_data['std'], 
                       color=colors[year_columns.index(year) % len(colors)], 
                       linestyle=line_styles[i % len(line_styles)],
                       linewidth=2.5, 
                       marker='o', 
                       markersize=5,
                       capsize=3,
                       alpha=0.8,
                       label=f'{int(year)}')
    
    ax.set_xlim(0, 23)
    ax.set_xticks(range(0, 24, 3))
    ax.legend(loc='upper right', fontsize=STANDARD_LAYOUT['legend_fontsize'])
    
    # Add annotation about data reduction
    ax.text(0.02, 0.98, 'Hourly averages ± std\nSelected years shown', 
            transform=ax.transAxes, fontsize=8, 
            verticalalignment='top', alpha=0.7,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

def plot_alternative_temporal_progression(ax, df, year_columns, colors, title="24-hour foF2 Progression"):
    """
    Alternative approach: Heat map style visualization
    """
    
    ax.set_title(title, fontsize=STANDARD_LAYOUT['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel('Hour of Day', fontsize=STANDARD_LAYOUT['label_fontsize'])
    ax.set_ylabel('Year', fontsize=STANDARD_LAYOUT['label_fontsize'])
    
    # Create matrix for heatmap
    hours = range(24)
    heat_data = []
    
    for year in year_columns:
        df_year = df.dropna(subset=[year]).copy()
        df_year['Hour'] = df_year['DateTime'].dt.hour
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
        hourly_avg = df_year.groupby('Hour')['foF2_estimated'].mean()
        
        # Fill missing hours with NaN
        year_data = []
        for hour in hours:
            if hour in hourly_avg.index:
                year_data.append(hourly_avg[hour])
            else:
                year_data.append(np.nan)
        heat_data.append(year_data)
    
    # Create heatmap
    im = ax.imshow(heat_data, cmap='viridis', aspect='auto', interpolation='nearest')
    
    # Set ticks and labels
    ax.set_xticks(range(0, 24, 3))
    ax.set_xticklabels(range(0, 24, 3))
    ax.set_yticks(range(len(year_columns)))
    ax.set_yticklabels([str(int(year)) for year in year_columns])
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('foF2 (MHz)', fontsize=STANDARD_LAYOUT['label_fontsize'])

def load_station_data(station_name):
    """Load data for specific station"""
    
    print(f"📊 Loading {station_name} data...")
    
    if not os.path.exists(NVIS_DATA_FILE):
        print("⚠️ NVIS data file not found, creating synthetic data...")
        return create_synthetic_data()
    
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
        
        # Filter for April 15th only
        df = df[(df['DateTime'].dt.month == 4) & (df['DateTime'].dt.day == 15)]
        
        # Find year columns
        year_columns = []
        for col in df.columns:
            if str(col).isdigit() and 2017 <= int(col) <= 2023:
                year_columns.append(int(col))
        
        print(f"✅ Loaded {station_name} April 15th data: {len(df)} records, years: {year_columns}")
        
        return {
            'data': df,
            'year_columns': year_columns,
            'source': 'real'
        }
        
    except Exception as e:
        print(f"⚠️ Error loading {station_name} data: {e}")
        return create_synthetic_data()

def create_synthetic_data():
    """Create synthetic data for testing"""
    
    # Create 24 hours of data for April 15th
    dates = pd.date_range('2017-04-15 00:00', '2017-04-15 23:45', freq='15min')
    data = {
        'DateTime': dates,
        '2017': np.random.normal(-5, 3, len(dates)),
        '2018': np.random.normal(-4, 2.5, len(dates)),
        '2019': np.random.normal(-6, 3.5, len(dates)),
        '2020': np.random.normal(-3, 2, len(dates)),
        '2021': np.random.normal(-5.5, 3, len(dates)),
        '2022': np.random.normal(-4.5, 2.8, len(dates)),
        '2023': np.random.normal(-5.2, 3.2, len(dates))
    }
    
    df = pd.DataFrame(data)
    year_columns = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    
    return {
        'data': df,
        'year_columns': year_columns,
        'source': 'synthetic'
    }

def create_less_cluttered_april15th_chart(station_name, data, visualization_type="reduced_lines"):
    """Create April 15th chart with less cluttered temporal progression"""
    
    print(f"📈 Creating {station_name} April 15th chart (less cluttered)...")
    
    df = data['data']
    year_columns = data['year_columns']
    colors = STANDARD_LAYOUT['colors']
    
    # Create standardized chart
    fig, axes = create_standardized_chart(station_name, "April 15th", "2017-2023")
    
    # Plot standard panels (unchanged)
    plot_hourly_patterns(axes[0, 0], df, year_columns, colors)
    plot_statistical_distribution(axes[0, 1], df, year_columns, colors)
    plot_nvis_frequency_bands(axes[1, 1], df, year_columns)
    
    # Plot less cluttered temporal progression
    if visualization_type == "heatmap":
        plot_alternative_temporal_progression(axes[1, 0], df, year_columns, colors, 
                                            "24-hour foF2 Heatmap")
    else:
        plot_less_cluttered_temporal_progression(axes[1, 0], df, year_columns, colors,
                                                "24-hour foF2 Progression (Reduced)")
    
    # Apply standardized layout
    apply_standardized_layout(fig)
    
    # Save to test2 folder
    test2_folder = "output"
    if not os.path.exists(test2_folder):
        os.makedirs(test2_folder)
        print(f"📁 Created test2 folder: {test2_folder}")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    viz_suffix = "Heatmap" if visualization_type == "heatmap" else "Reduced"
    filename = f"new_standard_{station_name}_April_15th_{viz_suffix}_{timestamp}.png"
    full_path = os.path.join(test2_folder, filename)
    
    plt.savefig(full_path, dpi=160, bbox_inches='tight')
    print(f"✅ Saved to test2 folder: {filename}")
    print(f"📁 Full path: {full_path}")
    
    plt.close()

def main():
    """Main function"""
    
    print("🖥️ LESS CLUTTERED APRIL 15TH CHART GENERATOR")
    print("="*50)
    print("Creates Guam and Darwin April 15th charts with")
    print("less cluttered 24-hour foF2 progression.")
    print("Saves to ~/Desktop/test/test2/")
    print()
    print("Visualization options:")
    print("1. Reduced lines (every other year + error bars)")
    print("2. Heatmap (year vs hour color map)")
    print()
    
    choice = input("Select visualization (1-2, default 1): ").strip()
    viz_type = "heatmap" if choice == "2" else "reduced_lines"
    
    print(f"\n🎯 GENERATING LESS CLUTTERED APRIL 15TH CHARTS")
    print("="*55)
    
    # Load data for both stations
    guam_data = load_station_data("Guam")
    darwin_data = load_station_data("Darwin")
    
    # Generate charts
    print(f"\n[1/2] Guam April 15th")
    create_less_cluttered_april15th_chart("Guam", guam_data, viz_type)
    
    print(f"\n[2/2] Darwin April 15th")
    create_less_cluttered_april15th_chart("Darwin", darwin_data, viz_type)
    
    print(f"\n🎉 LESS CLUTTERED CHARTS GENERATED!")
    print("="*45)
    
    # Check results
    test2_folder = "output"
    if os.path.exists(test2_folder):
        png_files = [f for f in os.listdir(test2_folder) if f.endswith('.png')]
        print(f"📊 Found {len(png_files)} charts in test2 folder:")
        
        for file in sorted(png_files):
            file_path = os.path.join(test2_folder, file)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"  • {file} ({file_size:.1f} MB)")
        
        print(f"\n📁 Charts saved to: {test2_folder}")
        print(f"🖼️ To view: open {test2_folder}")
        
        print(f"\n🎯 CHANGES MADE:")
        if viz_type == "heatmap":
            print("  • Bottom-Left: 24-hour heatmap (year vs hour)")
            print("  • Color intensity shows foF2 values")
            print("  • Eliminates line clutter completely")
        else:
            print("  • Bottom-Left: Reduced to every other year")
            print("  • Added error bars for variability")
            print("  • Hourly averages instead of all points")
            print("  • Improved transparency and line styles")
        
        print("  • Other 3 panels unchanged (consistent layout)")

if __name__ == "__main__":
    main()
