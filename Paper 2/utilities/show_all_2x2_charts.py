#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Show All Existing 2x2 Charts
============================

Opens all existing 2x2 combined overview charts at once.

Author: Research Team
License: MIT
"""

import subprocess
import os
import glob
from datetime import datetime

def show_all_existing_charts():
    """Open all existing 2x2 combined overview charts"""
    
    print("🖼️  SHOWING ALL EXISTING 2x2 CHARTS")
    print("="*45)
    
    # Find all combined overview charts in the main project directory
    base_dir = "/Users/samanthabutterworth/PycharmProjects/pythonProject3/"
    chart_patterns = [
        "*Combined_Overview*.png",
        "*_Combined_*.png",
        "foF2_Analysis_*.png"
    ]

    all_charts = []
    for pattern in chart_patterns:
        full_pattern = os.path.join(base_dir, pattern)
        charts = glob.glob(full_pattern)
        all_charts.extend(charts)
    
    # Remove duplicates and sort
    all_charts = sorted(list(set(all_charts)))
    
    if not all_charts:
        print("❌ No 2x2 combined overview charts found!")
        print("Run the foF2 analysis scripts first to generate them.")
        return
    
    print(f"📊 Found {len(all_charts)} combined overview charts:")
    print()
    
    # List all charts with details
    for i, chart in enumerate(all_charts, 1):
        file_size = os.path.getsize(chart) / (1024 * 1024)  # MB
        mod_time = datetime.fromtimestamp(os.path.getmtime(chart)).strftime('%Y-%m-%d %H:%M')
        chart_name = os.path.basename(chart)
        
        # Determine chart type
        if "Darwin" in chart_name:
            station = "🇦🇺 Darwin"
        elif "Guam" in chart_name:
            station = "🇺🇸 Guam"
        else:
            station = "📊 Analysis"

        if "April_15-28" in chart_name or "April_15_28" in chart_name:
            period = "April 15-28"
        elif "April_15th" in chart_name or "April_15_" in chart_name:
            period = "April 15th"
        elif "April" in chart_name:
            period = "Full April"
        elif "NVIS" in chart_name:
            period = "NVIS Analysis"
        else:
            period = "Multi-period"

        print(f"  {i:2d}. {station} - {period}")
        print(f"      📁 {chart_name}")
        print(f"      📏 {file_size:.1f} MB, modified: {mod_time}")
        print()
    
    # Open all charts at once
    print("🚀 Opening all charts in Preview...")
    
    try:
        # Open all charts with one command
        cmd = ['open'] + all_charts
        subprocess.run(cmd, check=True)
        
        print("✅ All charts opened successfully!")
        print()
        print("📋 CHART LAYOUT (2x2 Grid):")
        print("  Top-Left:     Daily Average foF2 Progression")
        print("  Top-Right:    Hourly Patterns (24h with day/night)")
        print("  Bottom-Left:  foF2 Distribution by Year (box plots)")
        print("  Bottom-Right: foF2 vs NVIS Frequency Bands")
        print()
        print("💡 TIP: Use Preview's thumbnail view to see all charts at once!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error opening charts: {e}")
        print("\n🔧 Manual commands to open charts:")
        for chart in all_charts:
            print(f"  open '{chart}'")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def show_specific_charts():
    """Show charts by category"""
    
    print("📊 CHART CATEGORIES")
    print("="*25)
    print("1. Darwin Station Charts")
    print("2. Guam Station Charts") 
    print("3. April 15-28 Period Charts")
    print("4. April 15th Charts")
    print("5. Full April Charts")
    print("6. All Charts")
    print()
    
    choice = input("Select category (1-6, default 6): ").strip()
    
    base_dir = "/Users/samanthabutterworth/PycharmProjects/pythonProject3/"

    if choice == "1":
        pattern = "Darwin*Combined_Overview*.png"
    elif choice == "2":
        pattern = "Guam*Combined_Overview*.png"
    elif choice == "3":
        pattern = "*April_15-28*Combined_Overview*.png"
    elif choice == "4":
        pattern = "*April_15th*Combined_Overview*.png"
    elif choice == "5":
        pattern = "*April*Combined_Overview*.png"
    else:
        show_all_existing_charts()
        return

    full_pattern = os.path.join(base_dir, pattern)
    charts = glob.glob(full_pattern)
    
    if charts:
        print(f"\n📊 Opening {len(charts)} charts...")
        try:
            subprocess.run(['open'] + charts, check=True)
            print("✅ Charts opened!")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ No charts found for this category")

def main():
    """Main function"""
    
    print("🎯 2x2 CHART VIEWER")
    print("="*25)
    print("Options:")
    print("1. Show all existing 2x2 charts")
    print("2. Show charts by category")
    print("3. List chart files only")
    print()
    
    choice = input("Select option (1-3, default 1): ").strip()
    
    if choice == "2":
        show_specific_charts()
    elif choice == "3":
        # Just list the files
        base_dir = "/Users/samanthabutterworth/PycharmProjects/pythonProject3/"
        charts = glob.glob(os.path.join(base_dir, "*Combined_Overview*.png"))
        charts.extend(glob.glob(os.path.join(base_dir, "foF2_Analysis_*.png")))
        if charts:
            print(f"\n📋 Found {len(charts)} combined overview charts:")
            for chart in sorted(charts):
                chart_name = os.path.basename(chart)
                print(f"  • {chart_name}")
        else:
            print("❌ No combined overview charts found")
    else:
        show_all_existing_charts()

if __name__ == "__main__":
    main()
