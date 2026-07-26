#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure 28: Raspberry Pi CPU Throttling Temperature Analysis
===========================================================

Generates Figure 28 for Paper 2 showing Raspberry Pi CPU temperature
monitoring and throttling analysis during BearWave field operations.

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

# Raspberry Pi temperature thresholds (°C)
THROTTLING_TEMP = 80.0      # Temperature at which CPU throttling occurs
WARNING_TEMP = 70.0         # Warning threshold for high temperatures
CRITICAL_TEMP = 85.0        # Critical temperature threshold
AMBIENT_TEMP = 30.0         # Estimated ambient temperature in Borneo

def load_and_clean_data():
    """Load and clean Raspberry Pi CPU temperature data"""
    print(f"📊 Loading Raspberry Pi CPU temperature data from {DATA_FILE}...")
    
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
    
    # Create datetime (assuming sequential 10-second intervals)
    start_time = datetime.now().replace(hour=16, minute=29, second=36, microsecond=0)
    df['DateTime'] = [start_time + timedelta(seconds=i*10) for i in range(len(df))]
    
    print(f"✅ Cleaned data: {len(df)} valid temperature records")
    return df

def generate_fig28_cpu_throttling_chart(df):
    """Generate Figure 28: Raspberry Pi CPU Throttling Temperature chart"""
    print("📊 Generating Figure 28: Raspberry Pi CPU Throttling Temperature...")
    
    # Calculate statistics
    avg_temp = df['Temp_C'].mean()
    max_temp = df['Temp_C'].max()
    min_temp = df['Temp_C'].min()
    
    # Calculate time above thresholds
    time_above_warning = (df['Temp_C'] > WARNING_TEMP).sum() / len(df) * 100
    time_above_throttling = (df['Temp_C'] > THROTTLING_TEMP).sum() / len(df) * 100
    
    # Create the main figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Top subplot: Temperature timeline
    ax1.plot(df['DateTime'], df['Temp_C'], color='darkred', linewidth=1.5, alpha=0.8, label='CPU Temperature')
    
    # Add threshold lines
    ax1.axhline(y=WARNING_TEMP, color='orange', linestyle='--', linewidth=2, 
                label=f'Warning Threshold ({WARNING_TEMP}°C)')
    ax1.axhline(y=THROTTLING_TEMP, color='red', linestyle='--', linewidth=2,
                label=f'Throttling Threshold ({THROTTLING_TEMP}°C)')
    ax1.axhline(y=CRITICAL_TEMP, color='darkred', linestyle='--', linewidth=2,
                label=f'Critical Threshold ({CRITICAL_TEMP}°C)')
    ax1.axhline(y=AMBIENT_TEMP, color='green', linestyle=':', linewidth=2,
                label=f'Ambient Temperature ({AMBIENT_TEMP}°C)')
    
    # Add moving average
    window = 50
    df['Temp_MA'] = df['Temp_C'].rolling(window=window).mean()
    ax1.plot(df['DateTime'], df['Temp_MA'], color='blue', linewidth=2, 
            label=f'{window}-point Moving Average')
    
    # Shade regions above thresholds
    ax1.fill_between(df['DateTime'], WARNING_TEMP, df['Temp_C'], 
                     where=(df['Temp_C'] > WARNING_TEMP), 
                     color='orange', alpha=0.2, label='Above Warning')
    ax1.fill_between(df['DateTime'], THROTTLING_TEMP, df['Temp_C'], 
                     where=(df['Temp_C'] > THROTTLING_TEMP), 
                     color='red', alpha=0.3, label='Above Throttling')
    
    ax1.set_title('Figure 28: Raspberry Pi CPU Throttling Temperature\n'
                  f'Avg: {avg_temp:.1f}°C | Max: {max_temp:.1f}°C | Min: {min_temp:.1f}°C | '
                  f'Above Warning: {time_above_warning:.1f}%', 
                  fontsize=14, fontweight='bold')
    ax1.set_ylabel('Temperature (°C)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.set_ylim(min_temp - 5, max_temp + 5)
    
    # Bottom subplot: CPU Speed vs Temperature correlation
    if df['CPU_Speed_MHz'].notna().any():
        # Create scatter plot of temperature vs CPU speed
        colors = ['green' if temp < WARNING_TEMP else 'orange' if temp < THROTTLING_TEMP 
                  else 'red' for temp in df['Temp_C']]
        
        ax2.scatter(df['Temp_C'], df['CPU_Speed_MHz'], c=colors, alpha=0.6, s=20)
        
        # Add trend line
        z = np.polyfit(df['Temp_C'].dropna(), df['CPU_Speed_MHz'].dropna(), 1)
        p = np.poly1d(z)
        ax2.plot(df['Temp_C'], p(df['Temp_C']), "r--", alpha=0.8, linewidth=2, label='Trend Line')
        
        ax2.axvline(x=WARNING_TEMP, color='orange', linestyle='--', alpha=0.7, label=f'Warning ({WARNING_TEMP}°C)')
        ax2.axvline(x=THROTTLING_TEMP, color='red', linestyle='--', alpha=0.7, label=f'Throttling ({THROTTLING_TEMP}°C)')
        
        ax2.set_xlabel('Temperature (°C)', fontsize=12)
        ax2.set_ylabel('CPU Speed (MHz)', fontsize=12)
        ax2.set_title('CPU Speed vs Temperature Correlation', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
    else:
        # Show temperature distribution histogram
        ax2.hist(df['Temp_C'], bins=30, alpha=0.7, color='darkred', edgecolor='black')
        ax2.axvline(avg_temp, color='blue', linestyle='--', linewidth=2,
                   label=f'Mean: {avg_temp:.1f}°C')
        ax2.axvline(WARNING_TEMP, color='orange', linestyle='--', linewidth=2,
                   label=f'Warning: {WARNING_TEMP}°C')
        ax2.axvline(THROTTLING_TEMP, color='red', linestyle='--', linewidth=2,
                   label=f'Throttling: {THROTTLING_TEMP}°C')
        
        ax2.set_xlabel('Temperature (°C)', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.set_title('Temperature Distribution', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
    
    # Format x-axis for top subplot
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    
    # Save as Figure 28
    filename = 'Fig28_Raspberry_Pi_CPU_Throttling_Temperature.png'
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")
    
    return {
        'avg_temp': avg_temp,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'time_above_warning': time_above_warning,
        'time_above_throttling': time_above_throttling
    }

def generate_thermal_performance_summary(df, stats):
    """Generate thermal performance summary for Paper 2"""
    print("📊 Generating thermal performance summary...")
    
    plt.figure(figsize=(12, 8))
    
    # Create 2x2 subplot layout
    plt.subplot(2, 2, 1)
    # Temperature over time with key statistics
    plt.plot(range(len(df)), df['Temp_C'], color='darkred', alpha=0.7, linewidth=1)
    plt.axhline(y=stats['avg_temp'], color='blue', linestyle='--', linewidth=2, 
                label=f'Average: {stats["avg_temp"]:.1f}°C')
    plt.axhline(y=THROTTLING_TEMP, color='red', linestyle='--', linewidth=2,
                label=f'Throttling: {THROTTLING_TEMP}°C')
    plt.title('Temperature Timeline', fontweight='bold')
    plt.xlabel('Sample Number')
    plt.ylabel('Temperature (°C)')
    plt.legend(fontsize=9)
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Temperature statistics
    plt.subplot(2, 2, 2)
    metrics = ['Avg', 'Max', 'Min', 'Range']
    values = [stats['avg_temp'], stats['max_temp'], stats['min_temp'], 
              stats['max_temp'] - stats['min_temp']]
    colors = ['blue', 'red', 'green', 'orange']
    
    bars = plt.bar(metrics, values, color=colors, alpha=0.7)
    plt.title('Temperature Statistics (°C)', fontweight='bold')
    plt.ylabel('Temperature (°C)')
    
    # Add value labels
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Subplot 3: Threshold analysis
    plt.subplot(2, 2, 3)
    thresholds = ['Normal\n(<70°C)', 'Warning\n(70-80°C)', 'Throttling\n(>80°C)']
    normal_time = 100 - stats['time_above_warning']
    warning_time = stats['time_above_warning'] - stats['time_above_throttling']
    throttling_time = stats['time_above_throttling']
    
    percentages = [normal_time, warning_time, throttling_time]
    colors = ['green', 'orange', 'red']
    
    bars = plt.bar(thresholds, percentages, color=colors, alpha=0.7)
    plt.title('Time in Temperature Zones (%)', fontweight='bold')
    plt.ylabel('Percentage of Time (%)')
    
    for bar, value in zip(bars, percentages):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Subplot 4: System health status
    plt.subplot(2, 2, 4)
    if stats['max_temp'] < WARNING_TEMP:
        health_status = 'EXCELLENT'
        health_color = 'green'
    elif stats['max_temp'] < THROTTLING_TEMP:
        health_status = 'GOOD'
        health_color = 'orange'
    else:
        health_status = 'CAUTION'
        health_color = 'red'
    
    plt.text(0.5, 0.7, 'SYSTEM STATUS', ha='center', va='center', 
             fontsize=14, fontweight='bold', transform=plt.gca().transAxes)
    plt.text(0.5, 0.5, health_status, ha='center', va='center',
             fontsize=20, fontweight='bold', color=health_color,
             transform=plt.gca().transAxes)
    plt.text(0.5, 0.3, f'Max: {stats["max_temp"]:.1f}°C', ha='center', va='center',
             fontsize=12, transform=plt.gca().transAxes)
    plt.text(0.5, 0.1, f'Samples: {len(df)}', ha='center', va='center',
             fontsize=12, transform=plt.gca().transAxes)
    plt.axis('off')
    
    plt.suptitle('Raspberry Pi Thermal Performance Analysis - Paper 2', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Save
    filename = 'Raspberry_Pi_Thermal_Performance_Summary.png'
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {filename}")

def main():
    """Main execution function"""
    print("🌡️ FIGURE 28: RASPBERRY PI CPU THROTTLING TEMPERATURE")
    print("=" * 60)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load and process data
    df = load_and_clean_data()
    
    if len(df) == 0:
        print("❌ No data loaded, exiting...")
        return
    
    # Generate Figure 28
    stats = generate_fig28_cpu_throttling_chart(df)
    
    # Generate additional thermal analysis
    generate_thermal_performance_summary(df, stats)
    
    # Print summary
    print("\n🎉 FIGURE 28 GENERATION COMPLETE!")
    print("=" * 60)
    print(f"📊 Total samples analyzed: {len(df)}")
    print(f"🌡️ Average temperature: {stats['avg_temp']:.1f}°C")
    print(f"🔥 Maximum temperature: {stats['max_temp']:.1f}°C")
    print(f"❄️ Minimum temperature: {stats['min_temp']:.1f}°C")
    print(f"⚠️ Time above warning threshold: {stats['time_above_warning']:.1f}%")
    print(f"🚨 Time above throttling threshold: {stats['time_above_throttling']:.1f}%")
    print(f"📁 Charts saved to: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
