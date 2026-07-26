#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Six Standardized Charts to Desktop/test Folder
=======================================================

Creates exactly 6 standardized foF2 analysis charts using the
standardized layout enforcer and saves them all to ~/Desktop/test/

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

def load_guam_data():
    """Load Guam data for chart generation"""
    
    print("📊 Loading Guam data...")
    
    if not os.path.exists(NVIS_DATA_FILE):
        print("⚠️ NVIS data file not found, creating synthetic data...")
        return create_synthetic_data()
    
    try:
        # Load real Guam data
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=None)
        
        # Find header row
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            raise Exception("Header row not found")
        
        # Read with proper header
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=header_row)
        df = df.dropna(how='all')
        
        # Create DateTime column
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for April 15-28
        df = df[(df['DateTime'].dt.month == 4) & 
                (df['DateTime'].dt.day >= 15) & 
                (df['DateTime'].dt.day <= 28)]
        
        # Find year columns
        year_columns = []
        for col in df.columns:
            if str(col).isdigit() and 2017 <= int(col) <= 2023:
                year_columns.append(int(col))
        
        print(f"✅ Loaded Guam data: {len(df)} records, years: {year_columns}")
        
        return {
            'data': df,
            'year_columns': year_columns,
            'source': 'real'
        }
        
    except Exception as e:
        print(f"⚠️ Error loading Guam data: {e}")
        return create_synthetic_data()

def load_darwin_data():
    """Load Darwin data for chart generation"""
    
    print("📊 Loading Darwin data...")
    
    if not os.path.exists(NVIS_DATA_FILE):
        print("⚠️ NVIS data file not found, creating synthetic data...")
        return create_synthetic_data()
    
    try:
        # Load real Darwin data
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=None)
        
        # Find header row
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            raise Exception("Header row not found")
        
        # Read with proper header
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=header_row)
        df = df.dropna(how='all')
        
        # Create DateTime column
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for April 15-28
        df = df[(df['DateTime'].dt.month == 4) & 
                (df['DateTime'].dt.day >= 15) & 
                (df['DateTime'].dt.day <= 28)]
        
        # Find year columns
        year_columns = []
        for col in df.columns:
            if str(col).isdigit() and 2017 <= int(col) <= 2023:
                year_columns.append(int(col))
        
        print(f"✅ Loaded Darwin data: {len(df)} records, years: {year_columns}")
        
        return {
            'data': df,
            'year_columns': year_columns,
            'source': 'real'
        }
        
    except Exception as e:
        print(f"⚠️ Error loading Darwin data: {e}")
        return create_synthetic_data()

def create_synthetic_data():
    """Create synthetic data for testing"""
    
    dates = pd.date_range('2017-04-15', '2017-04-28', freq='15min')
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

def create_standardized_chart_with_data(station, period, data, filename):
    """Create a standardized chart with specific data"""
    
    print(f"📈 Creating {station} {period} chart...")
    
    df = data['data']
    year_columns = data['year_columns']
    colors = STANDARD_LAYOUT['colors']
    
    # Create standardized chart
    fig, axes = create_standardized_chart(station, period, "2017-2023")
    
    # Plot each panel using standardized functions
    plot_hourly_patterns(axes[0, 0], df, year_columns, colors)
    plot_statistical_distribution(axes[0, 1], df, year_columns, colors)
    
    # Determine period type for temporal progression
    if "15th" in period:
        period_type = "single_day"
    elif "15-28" in period:
        period_type = "daily"
    else:
        period_type = "monthly"
    
    plot_temporal_progression(axes[1, 0], df, year_columns, colors, period_type=period_type)
    plot_nvis_frequency_bands(axes[1, 1], df, year_columns)
    
    # Apply standardized layout
    apply_standardized_layout(fig)
    
    # Save to test folder
    save_standardized_chart(fig, filename)
    
    plt.close()

def generate_all_six_charts():
    """Generate all 6 standardized charts"""
    
    print("🎯 GENERATING ALL 6 STANDARDIZED CHARTS")
    print("="*45)
    print("Creating standardized 2x2 charts for all analyses")
    print("and saving them to ~/Desktop/test/ folder.")
    print()
    
    # Create test folder if it doesn't exist
    test_folder = "output"
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
        print(f"📁 Created test folder: {test_folder}")
    else:
        print(f"📁 Using existing test folder: {test_folder}")
    
    # Load data
    guam_data = load_guam_data()
    darwin_data = load_darwin_data()
    
    # Chart configurations
    chart_configs = [
        {
            'station': 'Guam',
            'period': 'April 15-28',
            'data': guam_data,
            'filename': 'Guam_April_15_28_Analysis'
        },
        {
            'station': 'Guam',
            'period': 'April 15th',
            'data': guam_data,
            'filename': 'Guam_April_15th_Analysis'
        },
        {
            'station': 'Guam',
            'period': 'Full April',
            'data': guam_data,
            'filename': 'Guam_Full_April_Analysis'
        },
        {
            'station': 'Darwin',
            'period': 'April 15-28',
            'data': darwin_data,
            'filename': 'Darwin_April_15_28_Analysis'
        },
        {
            'station': 'Darwin',
            'period': 'April 15th',
            'data': darwin_data,
            'filename': 'Darwin_April_15th_Analysis'
        },
        {
            'station': 'Darwin',
            'period': 'Full April',
            'data': darwin_data,
            'filename': 'Darwin_Full_April_Analysis'
        }
    ]
    
    # Generate each chart
    for i, config in enumerate(chart_configs, 1):
        print(f"\n[{i}/6] {config['station']} - {config['period']}")
        create_standardized_chart_with_data(
            config['station'],
            config['period'],
            config['data'],
            config['filename']
        )
    
    print(f"\n🎉 ALL 6 STANDARDIZED CHARTS GENERATED!")
    print("="*45)
    
    # Check results
    png_files = [f for f in os.listdir(test_folder) if f.endswith('.png') and f.startswith('new_standard_')]
    print(f"📊 Found {len(png_files)} charts in test folder:")
    
    for file in sorted(png_files):
        file_path = os.path.join(test_folder, file)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        print(f"  • {file} ({file_size:.1f} MB)")
    
    print(f"\n📁 All charts saved to: {test_folder}")
    print(f"🖼️ To view: open {test_folder}")
    
    print(f"\n🎯 STANDARDIZED LAYOUT FEATURES:")
    print("  • Top-Left: Hourly Patterns (24h diurnal cycle)")
    print("  • Top-Right: Statistical Distribution (box plots)")
    print("  • Bottom-Left: Temporal Progression (period-specific)")
    print("  • Bottom-Right: NVIS Frequency Bands")
    print("  • Fixed title spacing (no overlapping)")
    print("  • Consistent colors and formatting")

def main():
    """Main function"""
    
    print("🖥️ SIX STANDARDIZED CHART GENERATOR")
    print("="*40)
    print("This will generate exactly 6 standardized foF2 charts")
    print("with consistent 2x2 layout and save them to Desktop/test")
    print()
    
    response = input("Generate all 6 charts? (Y/n): ").strip().lower()
    
    if response in ['', 'y', 'yes']:
        generate_all_six_charts()
    else:
        print("❌ Chart generation cancelled")

if __name__ == "__main__":
    main()
