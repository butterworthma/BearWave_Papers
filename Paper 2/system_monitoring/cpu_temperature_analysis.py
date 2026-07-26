#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CPU Temperature Analysis for BearWave System
============================================

Analyzes CPU temperature data from field deployments to assess
system thermal performance during NVIS operations in Borneo.

Part of BearWave Paper 1: "Enhancing Remote Conservation in Borneo: 
NVIS for Wildlife Monitoring and Protection using BearWave"

Author: Research Team
License: MIT
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
import os

# Configuration
DATA_FILE = 'data/cpu_temperature_data.xlsx'
OUTPUT_DIR = 'output'

# Temperature thresholds (°C)
THROTTLING_TEMP = 80.0      # Temperature at which CPU throttling occurs
WARNING_TEMP = 70.0         # Warning threshold for high temperatures
CRITICAL_TEMP = 85.0        # Critical temperature threshold
AMBIENT_TEMP = 30.0         # Estimated ambient temperature in Borneo

def load_and_clean_data():
    """Load and clean CPU temperature data"""
    print(f"📊 Loading CPU temperature data from {DATA_FILE}...")
    
    try:
        df = pd.read_excel(DATA_FILE)
        print(f"✅ Loaded {len(df)} records")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return pd.DataFrame()
    
    # Clean column names (first row contains headers)
    if 'results modified' in df.columns:
        # Use first row as headers
        new_columns = df.iloc[0].values
        df.columns = new_columns
        df = df.drop(0).reset_index(drop=True)
    
    # Rename columns for easier access
    df.columns = ['Time', 'Temp_C', 'Unit', 'CPU_Speed_MHz', 'Core_Speed_MHz', 'Health', 'Vcore']
    
    # Clean temperature data
    df['Temp_C'] = pd.to_numeric(df['Temp_C'], errors='coerce')
    df = df.dropna(subset=['Temp_C'])
    
    # Clean CPU speed data
    df['CPU_Speed_MHz'] = pd.to_numeric(df['CPU_Speed_MHz'], errors='coerce')
    df['Core_Speed_MHz'] = pd.to_numeric(df['Core_Speed_MHz'], errors='coerce')
    
    # Create datetime if possible (assuming today's date for time-only data)
    try:
        df['DateTime'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
        # If only time is provided, assume today's date
        if df['DateTime'].dt.date.nunique() == 1:
            base_date = datetime.now().date()
            df['DateTime'] = df['DateTime'].apply(lambda x: datetime.combine(base_date, x.time()))
    except:
        # Create sequential timestamps
        start_time = datetime.now().replace(hour=16, minute=29, second=36, microsecond=0)
        df['DateTime'] = [start_time + timedelta(seconds=i*10) for i in range(len(df))]
    
    print(f"✅ Cleaned data: {len(df)} valid temperature records")
    return df

def analyze_thermal_performance(df):
    """Analyze thermal performance metrics"""
    print("📊 Analyzing thermal performance...")
    
    # Calculate statistics
    avg_temp = df['Temp_C'].mean()
    max_temp = df['Temp_C'].max()
    min_temp = df['Temp_C'].min()
    std_temp = df['Temp_C'].std()
    
    # Calculate time above thresholds
    time_above_warning = (df['Temp_C'] > WARNING_TEMP).sum() / len(df) * 100
    time_above_throttling = (df['Temp_C'] > THROTTLING_TEMP).sum() / len(df) * 100
    time_above_critical = (df['Temp_C'] > CRITICAL_TEMP).sum() / len(df) * 100
    
    # Temperature rise above ambient
    temp_rise = avg_temp - AMBIENT_TEMP
    
    stats = {
        'avg_temp': avg_temp,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'std_temp': std_temp,
        'temp_rise': temp_rise,
        'time_above_warning': time_above_warning,
        'time_above_throttling': time_above_throttling,
        'time_above_critical': time_above_critical
    }
    
    return stats

def generate_temperature_timeline(df, stats):
    """Generate temperature timeline chart"""
    print("📊 Generating temperature timeline...")
    
    plt.figure(figsize=(16, 10))
    
    # Main temperature plot
    plt.subplot(2, 1, 1)
    plt.plot(df['DateTime'], df['Temp_C'], color='darkred', linewidth=1, alpha=0.8)
    
    # Add threshold lines
    plt.axhline(y=WARNING_TEMP, color='orange', linestyle='--', linewidth=2, 
                label=f'Warning Threshold ({WARNING_TEMP}°C)')
    plt.axhline(y=THROTTLING_TEMP, color='red', linestyle='--', linewidth=2,
                label=f'Throttling Threshold ({THROTTLING_TEMP}°C)')
    plt.axhline(y=CRITICAL_TEMP, color='darkred', linestyle='--', linewidth=2,
                label=f'Critical Threshold ({CRITICAL_TEMP}°C)')
    plt.axhline(y=AMBIENT_TEMP, color='green', linestyle=':', linewidth=2,
                label=f'Ambient Temperature ({AMBIENT_TEMP}°C)')
    
    # Add moving average
    window = min(50, len(df) // 10)
    if window > 1:
        df['Temp_MA'] = df['Temp_C'].rolling(window=window).mean()
        plt.plot(df['DateTime'], df['Temp_MA'], color='blue', linewidth=2, 
                label=f'{window}-point Moving Average')
    
    plt.title('BearWave System - CPU Temperature Monitoring\n'
              f'Avg: {stats["avg_temp"]:.1f}°C | Max: {stats["max_temp"]:.1f}°C | '
              f'Rise above ambient: {stats["temp_rise"]:.1f}°C', 
              fontsize=14, fontweight='bold')
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # CPU Speed subplot
    plt.subplot(2, 1, 2)
    if 'CPU_Speed_MHz' in df.columns and df['CPU_Speed_MHz'].notna().any():
        plt.plot(df['DateTime'], df['CPU_Speed_MHz'], color='blue', linewidth=1, 
                label='CPU Speed', alpha=0.8)
        plt.plot(df['DateTime'], df['Core_Speed_MHz'], color='green', linewidth=1,
                label='Core Speed', alpha=0.8)
        plt.ylabel('Speed (MHz)', fontsize=12)
        plt.legend()
    else:
        # Show temperature distribution instead
        plt.hist(df['Temp_C'], bins=30, alpha=0.7, color='darkred', edgecolor='black')
        plt.axvline(stats['avg_temp'], color='blue', linestyle='--', linewidth=2,
                   label=f'Mean: {stats["avg_temp"]:.1f}°C')
        plt.axvline(WARNING_TEMP, color='orange', linestyle='--', linewidth=2,
                   label=f'Warning: {WARNING_TEMP}°C')
        plt.xlabel('Temperature (°C)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.legend()
        plt.title('Temperature Distribution', fontsize=12)
    
    plt.xlabel('Time', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Format x-axis
    for ax in plt.gcf().get_axes():
        if hasattr(ax.xaxis, 'set_major_formatter'):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save
    filename = 'bearwave_cpu_temperature_analysis.png'
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")

def generate_thermal_summary(df, stats):
    """Generate thermal performance summary"""
    print("📊 Generating thermal performance summary...")
    
    plt.figure(figsize=(14, 8))
    
    # Create summary metrics plot
    plt.subplot(2, 2, 1)
    metrics = ['Avg Temp', 'Max Temp', 'Temp Rise', 'Std Dev']
    values = [stats['avg_temp'], stats['max_temp'], stats['temp_rise'], stats['std_temp']]
    colors = ['blue', 'red', 'orange', 'green']
    
    bars = plt.bar(metrics, values, color=colors, alpha=0.7)
    plt.title('Temperature Metrics (°C)', fontweight='bold')
    plt.ylabel('Temperature (°C)')
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Threshold exceedance plot
    plt.subplot(2, 2, 2)
    thresholds = ['Warning\n(>70°C)', 'Throttling\n(>80°C)', 'Critical\n(>85°C)']
    percentages = [stats['time_above_warning'], stats['time_above_throttling'], 
                  stats['time_above_critical']]
    colors = ['orange', 'red', 'darkred']
    
    bars = plt.bar(thresholds, percentages, color=colors, alpha=0.7)
    plt.title('Time Above Thresholds (%)', fontweight='bold')
    plt.ylabel('Percentage of Time (%)')
    
    # Add value labels
    for bar, value in zip(bars, percentages):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Temperature vs Time scatter
    plt.subplot(2, 2, 3)
    colors = ['green' if temp < WARNING_TEMP else 'orange' if temp < THROTTLING_TEMP 
              else 'red' for temp in df['Temp_C']]
    plt.scatter(range(len(df)), df['Temp_C'], c=colors, alpha=0.6, s=10)
    plt.axhline(y=WARNING_TEMP, color='orange', linestyle='--', alpha=0.7)
    plt.axhline(y=THROTTLING_TEMP, color='red', linestyle='--', alpha=0.7)
    plt.title('Temperature Over Time', fontweight='bold')
    plt.xlabel('Sample Number')
    plt.ylabel('Temperature (°C)')
    
    # System health assessment
    plt.subplot(2, 2, 4)
    if stats['max_temp'] < WARNING_TEMP:
        health_status = 'EXCELLENT'
        health_color = 'green'
    elif stats['max_temp'] < THROTTLING_TEMP:
        health_status = 'GOOD'
        health_color = 'orange'
    elif stats['max_temp'] < CRITICAL_TEMP:
        health_status = 'CAUTION'
        health_color = 'red'
    else:
        health_status = 'CRITICAL'
        health_color = 'darkred'
    
    plt.text(0.5, 0.7, 'SYSTEM HEALTH', ha='center', va='center', 
             fontsize=16, fontweight='bold', transform=plt.gca().transAxes)
    plt.text(0.5, 0.5, health_status, ha='center', va='center',
             fontsize=24, fontweight='bold', color=health_color,
             transform=plt.gca().transAxes)
    plt.text(0.5, 0.3, f'Max Temp: {stats["max_temp"]:.1f}°C', ha='center', va='center',
             fontsize=12, transform=plt.gca().transAxes)
    plt.text(0.5, 0.1, f'Duration: {len(df)} samples', ha='center', va='center',
             fontsize=12, transform=plt.gca().transAxes)
    plt.axis('off')
    
    plt.suptitle('BearWave System - Thermal Performance Summary', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    # Save
    filename = 'bearwave_thermal_performance_summary.png'
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")

def main():
    """Main execution function"""
    print("🌡️ BEARWAVE CPU TEMPERATURE ANALYSIS")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load and process data
    df = load_and_clean_data()
    
    if len(df) == 0:
        print("❌ No data loaded, exiting...")
        return
    
    # Analyze thermal performance
    stats = analyze_thermal_performance(df)
    
    # Generate charts
    generate_temperature_timeline(df, stats)
    generate_thermal_summary(df, stats)
    
    # Print summary
    print("\n🎉 THERMAL ANALYSIS COMPLETE!")
    print("=" * 50)
    print(f"📊 Total samples analyzed: {len(df)}")
    print(f"🌡️ Average temperature: {stats['avg_temp']:.1f}°C")
    print(f"🔥 Maximum temperature: {stats['max_temp']:.1f}°C")
    print(f"📈 Temperature rise above ambient: {stats['temp_rise']:.1f}°C")
    print(f"⚠️ Time above warning threshold: {stats['time_above_warning']:.1f}%")
    print(f"🚨 Time above throttling threshold: {stats['time_above_throttling']:.1f}%")
    print(f"📁 Charts saved to: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
