#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standardized Report Format for foF2 Analysis
============================================

Common formatting functions to ensure all foF2 analysis charts 
have consistent appearance for professional reports.

Author: Research Team
License: MIT
"""

import matplotlib.pyplot as plt
import numpy as np

# Standardized report configuration
REPORT_CONFIG = {
    'figure_size': (16, 12),
    'title_fontsize': 16,
    'subtitle_fontsize': 14,
    'label_fontsize': 12,
    'legend_fontsize': 10,
    'dpi': 160,
    'colors': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'],
    'grid_alpha': 0.3,
    'line_width': 2,
    'marker_size': 4
}

def create_standardized_4panel_chart(station_name, period_name, year_range):
    """
    Create standardized 4-panel chart layout for foF2 analysis

    STANDARDIZED LAYOUT:
    - Top-Left (0,0):     Hourly Patterns (24h diurnal cycle)
    - Top-Right (0,1):    Statistical Distribution (box plots by year)
    - Bottom-Left (1,0):  Temporal Progression (daily/period trends)
    - Bottom-Right (1,1): NVIS Frequency Bands (with DGFC frequencies)

    Parameters:
    - station_name: Name of the monitoring station
    - period_name: Time period being analyzed
    - year_range: Range of years in analysis

    Returns:
    - fig, axes: Figure and axes objects
    """

    fig, axes = plt.subplots(2, 2, figsize=REPORT_CONFIG['figure_size'])

    # Standardized main title
    main_title = f'Ionospheric foF2 Critical Frequency Analysis\n{station_name} Station - {period_name} ({year_range})'
    fig.suptitle(main_title,
                fontsize=REPORT_CONFIG['title_fontsize'],
                fontweight='bold',
                y=0.95)

    return fig, axes

def format_daily_progression_subplot(ax, title="Daily Average foF2 Progression"):
    """Format the daily progression subplot (top-left)"""
    ax.set_title(title, fontsize=REPORT_CONFIG['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel('Day of Period', fontsize=REPORT_CONFIG['label_fontsize'])
    ax.set_ylabel('Daily Average foF2 (MHz)', fontsize=REPORT_CONFIG['label_fontsize'])
    ax.legend(loc='upper right', fontsize=REPORT_CONFIG['legend_fontsize'])
    ax.grid(True, alpha=REPORT_CONFIG['grid_alpha'])

def format_hourly_patterns_subplot(ax, title="Hourly Patterns (24h Average)"):
    """Format the hourly patterns subplot (top-right)"""
    # Add day/night shading
    ax.axvspan(6, 18, alpha=0.15, color='yellow', label='Daylight')
    ax.axvspan(18, 24, alpha=0.15, color='gray', label='Night')
    ax.axvspan(0, 6, alpha=0.15, color='gray')
    
    ax.set_title(title, fontsize=REPORT_CONFIG['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel('Hour of Day (UTC)', fontsize=REPORT_CONFIG['label_fontsize'])
    ax.set_ylabel('Average foF2 (MHz)', fontsize=REPORT_CONFIG['label_fontsize'])
    ax.legend(loc='upper right', fontsize=REPORT_CONFIG['legend_fontsize'])
    ax.grid(True, alpha=REPORT_CONFIG['grid_alpha'])
    ax.set_xlim(0, 23)
    ax.set_xticks(range(0, 24, 6))

def format_statistical_distribution_subplot(ax, title="foF2 Distribution by Year"):
    """Format the statistical distribution subplot (bottom-left)"""
    ax.set_title(title, fontsize=REPORT_CONFIG['subtitle_fontsize'], fontweight='bold')
    ax.set_xlabel('Year', fontsize=REPORT_CONFIG['label_fontsize'])
    ax.set_ylabel('foF2 (MHz)', fontsize=REPORT_CONFIG['label_fontsize'])
    ax.grid(True, alpha=REPORT_CONFIG['grid_alpha'])

def format_nvis_frequency_subplot(ax, avg_fof2, std_fof2, title="foF2 vs NVIS Frequency Bands"):
    """Format the NVIS frequency bands subplot (bottom-right)"""
    
    # Plot foF2 range
    ax.axhspan(avg_fof2 - std_fof2, avg_fof2 + std_fof2,
               alpha=0.3, color='blue', label=f'foF2: {avg_fof2:.1f}±{std_fof2:.1f} MHz')
    ax.axhline(y=avg_fof2, color='blue', linewidth=2)
    
    # Add NVIS frequency bands
    ax.axhspan(2, 8, alpha=0.2, color='lightgreen', label='Night NVIS (2-8 MHz)')
    ax.axhspan(8, 15, alpha=0.2, color='lightblue', label='Day NVIS (8-15 MHz)')
    
    # Add DGFC frequencies
    ax.axhline(y=7.078, color='red', linewidth=2, linestyle='--', label='DGFC 7.078 MHz')
    ax.axhline(y=10.130, color='orange', linewidth=2, linestyle='--', label='DGFC 10.130 MHz')
    
    # Add MUF
    muf = avg_fof2 * 3
    ax.axhline(y=muf, color='purple', linewidth=2, linestyle=':',
               label=f'MUF: {muf:.1f} MHz')
    
    ax.set_title(title, fontsize=REPORT_CONFIG['subtitle_fontsize'], fontweight='bold')
    ax.set_ylabel('Frequency (MHz)', fontsize=REPORT_CONFIG['label_fontsize'])
    ax.set_xlabel('NVIS Frequency Bands', fontsize=REPORT_CONFIG['label_fontsize'])
    ax.legend(loc='upper right', fontsize=REPORT_CONFIG['legend_fontsize'])
    ax.grid(True, alpha=REPORT_CONFIG['grid_alpha'])
    ax.set_ylim(0, max(25, muf + 5))
    
    # Remove x-axis ticks for frequency bands plot
    ax.set_xticks([])

def apply_standardized_layout(fig):
    """Apply standardized layout settings"""
    plt.tight_layout()
    plt.subplots_adjust(top=0.90, hspace=0.3, wspace=0.3)

def save_standardized_chart(fig, filename, output_dir="/Users/samanthabutterworth/PycharmProjects/pythonProject3/"):
    """Save chart with standardized settings"""
    output_path = f"{output_dir}{filename}.png"
    fig.savefig(output_path, dpi=REPORT_CONFIG['dpi'], bbox_inches='tight')
    print(f"✅ Saved: {filename}.png")
    return output_path

def get_standardized_colors():
    """Get standardized color palette for consistency"""
    return REPORT_CONFIG['colors']

def create_standardized_filename(station, period, analysis_type, timestamp):
    """Create standardized filename format"""
    # Clean up station and period names
    station_clean = station.replace(' ', '_').replace('-', '_')
    period_clean = period.replace(' ', '_').replace('-', '_')
    
    return f"foF2_Analysis_{station_clean}_{period_clean}_{analysis_type}_{timestamp}"

# Example usage template
def example_standardized_chart():
    """
    Example of how to use the standardized format
    """
    
    # Create standardized chart
    fig, axes = create_standardized_4panel_chart("Guam", "April 15-28", "2017-2023")
    
    # Format each subplot
    format_daily_progression_subplot(axes[0, 0])
    format_hourly_patterns_subplot(axes[0, 1])
    format_statistical_distribution_subplot(axes[1, 0])
    format_nvis_frequency_subplot(axes[1, 1], avg_fof2=8.5, std_fof2=2.1)
    
    # Apply layout and save
    apply_standardized_layout(fig)
    save_standardized_chart(fig, "Example_Standardized_Chart")
    
    plt.show()
    plt.close()

if __name__ == "__main__":
    example_standardized_chart()
