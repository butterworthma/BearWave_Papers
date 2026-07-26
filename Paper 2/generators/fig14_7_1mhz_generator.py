#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure 14: 7.1 MHz NVIS Analysis Generator
==========================================

Generates 7.1 MHz NVIS propagation analysis charts for Paper 2.
Based on field trial data from DGFC Borneo operations.

Author: Research Team
License: MIT
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# Configuration
FILE_PATH = 'data/7_1_MHz_Standardized_data.xlsx'
OUTPUT_DIR = 'output'
FREQUENCY = '7.078 MHz'
POWER = '5 W'

def load_and_clean_data():
    """Load and clean 7.1 MHz data"""
    print(f"📊 Loading 7.1 MHz data from {FILE_PATH}...")
    
    try:
        # Load the Excel file
        df = pd.read_excel(FILE_PATH, sheet_name='final')
        print(f"✅ Loaded {len(df)} records")
    except:
        # Try without sheet name
        df = pd.read_excel(FILE_PATH)
        print(f"✅ Loaded {len(df)} records (default sheet)")
    
    # Assign column names if needed
    if len(df.columns) >= 11:
        df.columns = ['Date', 'Time', 'Raw_SNR', 'SNR', 'Frequency', 'Offset', 
                     'Band', 'Node', 'ID', 'Message', 'Locator']
    else:
        df.columns = ['Date', 'Time', 'SNR_DB', 'Value2', 'Value3', 'Label1', 
                     'Label2', 'Label3', 'Label4', 'Label5', 'Label6'][:len(df.columns)]
    
    # Clean data
    df = df.dropna(subset=['Date', 'Time', 'SNR' if 'SNR' in df.columns else 'SNR_DB'])
    
    # Convert SNR to numeric
    snr_col = 'SNR' if 'SNR' in df.columns else 'SNR_DB'
    df[snr_col] = pd.to_numeric(df[snr_col], errors='coerce')
    df = df.dropna(subset=[snr_col]).drop_duplicates()
    
    # Create datetime column
    df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str), errors='coerce')
    df = df.dropna(subset=['DateTime'])
    
    # Rename SNR column for consistency
    if 'SNR' in df.columns:
        df['SNR_DB'] = df['SNR']
    
    print(f"✅ Cleaned data: {len(df)} valid records")
    return df

def classify_time_period(hour):
    """Classify time as Day or Night"""
    return 'Day' if 6 <= hour.hour < 18 else 'Night'

def generate_24hour_analysis(df):
    """Generate 24-hour SNR analysis"""
    print("📊 Generating 24-hour analysis...")
    
    # Filter to best 24-hour period (based on your analysis)
    start_time = '2023-04-18 00:00:00'
    end_time = '2023-04-19 00:00:00'
    
    df_24h = df[(df['DateTime'] >= start_time) & (df['DateTime'] < end_time)].copy()
    
    if len(df_24h) == 0:
        print("⚠️ No data in specified 24-hour period, using all available data")
        df_24h = df.copy()
    
    # Group by hour
    df_24h['Hour'] = df_24h['DateTime'].dt.floor('h')
    hourly = df_24h.groupby('Hour')['SNR_DB'].agg(['mean', 'std', 'count']).reset_index()
    
    # Classify Day/Night
    hourly['Period'] = hourly['Hour'].apply(classify_time_period)
    
    # Calculate statistics
    day_data = hourly[hourly['Period'] == 'Day']
    night_data = hourly[hourly['Period'] == 'Night']
    
    day_avg = day_data['mean'].mean() if len(day_data) > 0 else 0
    night_avg = night_data['mean'].mean() if len(night_data) > 0 else 0
    overall_avg = hourly['mean'].mean()
    
    # Create plot
    plt.figure(figsize=(14, 8))
    
    # Plot Day and Night separately
    for period, group in hourly.groupby('Period'):
        color = 'orange' if period == 'Day' else 'navy'
        plt.plot(group['Hour'], group['mean'], marker='o', linestyle='-', 
                label=f'{period} (avg: {group["mean"].mean():.1f} dB)', 
                color=color, linewidth=2, markersize=6)
        
        # Add error bars
        plt.errorbar(group['Hour'], group['mean'], yerr=group['std'], 
                    color=color, alpha=0.3, capsize=3)
    
    # Formatting
    plt.title(f'{FREQUENCY} @ {POWER} - 24-Hour SNR Analysis\n'
              f'Day Average: {day_avg:.1f} dB | Night Average: {night_avg:.1f} dB | '
              f'Overall: {overall_avg:.1f} dB', fontsize=14, fontweight='bold')
    plt.xlabel('Time (Hours)', fontsize=12)
    plt.ylabel('Average SNR (dB)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Period', fontsize=11)
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # Save
    filename = f'{FREQUENCY.replace(" ", "_").replace(".", "_")}_24hour_analysis.png'
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    
    return hourly

def generate_best_period_analysis(df):
    """Generate analysis of best continuous period"""
    print("📊 Generating best period analysis...")
    
    # Best period based on your analysis: 2023-04-18 02:16:00 to 2023-04-18 22:51:15
    start_time = '2023-04-18 02:16:00'
    end_time = '2023-04-18 22:51:15'
    
    df_best = df[(df['DateTime'] >= start_time) & (df['DateTime'] <= end_time)].copy()
    
    if len(df_best) == 0:
        print("⚠️ No data in best period, using all available data")
        df_best = df.copy()
    
    # Create time series plot
    plt.figure(figsize=(16, 8))
    
    # Plot SNR over time
    plt.plot(df_best['DateTime'], df_best['SNR_DB'], 
             color='darkblue', alpha=0.7, linewidth=1)
    
    # Add moving average
    window = min(50, len(df_best) // 10)
    if window > 1:
        df_best['SNR_MA'] = df_best['SNR_DB'].rolling(window=window).mean()
        plt.plot(df_best['DateTime'], df_best['SNR_MA'], 
                color='red', linewidth=2, label=f'{window}-point Moving Average')
    
    # Add day/night shading
    for date in pd.date_range(df_best['DateTime'].min().date(), 
                             df_best['DateTime'].max().date(), freq='D'):
        day_start = pd.Timestamp(date.date()) + pd.Timedelta(hours=6)
        day_end = pd.Timestamp(date.date()) + pd.Timedelta(hours=18)
        plt.axvspan(day_start, day_end, alpha=0.1, color='yellow', label='Day' if date == pd.date_range(df_best['DateTime'].min().date(), df_best['DateTime'].max().date(), freq='D')[0] else "")
    
    # Statistics
    avg_snr = df_best['SNR_DB'].mean()
    std_snr = df_best['SNR_DB'].std()
    min_snr = df_best['SNR_DB'].min()
    max_snr = df_best['SNR_DB'].max()
    duration = df_best['DateTime'].max() - df_best['DateTime'].min()
    
    plt.title(f'{FREQUENCY} @ {POWER} - Best Continuous Period Analysis\n'
              f'Duration: {duration} | Avg: {avg_snr:.1f}±{std_snr:.1f} dB | '
              f'Range: {min_snr:.1f} to {max_snr:.1f} dB | N={len(df_best)}', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('SNR (dB)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=4))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # Save
    filename = f'{FREQUENCY.replace(" ", "_").replace(".", "_")}_best_period_analysis.png'
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    
    return df_best

def main():
    """Main execution function"""
    print(f"🎯 GENERATING {FREQUENCY} ANALYSIS CHARTS")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load and process data
    df = load_and_clean_data()
    
    # Generate analyses
    hourly_data = generate_24hour_analysis(df)
    best_period_data = generate_best_period_analysis(df)
    
    print("\n🎉 7.1 MHz ANALYSIS COMPLETE!")
    print(f"📁 Charts saved to: {OUTPUT_DIR}/")
    print(f"📊 Total data points analyzed: {len(df)}")
    print(f"📅 Date range: {df['DateTime'].min()} to {df['DateTime'].max()}")

if __name__ == "__main__":
    main()
