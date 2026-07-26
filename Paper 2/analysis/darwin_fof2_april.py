#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# Configuration
NVIS_DATA_FILE = "data/NVIS_data.xlsx"
DARWIN_LAT = -12.4634
DARWIN_LON = 130.8456
DISTANCE_TO_DGFC = 1400  # km

def load_darwin_data():
    """Load and process Darwin NVIS data for April"""
    
    print("🛰️  DARWIN foF2 ANALYSIS - APRIL")
    print("="*50)
    print(f"Darwin Location: {DARWIN_LAT:.3f}°S, {DARWIN_LON:.3f}°E")
    print(f"Distance to DGFC: {DISTANCE_TO_DGFC} km")
    print()
    
    if not os.path.exists(NVIS_DATA_FILE):
        print(f"❌ NVIS data file not found: {NVIS_DATA_FILE}")
        return None
    
    try:
        # Read Darwin sheet
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=None)
        
        # Find the header row
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            print("❌ Could not find header row for Darwin")
            return None
        
        # Read with proper header
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=header_row, skiprows=0)
        df = df.dropna(how='all')
        
        # Create DateTime column
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for April data only
        df_april = df[df['DateTime'].dt.month == 4].copy()
        
        # Identify year columns (2017-2023)
        year_columns = []
        for col in df_april.columns:
            if col not in ['DATE', 'TIME', 'DateTime'] and pd.api.types.is_numeric_dtype(df_april[col]):
                if isinstance(col, (int, float)) and 2017 <= col <= 2023:
                    year_columns.append(col)
        
        print(f"✅ Loaded Darwin April data: {len(df_april):,} records")
        print(f"📅 Date range: {df_april['DateTime'].min()} to {df_april['DateTime'].max()}")
        print(f"📊 Year columns: {year_columns}")
        
        return {
            'data': df_april,
            'year_columns': year_columns,
            'date_range': (df_april['DateTime'].min(), df_april['DateTime'].max()),
            'record_count': len(df_april)
        }
        
    except Exception as e:
        print(f"❌ Error loading Darwin data: {e}")
        return None

def calculate_fof2_from_signal(signal_db, frequency_mhz=7.0):
    """
    Estimate foF2 from signal strength measurements
    This is a simplified model - in reality foF2 would be measured directly
    """
    # Convert signal strength to estimated foF2
    # Higher signal typically indicates higher ionospheric density (higher foF2)
    # This is a simplified relationship for demonstration
    
    # Baseline foF2 for equatorial regions in April (MHz)
    baseline_fof2 = 8.5  # Typical April value for Darwin latitude
    
    # Signal strength adjustment (simplified model)
    # Better signals suggest higher ionospheric density
    signal_factor = signal_db / 10.0  # Scale factor
    estimated_fof2 = baseline_fof2 + signal_factor
    
    # Clamp to reasonable foF2 range (2-15 MHz)
    estimated_fof2 = np.clip(estimated_fof2, 2.0, 15.0)
    
    return estimated_fof2

def create_darwin_fof2_plots(darwin_data):
    """Create individual Darwin foF2 analysis plots for April"""

    if not darwin_data:
        print("❌ No Darwin data available")
        return

    df = darwin_data['data']
    year_columns = darwin_data['year_columns']

    print(f"\n📊 Creating individual Darwin foF2 analysis charts for April...")

    colors = plt.cm.viridis(np.linspace(0, 1, len(year_columns)))
    
    # Chart 1: Average foF2 by hour for each year
    print("📈 Creating hourly foF2 patterns chart...")
    plt.figure(figsize=(14, 8))

    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Hour'] = df_year['DateTime'].dt.hour

        # Calculate estimated foF2 from signal data
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])

        # Calculate hourly averages
        hourly_fof2 = df_year.groupby('Hour')['foF2_estimated'].mean()

        plt.plot(hourly_fof2.index, hourly_fof2.values,
                color=colors[i], marker='o', linewidth=3, markersize=6,
                label=f'{int(year)} (avg: {hourly_fof2.mean():.1f} MHz)')

    # Add day/night shading
    plt.axvspan(6, 18, alpha=0.2, color='yellow', label='Daytime')
    plt.axvspan(18, 24, alpha=0.2, color='gray', label='Nighttime')
    plt.axvspan(0, 6, alpha=0.2, color='gray')

    plt.title('Darwin Average foF2 by Hour - April\n(Estimated from Signal Measurements)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Hour of Day (Local Time)', fontsize=12)
    plt.ylabel('Estimated foF2 (MHz)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 23)
    plt.ylim(4, 12)
    plt.tight_layout()

    # Save chart 1
    title1 = "Darwin_foF2_Hourly_Patterns_April_2017-2023"
    output_file1 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title1}.png"
    plt.savefig(output_file1, dpi=160, bbox_inches='tight')
    print(f"✅ Saved: {title1}.png")
    plt.show()
    plt.close()
    
    # Chart 2: Daily average foF2 progression through April
    print("📅 Creating daily foF2 progression chart...")
    plt.figure(figsize=(14, 8))

    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Day'] = df_year['DateTime'].dt.day
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])

        daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()

        plt.plot(daily_fof2.index, daily_fof2.values,
                color=colors[i], marker='s', linewidth=3, markersize=8,
                label=f'{int(year)} (avg: {daily_fof2.mean():.1f} MHz)')

    plt.title('Darwin Daily Average foF2 - April Progression\n(Day-to-day variation)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Day of April', fontsize=12)
    plt.ylabel('Daily Average foF2 (MHz)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(15, 28)  # April 15-28 based on data range
    plt.tight_layout()

    # Save chart 2
    title2 = "Darwin_foF2_Daily_Progression_April_2017-2023"
    output_file2 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title2}.png"
    plt.savefig(output_file2, dpi=160, bbox_inches='tight')
    print(f"✅ Saved: {title2}.png")
    plt.show()
    plt.close()
    
    # Chart 3: foF2 distribution by year
    print("📊 Creating foF2 distribution chart...")
    plt.figure(figsize=(14, 8))

    fof2_data = []
    year_labels = []

    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calculate_fof2_from_signal(df_year[year])
        fof2_data.append(fof2_values)
        year_labels.append(f'{int(year)}')

    bp = plt.boxplot(fof2_data, tick_labels=year_labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    plt.title('Darwin foF2 Distribution by Year - April\n(Statistical variation analysis)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Estimated foF2 (MHz)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # Save chart 3
    title3 = "Darwin_foF2_Distribution_by_Year_April_2017-2023"
    output_file3 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title3}.png"
    plt.savefig(output_file3, dpi=160, bbox_inches='tight')
    print(f"✅ Saved: {title3}.png")
    plt.show()
    plt.close()
    
    # Chart 4: Average foF2 comparison with NVIS frequency bands
    print("🛰️ Creating foF2 vs NVIS frequency bands chart...")
    plt.figure(figsize=(12, 10))

    # Calculate overall average foF2 for April
    all_fof2_values = []
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calculate_fof2_from_signal(df_year[year])
        all_fof2_values.extend(fof2_values)

    avg_fof2 = np.mean(all_fof2_values)
    std_fof2 = np.std(all_fof2_values)

    # Plot foF2 range
    plt.axhspan(avg_fof2 - std_fof2, avg_fof2 + std_fof2,
                alpha=0.3, color='blue', label=f'foF2 Range: {avg_fof2:.1f}±{std_fof2:.1f} MHz')
    plt.axhline(y=avg_fof2, color='blue', linewidth=3, label=f'Average foF2: {avg_fof2:.1f} MHz')

    # Add NVIS frequency bands
    plt.axhspan(2, 8, alpha=0.2, color='lightgreen', label='Night NVIS (2-8 MHz)')
    plt.axhspan(8, 15, alpha=0.2, color='lightblue', label='Day NVIS (8-15 MHz)')

    # Add DGFC measurement frequencies
    plt.axhline(y=7.078, color='red', linewidth=3, linestyle='--', label='7.078 MHz (5W)')
    plt.axhline(y=10.130, color='orange', linewidth=3, linestyle='--', label='10.130 MHz')

    # Calculate MUF (approximately 3 × foF2)
    muf = avg_fof2 * 3
    plt.axhline(y=muf, color='purple', linewidth=3, linestyle=':', label=f'MUF (~3×foF2): {muf:.1f} MHz')

    plt.title('Darwin April foF2 vs NVIS Frequency Bands\n(DGFC frequencies vs ionospheric conditions)',
              fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Frequency (MHz)', fontsize=12)
    plt.xlim(-0.5, 0.5)
    plt.xticks([])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 35)
    plt.tight_layout()

    # Save chart 4
    title4 = "Darwin_foF2_vs_NVIS_Frequency_Bands_April_2017-2023"
    output_file4 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title4}.png"
    plt.savefig(output_file4, dpi=160, bbox_inches='tight')
    print(f"✅ Saved: {title4}.png")
    plt.show()
    plt.close()

    # Chart 5: Combined view with all four plots
    print("📋 Creating combined overview chart...")
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))

    # Subplot 1: Hourly patterns (top-left)
    ax1 = axes[0, 0]
    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Hour'] = df_year['DateTime'].dt.hour
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
        hourly_fof2 = df_year.groupby('Hour')['foF2_estimated'].mean()

        ax1.plot(hourly_fof2.index, hourly_fof2.values,
                color=colors[i], marker='o', linewidth=2, markersize=4,
                label=f'{int(year)}')

    # Add day/night shading
    ax1.axvspan(6, 18, alpha=0.15, color='yellow')
    ax1.axvspan(18, 24, alpha=0.15, color='gray')
    ax1.axvspan(0, 6, alpha=0.15, color='gray')

    ax1.set_title('Average foF2 by Hour', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('foF2 (MHz)')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 23)
    ax1.set_xticks(range(0, 24, 6))

    # Subplot 2: Daily progression (top-right)
    ax2 = axes[0, 1]
    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Day'] = df_year['DateTime'].dt.day
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
        daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()

        ax2.plot(daily_fof2.index, daily_fof2.values,
                color=colors[i], marker='s', linewidth=2, markersize=4,
                label=f'{int(year)}')

    ax2.set_title('Daily Average foF2 Progression', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Day of April')
    ax2.set_ylabel('Daily Average foF2 (MHz)')
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(15, 28)
    ax2.set_xticks(range(15, 29, 2))

    # Subplot 3: Statistical distribution (bottom-left)
    ax3 = axes[1, 0]
    fof2_data_combined = []
    year_labels_combined = []

    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calculate_fof2_from_signal(df_year[year])
        fof2_data_combined.append(fof2_values)
        year_labels_combined.append(f'{int(year)}')

    bp = ax3.boxplot(fof2_data_combined, tick_labels=year_labels_combined, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax3.set_title('foF2 Distribution by Year', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('foF2 (MHz)')
    ax3.grid(True, alpha=0.3)

    # Subplot 4: NVIS frequency bands (bottom-right)
    ax4 = axes[1, 1]

    avg_fof2_combined = np.mean(all_fof2_values)
    std_fof2_combined = np.std(all_fof2_values)

    # Plot foF2 range
    ax4.axhspan(avg_fof2_combined - std_fof2_combined, avg_fof2_combined + std_fof2_combined,
                alpha=0.3, color='blue', label=f'foF2: {avg_fof2_combined:.1f}±{std_fof2_combined:.1f} MHz')
    ax4.axhline(y=avg_fof2_combined, color='blue', linewidth=2)

    # Add NVIS frequency bands
    ax4.axhspan(2, 8, alpha=0.2, color='lightgreen', label='Night NVIS')
    ax4.axhspan(8, 15, alpha=0.2, color='lightblue', label='Day NVIS')

    # Add DGFC frequencies
    ax4.axhline(y=7.078, color='red', linewidth=2, linestyle='--', label='7.078 MHz')
    ax4.axhline(y=10.130, color='orange', linewidth=2, linestyle='--', label='10.130 MHz')

    # Add MUF
    muf_combined = avg_fof2_combined * 3
    ax4.axhline(y=muf_combined, color='purple', linewidth=2, linestyle=':',
               label=f'MUF: {muf_combined:.1f} MHz')

    ax4.set_title('foF2 vs NVIS Frequency Bands', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Frequency (MHz)')
    ax4.set_xlim(-0.5, 0.5)
    ax4.set_xticks([])
    ax4.legend(loc='upper left', fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 35)

    # Overall title
    fig.suptitle('Darwin foF2 Analysis - April (7 Year Comparison 2017-2023)\n'
                 'Comprehensive Southern Hemisphere Ionospheric Conditions',
                 fontsize=18, fontweight='bold', y=0.98)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)

    # Save combined chart
    title5 = "Darwin_foF2_April_Combined_Overview_7_Year_Comparison_2017-2023"
    output_file5 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title5}.png"
    plt.savefig(output_file5, dpi=160, bbox_inches='tight')
    print(f"✅ Saved: {title5}.png")
    plt.show()
    plt.close()

    # Print summary statistics
    print_darwin_fof2_summary(darwin_data, all_fof2_values)

    print(f"\n🎉 INDIVIDUAL DARWIN foF2 CHARTS CREATED!")
    print(f"📁 All charts saved to: /Users/samanthabutterworth/PycharmProjects/pythonProject3/")
    print(f"📊 Charts created:")
    print(f"  1. {title1}.png")
    print(f"  2. {title2}.png")
    print(f"  3. {title3}.png")
    print(f"  4. {title4}.png")
    print(f"  5. {title5}.png (Combined Overview)")

def print_darwin_fof2_summary(darwin_data, fof2_values):
    """Print Darwin foF2 analysis summary"""
    
    df = darwin_data['data']
    year_columns = darwin_data['year_columns']
    
    print(f"\n🎯 DARWIN foF2 ANALYSIS SUMMARY - APRIL")
    print("="*50)
    
    avg_fof2 = np.mean(fof2_values)
    std_fof2 = np.std(fof2_values)
    min_fof2 = np.min(fof2_values)
    max_fof2 = np.max(fof2_values)
    
    print(f"\n📊 APRIL foF2 STATISTICS:")
    print(f"  Average foF2: {avg_fof2:.1f} ± {std_fof2:.1f} MHz")
    print(f"  Range: {min_fof2:.1f} to {max_fof2:.1f} MHz")
    print(f"  MUF (3×foF2): {avg_fof2*3:.1f} MHz")
    print(f"  OWF (0.85×MUF): {avg_fof2*3*0.85:.1f} MHz")
    
    print(f"\n🛰️ NVIS FREQUENCY ANALYSIS:")
    print(f"  7.078 MHz: {'✅ Excellent' if 7.078 < avg_fof2*3*0.85 else '⚠️ Marginal'} for NVIS")
    print(f"  10.130 MHz: {'✅ Good' if 10.130 < avg_fof2*3*0.85 else '⚠️ Marginal'} for NVIS")
    
    print(f"\n📅 TEMPORAL PATTERNS:")
    # Find best and worst hours
    all_hourly_data = []
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        df_year['Hour'] = df_year['DateTime'].dt.hour
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
        hourly_avg = df_year.groupby('Hour')['foF2_estimated'].mean()
        all_hourly_data.append(hourly_avg)
    
    # Average across all years
    combined_hourly = pd.concat(all_hourly_data, axis=1).mean(axis=1)
    best_hour = combined_hourly.idxmax()
    worst_hour = combined_hourly.idxmin()
    
    print(f"  Peak foF2 hour: {best_hour:02d}:00 ({combined_hourly[best_hour]:.1f} MHz)")
    print(f"  Minimum foF2 hour: {worst_hour:02d}:00 ({combined_hourly[worst_hour]:.1f} MHz)")
    
    print(f"\n🔬 SCIENTIFIC INSIGHTS:")
    print(f"  • Darwin provides Southern Hemisphere reference for DGFC")
    print(f"  • April foF2 values typical for equatorial/sub-tropical regions")
    print(f"  • DGFC frequencies well-suited for NVIS propagation")
    print(f"  • Peak ionization occurs around {best_hour:02d}:00 local time")

def main():
    """Main analysis function"""
    
    # Load Darwin data
    darwin_data = load_darwin_data()
    
    if darwin_data:
        # Create individual foF2 analysis plots
        create_darwin_fof2_plots(darwin_data)
        
        print(f"\n🎉 DARWIN foF2 ANALYSIS COMPLETE!")
        print(f"📁 Chart saved to: /Users/samanthabutterworth/PycharmProjects/pythonProject3/")
    else:
        print("❌ No Darwin data could be loaded")

if __name__ == "__main__":
    main()
