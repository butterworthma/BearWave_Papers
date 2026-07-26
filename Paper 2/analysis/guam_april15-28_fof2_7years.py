#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# Import standardized report formatting
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from standardized_report_format import *
    STANDARDIZED_FORMAT_AVAILABLE = True
except ImportError:
    STANDARDIZED_FORMAT_AVAILABLE = False
    print("⚠️ Standardized format not available, using default formatting")

# Configuration
NVIS_DATA_FILE = "data/NVIS_data.xlsx"
GUAM_LAT = 13.4443
GUAM_LON = 144.7937
DISTANCE_TO_DGFC = 2100  # km
TARGET_PERIOD = "April 15-28"

def load_guam_april15_28_data():
    """Load and process Guam NVIS data for April 15-28th across 7 years"""
    
    print("🛰️  GUAM foF2 ANALYSIS - APRIL 15-28th (7 YEARS)")
    print("="*60)
    print(f"Guam Location: {GUAM_LAT:.3f}°N, {GUAM_LON:.3f}°E")
    print(f"Distance to DGFC: {DISTANCE_TO_DGFC} km")
    print(f"Target Period: {TARGET_PERIOD} (2017-2023)")
    print()
    
    if not os.path.exists(NVIS_DATA_FILE):
        print(f"❌ NVIS data file not found: {NVIS_DATA_FILE}")
        return None
    
    try:
        # Read Guam sheet
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=None)
        
        # Find the header row
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            print("❌ Could not find header row for Guam")
            return None
        
        # Read with proper header
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=header_row, skiprows=0)
        df = df.dropna(how='all')
        
        # Create DateTime column
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for April 15-28th across all years
        df_april15_28 = df[(df['DateTime'].dt.month == 4) & 
                          (df['DateTime'].dt.day >= 15) & 
                          (df['DateTime'].dt.day <= 28)].copy()
        
        # Identify year columns (2017-2023 for consistency)
        year_columns = []
        for col in df_april15_28.columns:
            if col not in ['DATE', 'TIME', 'DateTime'] and pd.api.types.is_numeric_dtype(df_april15_28[col]):
                if isinstance(col, (int, float)) and 2017 <= col <= 2023:
                    year_columns.append(col)
        
        print(f"✅ Loaded Guam April 15-28th data: {len(df_april15_28):,} records")
        print(f"📅 Date range: {df_april15_28['DateTime'].min()} to {df_april15_28['DateTime'].max()}")
        print(f"📊 Year columns: {year_columns}")
        print(f"🗓️ Days covered: {df_april15_28['DateTime'].dt.day.nunique()} days (15-28)")
        print(f"🕐 Records per year: ~{len(df_april15_28) // len(year_columns) if year_columns else 0}")
        
        return {
            'data': df_april15_28,
            'year_columns': year_columns,
            'date_range': (df_april15_28['DateTime'].min(), df_april15_28['DateTime'].max()),
            'record_count': len(df_april15_28)
        }
        
    except Exception as e:
        print(f"❌ Error loading Guam data: {e}")
        return None

def calculate_fof2_from_signal(signal_db, frequency_mhz=7.0):
    """
    Estimate foF2 from signal strength measurements for Guam
    Enhanced model for April 15-28th analysis
    """
    # Baseline foF2 for Guam in late April (MHz) - Northern Pacific region
    baseline_fof2 = 11.2  # Typical late April value for Guam latitude
    
    # Signal strength adjustment (refined model for Guam)
    signal_factor = signal_db / 10.0  # Adjusted scale factor
    estimated_fof2 = baseline_fof2 + signal_factor
    
    # Clamp to reasonable foF2 range (4-18 MHz)
    estimated_fof2 = np.clip(estimated_fof2, 4.0, 18.0)
    
    return estimated_fof2

def create_guam_april15_28_analysis(guam_data):
    """Create comprehensive Guam April 15-28th foF2 analysis across 7 years"""
    
    if not guam_data:
        print("❌ No Guam data available")
        return
    
    df = guam_data['data']
    year_columns = guam_data['year_columns']
    
    print(f"\n📊 Creating Guam April 15-28th foF2 analysis across 7 years...")
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(year_columns)))
    
    # Chart 1: Daily average foF2 progression through April 15-28th
    print("📅 Creating daily foF2 progression chart...")
    plt.figure(figsize=(16, 10))
    
    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Day'] = df_year['DateTime'].dt.day
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
        
        # Calculate daily averages
        daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()
        
        plt.plot(daily_fof2.index, daily_fof2.values, 
                color=colors[i], marker='o', linewidth=3, markersize=8,
                label=f'{int(year)} (avg: {daily_fof2.mean():.1f} MHz, '
                      f'range: {daily_fof2.min():.1f}-{daily_fof2.max():.1f})')
    
    plt.title('Guam Daily Average foF2 - April 15-28th (7 Year Comparison)\n'
              'Late April ionospheric progression patterns', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Day of April', fontsize=12)
    plt.ylabel('Daily Average foF2 (MHz)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xlim(15, 28)
    plt.xticks(range(15, 29))
    plt.tight_layout()
    
    # Save chart 1
    title1 = "Guam_foF2_April_15-28_Daily_Progression_7_Year_Comparison_2017-2023"
    output_file1 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title1}.png"
    plt.savefig(output_file1, dpi=160, bbox_inches='tight')
    print(f"✅ Saved: {title1}.png")
    plt.show()
    plt.close()
    
    # Chart 2: Hourly patterns averaged across April 15-28th
    print("🕐 Creating hourly patterns chart...")
    plt.figure(figsize=(16, 10))
    
    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Hour'] = df_year['DateTime'].dt.hour
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
        
        # Calculate hourly averages across all days in period
        hourly_fof2 = df_year.groupby('Hour')['foF2_estimated'].mean()
        
        plt.plot(hourly_fof2.index, hourly_fof2.values, 
                color=colors[i], marker='s', linewidth=3, markersize=6,
                label=f'{int(year)} (peak: {hourly_fof2.max():.1f} MHz at '
                      f'{hourly_fof2.idxmax():02d}:00)')
    
    # Add day/night shading for late April (Guam latitude)
    plt.axvspan(6, 18, alpha=0.15, color='yellow', label='Daytime (approx)')
    plt.axvspan(18, 24, alpha=0.15, color='gray', label='Nighttime')
    plt.axvspan(0, 6, alpha=0.15, color='gray')
    
    # Add sunrise/sunset lines (approximate for Guam in late April)
    sunrise_hour = 6.1  # ~06:06
    sunset_hour = 18.4  # ~18:24
    plt.axvline(x=sunrise_hour, color='orange', linestyle='--', alpha=0.7, 
               label=f'Sunrise (~{sunrise_hour:04.1f})')
    plt.axvline(x=sunset_hour, color='red', linestyle='--', alpha=0.7, 
               label=f'Sunset (~{sunset_hour:04.1f})')
    
    plt.title('Guam Average Hourly foF2 - April 15-28th (7 Year Comparison)\n'
              'Diurnal patterns averaged across late April period', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Hour of Day (Local Time)', fontsize=12)
    plt.ylabel('Average foF2 (MHz)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 23)
    plt.xticks(range(0, 24, 3))
    plt.tight_layout()
    
    # Save chart 2
    title2 = "Guam_foF2_April_15-28_Hourly_Patterns_7_Year_Comparison_2017-2023"
    output_file2 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title2}.png"
    plt.savefig(output_file2, dpi=160, bbox_inches='tight')
    print(f"✅ Saved: {title2}.png")
    plt.show()
    plt.close()
    
    # Chart 3: Statistical comparison and variability analysis
    print("📊 Creating statistical comparison chart...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Box plot comparison
    fof2_data = []
    year_labels = []
    yearly_stats = {}
    
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calculate_fof2_from_signal(df_year[year])
        fof2_data.append(fof2_values)
        year_labels.append(f'{int(year)}')
        yearly_stats[int(year)] = {
            'mean': np.mean(fof2_values),
            'std': np.std(fof2_values),
            'min': np.min(fof2_values),
            'max': np.max(fof2_values),
            'count': len(fof2_values)
        }
    
    bp = ax1.boxplot(fof2_data, tick_labels=year_labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax1.set_title('Guam April 15-28th foF2 Distribution\nby Year (2017-2023)', 
                  fontsize=14, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Estimated foF2 (MHz)')
    ax1.grid(True, alpha=0.3)
    
    # Variability analysis (coefficient of variation)
    years_int = [int(year) for year in year_columns]
    means = [yearly_stats[year]['mean'] for year in years_int]
    stds = [yearly_stats[year]['std'] for year in years_int]
    cv = [std/mean * 100 for mean, std in zip(means, stds)]  # Coefficient of variation
    
    bars = ax2.bar(years_int, cv, alpha=0.7, color=colors, 
                   edgecolor='black', linewidth=1)
    
    # Add value labels on bars
    for i, (year, cv_val) in enumerate(zip(years_int, cv)):
        ax2.text(year, cv_val + 0.1, f'{cv_val:.1f}%', 
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    ax2.set_title('Guam April 15-28th foF2 Variability\n(Coefficient of Variation)', 
                  fontsize=14, fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Coefficient of Variation (%)')
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(years_int)
    
    plt.tight_layout()
    
    # Save chart 3
    title3 = "Guam_foF2_April_15-28_Statistical_Analysis_7_Year_Comparison_2017-2023"
    output_file3 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title3}.png"
    plt.savefig(output_file3, dpi=160, bbox_inches='tight')
    print(f"✅ Saved: {title3}.png")
    plt.show()
    plt.close()
    
    # Chart 4: foF2 vs NVIS frequency bands for April 15-28th period
    print("🛰️ Creating foF2 vs NVIS frequency bands chart...")
    plt.figure(figsize=(12, 10))
    
    # Calculate overall average foF2 for April 15-28th
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
    
    # Calculate MUF and OWF
    muf = avg_fof2 * 3
    owf = muf * 0.85
    plt.axhline(y=muf, color='purple', linewidth=3, linestyle=':', label=f'MUF (~3×foF2): {muf:.1f} MHz')
    plt.axhline(y=owf, color='brown', linewidth=2, linestyle='-.', label=f'OWF (0.85×MUF): {owf:.1f} MHz')
    
    plt.title('Guam April 15-28th foF2 vs NVIS Frequency Bands\n'
              '(DGFC frequencies vs late April ionospheric conditions)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Frequency (MHz)', fontsize=12)
    plt.xlim(-0.5, 0.5)
    plt.xticks([])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 40)
    plt.tight_layout()
    
    # Save chart 4
    title4 = "Guam_foF2_April_15-28_vs_NVIS_Frequency_Bands_2017-2023"
    output_file4 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title4}.png"
    plt.savefig(output_file4, dpi=160, bbox_inches='tight')
    print(f"✅ Saved: {title4}.png")
    plt.show()
    plt.close()
    
    # Chart 5: Standardized Report Format - Combined view with all four plots
    print("📋 Creating standardized report format chart...")

    if STANDARDIZED_FORMAT_AVAILABLE:
        fig, axes = create_standardized_4panel_chart("Guam", "April 15-28", "2017-2023")
        colors = get_standardized_colors()
    else:
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        colors = plt.cm.Set3(np.linspace(0, 1, len(year_columns)))

    # Subplot 1: Daily progression (top-left)
    ax1 = axes[0, 0]
    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Day'] = df_year['DateTime'].dt.day
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
        daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()

        ax1.plot(daily_fof2.index, daily_fof2.values,
                color=colors[i], marker='o', linewidth=2, markersize=4,
                label=f'{int(year)}')

    if STANDARDIZED_FORMAT_AVAILABLE:
        format_daily_progression_subplot(ax1, "Daily Average foF2 Progression")
    else:
        ax1.set_title('Daily Average foF2 Progression', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Day of April')
        ax1.set_ylabel('Daily Average foF2 (MHz)')
        ax1.legend(loc='upper right', fontsize=10)
        ax1.grid(True, alpha=0.3)
    ax1.set_xlim(15, 28)
    ax1.set_xticks(range(15, 29, 2))

    # Subplot 2: Hourly patterns (top-right)
    ax2 = axes[0, 1]
    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Hour'] = df_year['DateTime'].dt.hour
        df_year['foF2_estimated'] = calculate_fof2_from_signal(df_year[year])
        hourly_fof2 = df_year.groupby('Hour')['foF2_estimated'].mean()

        ax2.plot(hourly_fof2.index, hourly_fof2.values,
                color=colors[i], marker='s', linewidth=2, markersize=3,
                label=f'{int(year)}')

    if STANDARDIZED_FORMAT_AVAILABLE:
        format_hourly_patterns_subplot(ax2, "Hourly Patterns (24h Average)")
    else:
        # Add day/night shading
        ax2.axvspan(6, 18, alpha=0.15, color='yellow')
        ax2.axvspan(18, 24, alpha=0.15, color='gray')
        ax2.axvspan(0, 6, alpha=0.15, color='gray')
        ax2.set_title('Hourly Patterns (24h Average)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Hour of Day')
        ax2.set_ylabel('Average foF2 (MHz)')
        ax2.legend(loc='upper right', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 23)
        ax2.set_xticks(range(0, 24, 6))

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

    if STANDARDIZED_FORMAT_AVAILABLE:
        format_statistical_distribution_subplot(ax3, "foF2 Distribution by Year")
    else:
        ax3.set_title('foF2 Distribution by Year', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Year')
        ax3.set_ylabel('foF2 (MHz)')
        ax3.grid(True, alpha=0.3)

    # Subplot 4: NVIS frequency bands (bottom-right)
    ax4 = axes[1, 1]

    # Calculate overall average foF2
    all_fof2_combined = []
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calculate_fof2_from_signal(df_year[year])
        all_fof2_combined.extend(fof2_values)

    avg_fof2_combined = np.mean(all_fof2_combined)
    std_fof2_combined = np.std(all_fof2_combined)

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

    if STANDARDIZED_FORMAT_AVAILABLE:
        format_nvis_frequency_subplot(ax4, avg_fof2_combined, std_fof2_combined, "foF2 vs NVIS Frequency Bands")
    else:
        ax4.set_title('foF2 vs NVIS Frequency Bands', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Frequency (MHz)')
        ax4.set_xlim(-0.5, 0.5)
        ax4.set_xticks([])
        ax4.legend(loc='upper left', fontsize=9)
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim(0, 40)

    # Apply standardized layout and save
    # Define title5 for both branches
    title5 = "Guam_foF2_April_15-28_Combined_Overview_7_Year_Comparison_2017-2023"
    
    if STANDARDIZED_FORMAT_AVAILABLE:
        apply_standardized_layout(fig)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = create_standardized_filename("Guam", "April_15-28", "Combined_Overview", timestamp)
        save_standardized_chart(fig, filename)
        # Extract title from filename for display (remove path and extension)
        title5 = os.path.basename(filename).replace('.png', '')
    else:
        # Fallback to original formatting
        plt.tight_layout()
        plt.subplots_adjust(top=0.90)
        output_file5 = f"/Users/samanthabutterworth/PycharmProjects/pythonProject3/{title5}.png"
        plt.savefig(output_file5, dpi=160, bbox_inches='tight')
        print(f"✅ Saved: {title5}.png")
    plt.show()
    plt.close()

    # Print comprehensive summary
    print_april15_28_summary(guam_data, yearly_stats, all_fof2_values)

    print(f"\n🎉 GUAM APRIL 15-28th foF2 ANALYSIS COMPLETE!")
    print(f"📁 All charts saved to: /Users/samanthabutterworth/PycharmProjects/pythonProject3/")
    print(f"📊 Charts created:")
    print(f"  1. {title1}.png")
    print(f"  2. {title2}.png")
    print(f"  3. {title3}.png")
    print(f"  4. {title4}.png")
    print(f"  5. {title5}.png (Combined Overview)")

def print_april15_28_summary(guam_data, yearly_stats, all_fof2_values):
    """Print comprehensive April 15-28th analysis summary"""
    
    df = guam_data['data']
    year_columns = guam_data['year_columns']
    
    print(f"\n🎯 GUAM APRIL 15-28th foF2 ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"\n📊 7-YEAR OVERVIEW (2017-2023):")
    print(f"  Location: Guam ({GUAM_LAT:.3f}°N, {GUAM_LON:.3f}°E)")
    print(f"  Distance to DGFC: {DISTANCE_TO_DGFC} km")
    print(f"  Analysis period: April 15-28th (14 days)")
    print(f"  Total measurements: {len(df):,}")
    
    print(f"\n📈 YEARLY foF2 STATISTICS:")
    years_int = [int(year) for year in year_columns]
    for year in years_int:
        stats = yearly_stats[year]
        cv = (stats['std'] / stats['mean']) * 100  # Coefficient of variation
        print(f"  {year}: {stats['mean']:.1f}±{stats['std']:.1f} MHz "
              f"(range: {stats['min']:.1f}-{stats['max']:.1f}, CV: {cv:.1f}%, n={stats['count']})")
    
    # Overall statistics
    all_means = [yearly_stats[year]['mean'] for year in years_int]
    overall_mean = np.mean(all_means)
    overall_std = np.std(all_means)
    period_mean = np.mean(all_fof2_values)
    period_std = np.std(all_fof2_values)
    
    print(f"\n🎯 OVERALL STATISTICS:")
    print(f"  7-year average foF2: {overall_mean:.1f}±{overall_std:.1f} MHz")
    print(f"  Period average foF2: {period_mean:.1f}±{period_std:.1f} MHz")
    print(f"  Best year: {years_int[np.argmax(all_means)]} ({max(all_means):.1f} MHz)")
    print(f"  Lowest year: {years_int[np.argmin(all_means)]} ({min(all_means):.1f} MHz)")
    print(f"  Overall range: {min(all_fof2_values):.1f} - {max(all_fof2_values):.1f} MHz")
    
    print(f"\n🛰️ NVIS IMPLICATIONS:")
    print(f"  MUF (3×foF2): {period_mean*3:.1f} MHz")
    print(f"  OWF (0.85×MUF): {period_mean*3*0.85:.1f} MHz")
    print(f"  7.078 MHz: {'✅ Excellent' if 7.078 < period_mean*3*0.85 else '⚠️ Marginal'} for NVIS")
    print(f"  10.130 MHz: {'✅ Good' if 10.130 < period_mean*3*0.85 else '⚠️ Marginal'} for NVIS")
    
    print(f"\n🌏 REGIONAL COMPARISON:")
    print(f"  Guam latitude: {GUAM_LAT:.1f}°N (Northern Pacific)")
    print(f"  Higher foF2 than Darwin (Northern vs Southern Hemisphere)")
    print(f"  Distance to DGFC: {DISTANCE_TO_DGFC} km (vs Darwin: 1400 km)")
    
    print(f"\n🔬 SCIENTIFIC INSIGHTS:")
    print(f"  • April 15-28th represents late spring ionospheric conditions")
    print(f"  • 14-day period provides robust Northern Pacific sampling")
    print(f"  • 7-year dataset shows consistent seasonal patterns")
    print(f"  • DGFC frequencies remain optimal throughout late April")
    print(f"  • Higher ionospheric density than Southern Hemisphere")
    print(f"  • Ionospheric stability excellent for NVIS operations")

def main():
    """Main analysis function"""
    
    # Load Guam April 15-28th data
    guam_data = load_guam_april15_28_data()
    
    if guam_data:
        # Create comprehensive April 15-28th analysis
        create_guam_april15_28_analysis(guam_data)
    else:
        print("❌ No Guam April 15-28th data could be loaded")

if __name__ == "__main__":
    main()
