#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2x2 Chart Generator for Complete NVIS Data
==========================================

Generates 2x2 comparison charts using the complete NVIS dataset
from "Complete (version 1).xlsx" for comprehensive ionospheric analysis.

Author: Research Team
License: MIT
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

# Configuration
DATA_FILE = 'data/Complete_NVIS_data.xlsx'
OUTPUT_DIR = 'output'

def load_complete_data():
    """Load complete NVIS data from both Guam and Darwin sheets"""
    print(f"📊 Loading complete NVIS data from {DATA_FILE}...")
    
    try:
        # Load both sheets
        guam_df = pd.read_excel(DATA_FILE, sheet_name='Guam')
        darwin_df = pd.read_excel(DATA_FILE, sheet_name='Darwin')
        
        print(f"✅ Loaded Guam: {guam_df.shape}, Darwin: {darwin_df.shape}")
        
        # Find the header row (where DATE and TIME appear)
        guam_header_row = None
        for i in range(20):  # Check first 20 rows
            if 'DATE' in str(guam_df.iloc[i, 0]) and 'TIME' in str(guam_df.iloc[i, 1]):
                guam_header_row = i
                break
        
        darwin_header_row = None
        for i in range(20):  # Check first 20 rows
            if 'DATE' in str(darwin_df.iloc[i, 0]) and 'TIME' in str(darwin_df.iloc[i, 1]):
                darwin_header_row = i
                break
        
        if guam_header_row is not None:
            print(f"📋 Found Guam headers at row {guam_header_row}")
            # Re-load with correct header
            guam_df = pd.read_excel(DATA_FILE, sheet_name='Guam', header=guam_header_row)
        
        if darwin_header_row is not None:
            print(f"📋 Found Darwin headers at row {darwin_header_row}")
            # Re-load with correct header
            darwin_df = pd.read_excel(DATA_FILE, sheet_name='Darwin', header=darwin_header_row)
        
        return guam_df, darwin_df
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

def clean_and_process_data(df, station_name):
    """Clean and process ionospheric data"""
    print(f"🔧 Processing {station_name} data...")
    
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    # Find year columns (numeric columns that look like years)
    year_columns = []
    for col in df.columns:
        if isinstance(col, (int, float)) and 2010 <= col <= 2030:
            year_columns.append(col)
        elif isinstance(col, str) and col.replace('.', '').isdigit():
            year = float(col)
            if 2010 <= year <= 2030:
                year_columns.append(col)
    
    print(f"📅 Found year columns: {year_columns}")
    
    # Create processed data structure
    processed_data = []
    
    for idx, row in df.iterrows():
        try:
            date_str = str(row.iloc[0])  # DATE column
            time_str = str(row.iloc[1])  # TIME column
            
            # Skip header rows and invalid data
            if 'DATE' in date_str or pd.isna(row.iloc[0]):
                continue
            
            # Process each year's data
            for year_col in year_columns:
                if year_col in df.columns:
                    fof2_value = row[year_col]
                    if pd.notna(fof2_value) and isinstance(fof2_value, (int, float)):
                        processed_data.append({
                            'Date': date_str,
                            'Time': time_str,
                            'Year': int(float(str(year_col))),
                            'foF2': float(fof2_value),
                            'Station': station_name
                        })
        except Exception as e:
            continue
    
    result_df = pd.DataFrame(processed_data)
    print(f"✅ Processed {len(result_df)} records for {station_name}")
    
    return result_df

def generate_2x2_comparison_chart(guam_data, darwin_data):
    """Generate 2x2 comparison chart"""
    print("📊 Generating 2x2 comparison chart...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Chart 1: Guam foF2 by Year
    if not guam_data.empty:
        guam_yearly = guam_data.groupby('Year')['foF2'].agg(['mean', 'std', 'count']).reset_index()
        ax1.errorbar(guam_yearly['Year'], guam_yearly['mean'], yerr=guam_yearly['std'], 
                    marker='o', capsize=5, capthick=2, linewidth=2, color='blue')
        ax1.set_title('Guam - Annual foF2 Trends', fontweight='bold', fontsize=12)
        ax1.set_xlabel('Year')
        ax1.set_ylabel('foF2 (MHz)')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(bottom=0)
    
    # Chart 2: Darwin foF2 by Year
    if not darwin_data.empty:
        darwin_yearly = darwin_data.groupby('Year')['foF2'].agg(['mean', 'std', 'count']).reset_index()
        ax2.errorbar(darwin_yearly['Year'], darwin_yearly['mean'], yerr=darwin_yearly['std'], 
                    marker='s', capsize=5, capthick=2, linewidth=2, color='red')
        ax2.set_title('Darwin - Annual foF2 Trends', fontweight='bold', fontsize=12)
        ax2.set_xlabel('Year')
        ax2.set_ylabel('foF2 (MHz)')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(bottom=0)
    
    # Chart 3: Station Comparison
    if not guam_data.empty and not darwin_data.empty:
        combined_yearly = pd.concat([
            guam_data.groupby('Year')['foF2'].mean().reset_index().assign(Station='Guam'),
            darwin_data.groupby('Year')['foF2'].mean().reset_index().assign(Station='Darwin')
        ])
        
        for station, group in combined_yearly.groupby('Station'):
            color = 'blue' if station == 'Guam' else 'red'
            marker = 'o' if station == 'Guam' else 's'
            ax3.plot(group['Year'], group['foF2'], marker=marker, linewidth=2, 
                    color=color, label=station, markersize=6)
        
        ax3.set_title('Guam vs Darwin - foF2 Comparison', fontweight='bold', fontsize=12)
        ax3.set_xlabel('Year')
        ax3.set_ylabel('foF2 (MHz)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(bottom=0)
    
    # Chart 4: Distribution Analysis
    if not guam_data.empty and not darwin_data.empty:
        ax4.hist(guam_data['foF2'], bins=30, alpha=0.6, color='blue', label='Guam', density=True)
        ax4.hist(darwin_data['foF2'], bins=30, alpha=0.6, color='red', label='Darwin', density=True)
        
        # Add statistics
        guam_mean = guam_data['foF2'].mean()
        darwin_mean = darwin_data['foF2'].mean()
        ax4.axvline(guam_mean, color='blue', linestyle='--', linewidth=2, 
                   label=f'Guam Mean: {guam_mean:.1f} MHz')
        ax4.axvline(darwin_mean, color='red', linestyle='--', linewidth=2,
                   label=f'Darwin Mean: {darwin_mean:.1f} MHz')
        
        ax4.set_title('foF2 Distribution Comparison', fontweight='bold', fontsize=12)
        ax4.set_xlabel('foF2 (MHz)')
        ax4.set_ylabel('Density')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Complete NVIS Data Analysis - 2x2 Comparison\n'
                 f'Guam: {len(guam_data)} records | Darwin: {len(darwin_data)} records', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # Save
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'Complete_NVIS_2x2_Comparison_{timestamp}.png'
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    
    return guam_yearly if not guam_data.empty else None, darwin_yearly if not darwin_data.empty else None

def generate_detailed_analysis(guam_data, darwin_data):
    """Generate detailed statistical analysis"""
    print("📊 Generating detailed analysis...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Monthly analysis for Guam
    if not guam_data.empty:
        # Try to extract month information
        guam_data['Month'] = pd.to_datetime(guam_data['Date'], errors='coerce').dt.month
        monthly_guam = guam_data.groupby('Month')['foF2'].agg(['mean', 'std']).reset_index()
        
        ax1.errorbar(monthly_guam['Month'], monthly_guam['mean'], yerr=monthly_guam['std'],
                    marker='o', capsize=5, color='blue', linewidth=2)
        ax1.set_title('Guam - Monthly foF2 Variation', fontweight='bold')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('foF2 (MHz)')
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(range(1, 13))
    
    # Monthly analysis for Darwin
    if not darwin_data.empty:
        darwin_data['Month'] = pd.to_datetime(darwin_data['Date'], errors='coerce').dt.month
        monthly_darwin = darwin_data.groupby('Month')['foF2'].agg(['mean', 'std']).reset_index()
        
        ax2.errorbar(monthly_darwin['Month'], monthly_darwin['mean'], yerr=monthly_darwin['std'],
                    marker='s', capsize=5, color='red', linewidth=2)
        ax2.set_title('Darwin - Monthly foF2 Variation', fontweight='bold')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('foF2 (MHz)')
        ax2.grid(True, alpha=0.3)
        ax2.set_xticks(range(1, 13))
    
    # Box plot comparison
    if not guam_data.empty and not darwin_data.empty:
        combined_data = [guam_data['foF2'].dropna(), darwin_data['foF2'].dropna()]
        ax3.boxplot(combined_data, labels=['Guam', 'Darwin'], patch_artist=True,
                   boxprops=dict(facecolor='lightblue', alpha=0.7),
                   medianprops=dict(color='red', linewidth=2))
        ax3.set_title('foF2 Distribution Box Plot', fontweight='bold')
        ax3.set_ylabel('foF2 (MHz)')
        ax3.grid(True, alpha=0.3)
    
    # Correlation analysis
    if not guam_data.empty and not darwin_data.empty:
        # Merge data by year for correlation
        guam_yearly_mean = guam_data.groupby('Year')['foF2'].mean().reset_index()
        darwin_yearly_mean = darwin_data.groupby('Year')['foF2'].mean().reset_index()
        
        merged = pd.merge(guam_yearly_mean, darwin_yearly_mean, on='Year', suffixes=('_Guam', '_Darwin'))
        
        if len(merged) > 1:
            ax4.scatter(merged['foF2_Guam'], merged['foF2_Darwin'], s=60, alpha=0.7, color='purple')
            
            # Add correlation line
            z = np.polyfit(merged['foF2_Guam'], merged['foF2_Darwin'], 1)
            p = np.poly1d(z)
            ax4.plot(merged['foF2_Guam'], p(merged['foF2_Guam']), "r--", alpha=0.8, linewidth=2)
            
            # Calculate correlation
            correlation = merged['foF2_Guam'].corr(merged['foF2_Darwin'])
            ax4.set_title(f'Guam vs Darwin Correlation\nr = {correlation:.3f}', fontweight='bold')
            ax4.set_xlabel('Guam foF2 (MHz)')
            ax4.set_ylabel('Darwin foF2 (MHz)')
            ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Detailed NVIS Analysis - Complete Dataset', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # Save
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'Complete_NVIS_Detailed_Analysis_{timestamp}.png'
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")

def main():
    """Main execution function"""
    print("📊 COMPLETE NVIS DATA - 2x2 CHART GENERATOR")
    print("=" * 60)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load complete data
    guam_raw, darwin_raw = load_complete_data()
    
    if guam_raw.empty and darwin_raw.empty:
        print("❌ No data loaded, exiting...")
        return
    
    # Process data
    guam_data = clean_and_process_data(guam_raw, 'Guam')
    darwin_data = clean_and_process_data(darwin_raw, 'Darwin')
    
    # Generate charts
    guam_yearly, darwin_yearly = generate_2x2_comparison_chart(guam_data, darwin_data)
    generate_detailed_analysis(guam_data, darwin_data)
    
    # Print summary
    print("\n🎉 2x2 CHART GENERATION COMPLETE!")
    print("=" * 60)
    print(f"📊 Guam data points: {len(guam_data)}")
    print(f"📊 Darwin data points: {len(darwin_data)}")
    
    if not guam_data.empty:
        print(f"🌊 Guam foF2 range: {guam_data['foF2'].min():.1f} - {guam_data['foF2'].max():.1f} MHz")
        print(f"🌊 Guam foF2 average: {guam_data['foF2'].mean():.1f} MHz")
    
    if not darwin_data.empty:
        print(f"🌏 Darwin foF2 range: {darwin_data['foF2'].min():.1f} - {darwin_data['foF2'].max():.1f} MHz")
        print(f"🌏 Darwin foF2 average: {darwin_data['foF2'].mean():.1f} MHz")
    
    print(f"📁 Charts saved to: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
