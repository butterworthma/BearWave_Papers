#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Display All foF2 Analysis Charts Side by Side
=============================================

This script creates a comprehensive side-by-side display of all 6 foF2 analysis charts:
- Darwin April 15th
- Darwin April 15-28th
- Darwin Full April
- Guam April 15th
- Guam April 15-28th
- Guam Full April

Each chart contains 4 subplots showing different aspects of the ionospheric analysis.

Author: Research Team
License: MIT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration
NVIS_DATA_FILE = "data/NVIS_data.xlsx"

# Import calculation functions from analysis scripts
def calculate_fof2_from_signal_darwin(signal_db, frequency_mhz=7.0):
    """Estimate foF2 from signal strength for Darwin"""
    baseline_fof2 = 9.0
    signal_factor = signal_db / 12.0
    estimated_fof2 = baseline_fof2 + signal_factor
    return np.clip(estimated_fof2, 3.0, 15.0)

def calculate_fof2_from_signal_guam(signal_db, frequency_mhz=7.0):
    """Estimate foF2 from signal strength for Guam"""
    baseline_fof2 = 10.5
    signal_factor = signal_db / 10.0
    estimated_fof2 = baseline_fof2 + signal_factor
    return np.clip(estimated_fof2, 4.0, 18.0)

def load_data(sheet_name, filter_func=None):
    """Generic data loading function"""
    if not os.path.exists(NVIS_DATA_FILE):
        return None
    
    try:
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name=sheet_name, header=None)
        
        # Find header row
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            return None
        
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name=sheet_name, header=header_row, skiprows=0)
        df = df.dropna(how='all')
        
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Apply filter if provided
        if filter_func:
            df = filter_func(df)
        
        # Identify year columns (2017-2023)
        year_columns = []
        for col in df.columns:
            if col not in ['DATE', 'TIME', 'DateTime'] and pd.api.types.is_numeric_dtype(df[col]):
                if isinstance(col, (int, float)) and 2017 <= col <= 2023:
                    year_columns.append(col)
        
        return {'data': df, 'year_columns': year_columns}
    except Exception as e:
        print(f"Error loading {sheet_name} data: {e}")
        return None

def create_4panel_chart(axes_list, data_dict, station_name, period_name, calc_func, colors):
    """Create a 4-panel chart in the given axes list [ax1, ax2, ax3, ax4]"""
    
    df = data_dict['data']
    year_columns = data_dict['year_columns']
    
    # Panel 1: Hourly Patterns (top-left)
    ax1 = axes_list[0]
    for i, year in enumerate(year_columns):
        df_year = df.dropna(subset=[year])
        df_year['Hour'] = df_year['DateTime'].dt.hour
        df_year['foF2_estimated'] = calc_func(df_year[year])
        hourly_fof2 = df_year.groupby('Hour')['foF2_estimated'].mean()
        
        ax1.plot(hourly_fof2.index, hourly_fof2.values,
                color=colors[i], marker='o', linewidth=1.5, markersize=3,
                label=f'{int(year)}')
    
    ax1.axvspan(6, 18, alpha=0.15, color='yellow')
    ax1.axvspan(18, 24, alpha=0.15, color='gray')
    ax1.axvspan(0, 6, alpha=0.15, color='gray')
    ax1.set_title('Hourly Patterns (24h)', fontsize=8, fontweight='bold', pad=3)
    ax1.set_xlabel('Hour (UTC)', fontsize=7)
    ax1.set_ylabel('foF2 (MHz)', fontsize=7)
    ax1.legend(loc='best', fontsize=6, ncol=4, framealpha=0.8)
    ax1.tick_params(labelsize=6)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 23)
    ax1.set_xticks(range(0, 24, 6))
    
    # Panel 2: Statistical Distribution (top-right)
    ax2 = axes_list[1]
    fof2_data = []
    year_labels = []
    
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calc_func(df_year[year])
        fof2_data.append(fof2_values)
        year_labels.append(f'{int(year)}')
    
    bp = ax2.boxplot(fof2_data, tick_labels=year_labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_title('foF2 Distribution', fontsize=8, fontweight='bold', pad=3)
    ax2.set_xlabel('Year', fontsize=7)
    ax2.set_ylabel('foF2 (MHz)', fontsize=7)
    ax2.tick_params(labelsize=6)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: Daily/Temporal Progression (bottom-left)
    ax3 = axes_list[2]
    
    # Determine if we need daily or hourly progression
    if 'Day' in str(period_name) or '15-28' in str(period_name):
        # Daily progression
        for i, year in enumerate(year_columns):
            df_year = df.dropna(subset=[year])
            df_year['Day'] = df_year['DateTime'].dt.day
            df_year['foF2_estimated'] = calc_func(df_year[year])
            daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()
            
            ax3.plot(daily_fof2.index, daily_fof2.values,
                    color=colors[i], marker='o', linewidth=1.5, markersize=3,
                    label=f'{int(year)}')
        
        ax3.set_xlabel('Day of Period', fontsize=7)
        ax3.set_title('Daily Progression', fontsize=8, fontweight='bold', pad=3)
    else:
        # For April 15th, show 24-hour progression
        for i, year in enumerate(year_columns):
            df_year = df.dropna(subset=[year])
            df_year['Hour'] = df_year['DateTime'].dt.hour
            df_year['Minute'] = df_year['DateTime'].dt.minute
            df_year['HourDecimal'] = df_year['Hour'] + df_year['Minute'] / 60.0
            df_year['foF2_estimated'] = calc_func(df_year[year])
            df_year = df_year.sort_values('HourDecimal')
            
            ax3.plot(df_year['HourDecimal'], df_year['foF2_estimated'],
                    color=colors[i], marker='o', linewidth=1.5, markersize=2,
                    label=f'{int(year)}')
        
        ax3.axvspan(6, 18, alpha=0.15, color='yellow')
        ax3.axvspan(18, 24, alpha=0.15, color='gray')
        ax3.axvspan(0, 6, alpha=0.15, color='gray')
        ax3.set_xlabel('Hour', fontsize=7)
        ax3.set_title('24h Progression', fontsize=8, fontweight='bold', pad=3)
        ax3.set_xlim(0, 24)
        ax3.set_xticks(range(0, 25, 6))
    
    ax3.set_ylabel('foF2 (MHz)', fontsize=7)
    ax3.legend(loc='best', fontsize=6, ncol=4, framealpha=0.8)
    ax3.tick_params(labelsize=6)
    ax3.grid(True, alpha=0.3)
    
    # Panel 4: NVIS Frequency Bands (bottom-right)
    ax4 = axes_list[3]
    
    # Calculate overall average foF2
    all_fof2_combined = []
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        fof2_values = calc_func(df_year[year])
        all_fof2_combined.extend(fof2_values)
    
    avg_fof2_combined = np.mean(all_fof2_combined)
    std_fof2_combined = np.std(all_fof2_combined)
    
    # Plot foF2 range
    ax4.axhspan(avg_fof2_combined - std_fof2_combined, avg_fof2_combined + std_fof2_combined,
                alpha=0.3, color='blue', label=f'foF2: {avg_fof2_combined:.1f}±{std_fof2_combined:.1f}')
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
               label=f'MUF: {muf_combined:.1f}')
    
    ax4.set_title('NVIS vs DGFC', fontsize=8, fontweight='bold', pad=3)
    ax4.set_ylabel('Frequency (MHz)', fontsize=7)
    ax4.set_xlim(-0.5, 0.5)
    ax4.set_xticks([])
    ax4.legend(loc='best', fontsize=6, framealpha=0.8)
    ax4.tick_params(labelsize=6)
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 40)
    
    # Add panel title above the top-left subplot
    panel_title = f'{station_name} - {period_name}'
    ax1.text(0.5, 1.08, panel_title, transform=ax1.transAxes,
                      fontsize=9, fontweight='bold', ha='center',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7, pad=2))

def create_single_panel(ax, data_dict, panel_type, station_name, period_name, calc_func, colors):
    """Create a single panel of a specific type"""
    
    df = data_dict['data']
    year_columns = data_dict['year_columns']
    
    if panel_type == 'hourly':
        # Hourly Patterns
        for i, year in enumerate(year_columns):
            df_year = df.dropna(subset=[year]).copy()
            df_year['Hour'] = df_year['DateTime'].dt.hour
            df_year['foF2_estimated'] = calc_func(df_year[year])
            hourly_fof2 = df_year.groupby('Hour')['foF2_estimated'].mean()
            
            ax.plot(hourly_fof2.index, hourly_fof2.values,
                    color=colors[i], marker='o', linewidth=1.5, markersize=3,
                    label=f'{int(year)}')
        
        ax.axvspan(6, 18, alpha=0.15, color='yellow')
        ax.axvspan(18, 24, alpha=0.15, color='gray')
        ax.axvspan(0, 6, alpha=0.15, color='gray')
        ax.set_title(f'{station_name} - {period_name}\nHourly Patterns (24h)', 
                    fontsize=18, fontweight='bold', pad=10)
        ax.set_xlabel('Hour (UTC)', fontsize=8)
        ax.set_ylabel('foF2 (MHz)', fontsize=8)
        ax.legend(loc='best', fontsize=6, ncol=4, framealpha=0.8)
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 23)
        ax.set_xticks(range(0, 24, 6))
        
    elif panel_type == 'distribution':
        # Statistical Distribution
        fof2_data = []
        year_labels = []
        
        for year in year_columns:
            df_year = df.dropna(subset=[year]).copy()
            fof2_values = calc_func(df_year[year])
            fof2_data.append(fof2_values)
            year_labels.append(f'{int(year)}')
        
        bp = ax.boxplot(fof2_data, tick_labels=year_labels, patch_artist=True)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_title(f'{station_name} - {period_name}\nfoF2 Distribution', 
                    fontsize=18, fontweight='bold', pad=10)
        ax.set_xlabel('Year', fontsize=8)
        ax.set_ylabel('foF2 (MHz)', fontsize=8)
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.3)
        
    elif panel_type == 'progression':
        # Daily/Temporal Progression
        if 'Day' in str(period_name) or '15-28' in str(period_name) or 'Full' in str(period_name):
            # Daily progression
            for i, year in enumerate(year_columns):
                df_year = df.dropna(subset=[year]).copy()
                df_year['Day'] = df_year['DateTime'].dt.day
                df_year['foF2_estimated'] = calc_func(df_year[year])
                daily_fof2 = df_year.groupby('Day')['foF2_estimated'].mean()
                
                ax.plot(daily_fof2.index, daily_fof2.values,
                        color=colors[i], marker='o', linewidth=1.5, markersize=3,
                        label=f'{int(year)}')
            
            ax.set_xlabel('Day of Period', fontsize=8)
            ax.set_title(f'{station_name} - {period_name}\nDaily Progression', 
                        fontsize=18, fontweight='bold', pad=10)
        else:
            # For April 15th, show 24-hour progression
            for i, year in enumerate(year_columns):
                df_year = df.dropna(subset=[year]).copy()
                df_year['Hour'] = df_year['DateTime'].dt.hour
                df_year['Minute'] = df_year['DateTime'].dt.minute
                df_year['HourDecimal'] = df_year['Hour'] + df_year['Minute'] / 60.0
                df_year['foF2_estimated'] = calc_func(df_year[year])
                df_year = df_year.sort_values('HourDecimal')
                
                ax.plot(df_year['HourDecimal'], df_year['foF2_estimated'],
                        color=colors[i], marker='o', linewidth=1.5, markersize=2,
                        label=f'{int(year)}')
            
            ax.axvspan(6, 18, alpha=0.15, color='yellow')
            ax.axvspan(18, 24, alpha=0.15, color='gray')
            ax.axvspan(0, 6, alpha=0.15, color='gray')
            ax.set_xlabel('Hour', fontsize=8)
            ax.set_title(f'{station_name} - {period_name}\n24h Progression', 
                        fontsize=18, fontweight='bold', pad=10)
            ax.set_xlim(0, 24)
            ax.set_xticks(range(0, 25, 6))
        
        ax.set_ylabel('foF2 (MHz)', fontsize=8)
        ax.legend(loc='best', fontsize=6, ncol=4, framealpha=0.8)
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.3)
        
    elif panel_type == 'nvis':
        # NVIS Frequency Bands
        all_fof2_combined = []
        for year in year_columns:
            df_year = df.dropna(subset=[year]).copy()
            fof2_values = calc_func(df_year[year])
            all_fof2_combined.extend(fof2_values)
        
        avg_fof2_combined = np.mean(all_fof2_combined)
        std_fof2_combined = np.std(all_fof2_combined)
        
        # Plot foF2 range
        ax.axhspan(avg_fof2_combined - std_fof2_combined, avg_fof2_combined + std_fof2_combined,
                    alpha=0.3, color='blue', label=f'foF2: {avg_fof2_combined:.1f}±{std_fof2_combined:.1f}')
        ax.axhline(y=avg_fof2_combined, color='blue', linewidth=2)
        
        # Add NVIS frequency bands
        ax.axhspan(2, 8, alpha=0.2, color='lightgreen', label='Night NVIS')
        ax.axhspan(8, 15, alpha=0.2, color='lightblue', label='Day NVIS')
        
        # Add DGFC frequencies
        ax.axhline(y=7.078, color='red', linewidth=2, linestyle='--', label='7.078 MHz')
        ax.axhline(y=10.130, color='orange', linewidth=2, linestyle='--', label='10.130 MHz')
        
        # Add MUF
        muf_combined = avg_fof2_combined * 3
        ax.axhline(y=muf_combined, color='purple', linewidth=2, linestyle=':',
                   label=f'MUF: {muf_combined:.1f}')
        
        ax.set_title(f'{station_name} - {period_name}\nNVIS vs DGFC', 
                    fontsize=18, fontweight='bold', pad=10)
        ax.set_ylabel('Frequency (MHz)', fontsize=8)
        ax.set_xlim(-0.5, 0.5)
        ax.set_xticks([])
        ax.legend(loc='best', fontsize=6, framealpha=0.8)
        ax.tick_params(labelsize=7)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 40)

def create_all_charts_side_by_side():
    """Create all charts stacked in columns by chart type"""
    
    print("📊 Loading all data...")
    
    # Load all datasets
    datasets = [
        load_data('Darwin', lambda df: df[(df['DateTime'].dt.month == 4) & (df['DateTime'].dt.day == 15)]),
        load_data('Darwin', lambda df: df[(df['DateTime'].dt.month == 4) & 
                                          (df['DateTime'].dt.day >= 15) & 
                                          (df['DateTime'].dt.day <= 28)]),
        load_data('Darwin', lambda df: df[df['DateTime'].dt.month == 4]),
        load_data('Guam', lambda df: df[(df['DateTime'].dt.month == 4) & (df['DateTime'].dt.day == 15)]),
        load_data('Guam', lambda df: df[(df['DateTime'].dt.month == 4) & 
                                        (df['DateTime'].dt.day >= 15) & 
                                        (df['DateTime'].dt.day <= 28)]),
        load_data('Guam', lambda df: df[df['DateTime'].dt.month == 4])
    ]
    
    dataset_info = [
        ('Darwin', 'April 15th', calculate_fof2_from_signal_darwin),
        ('Darwin', 'April 15-28th', calculate_fof2_from_signal_darwin),
        ('Darwin', 'Full April', calculate_fof2_from_signal_darwin),
        ('Guam', 'April 15th', calculate_fof2_from_signal_guam),
        ('Guam', 'April 15-28th', calculate_fof2_from_signal_guam),
        ('Guam', 'Full April', calculate_fof2_from_signal_guam)
    ]
    
    # Check if all data loaded successfully
    for i, (data, (station, period, _)) in enumerate(zip(datasets, dataset_info)):
        if data is None:
            print(f"❌ Failed to load {station} {period} data")
            return
    
    print("✅ All data loaded successfully")
    print("📈 Creating stacked column display...")
    
    # Create color scheme
    colors = plt.cm.viridis(np.linspace(0, 1, 7))  # 7 years
    
    # Create main figure: 7 rows (1 title row + 6 data rows) x 4 columns
    fig = plt.figure(figsize=(28, 40))
    gs = GridSpec(7, 4, figure=fig, hspace=0.35, wspace=0.4, 
                  left=0.08, right=0.94, top=0.99, bottom=0.05,
                  height_ratios=[0.25, 1, 1, 1, 1, 1, 1])
    
    panel_types = ['hourly', 'distribution', 'progression', 'nvis']
    panel_titles = ['Hourly Patterns (24h)', 'foF2 Distribution', 
                    'Temporal Progression', 'NVIS vs DGFC']
    
    # Create column titles in first row
    for col, title in enumerate(panel_titles):
        ax_title = fig.add_subplot(gs[0, col])
        ax_title.axis('off')
        ax_title.text(0.5, 0.5, title, transform=ax_title.transAxes,
                     fontsize=22, fontweight='bold', ha='center', va='center',
                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    # Create all panels in rows 1-6
    all_axes = []
    for row in range(6):
        for col in range(4):
            ax = fig.add_subplot(gs[row+1, col])
            station, period, calc_func = dataset_info[row]
            create_single_panel(ax, datasets[row], panel_types[col], 
                               station, period, calc_func, colors)
            all_axes.append(ax)
    
    # Adjust subplot margins to prevent title overlap with x-axis labels
    for ax in all_axes:
        # Ensure x-axis labels have space and don't overlap with titles below
        ax.tick_params(axis='x', pad=12)
        # Add bottom margin to accommodate x-axis labels
        ax.margins(y=0.05, x=0.05)
    
    # Main title removed per user request
    
    # Save the figure as PNG
    output_file = "All_foF2_Charts_Stacked_Columns_2017-2023.png"
    plt.savefig(output_file, dpi=160, bbox_inches='tight', format='png')
    print(f"✅ Saved as PNG: {output_file}")
    
    plt.show()

def main():
    """Main function"""
    create_all_charts_side_by_side()

if __name__ == "__main__":
    main()
