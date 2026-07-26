#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run All foF2 Scripts to Generate 2x2 Charts
===========================================

Simple script to execute all foF2 analysis scripts and generate
the standardized 2x2 combined overview charts for reports.

Author: Research Team
License: MIT
"""

import subprocess
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob

# Scripts to run for 2x2 chart generation
SCRIPTS_TO_RUN = [
    {
        'file': 'guam_april15-28_fof2_7years.py',
        'name': 'Guam April 15-28 (7 Years)',
        'description': 'Northern Pacific ionospheric conditions'
    },
    {
        'file': 'guam_april15_fof2_7years.py', 
        'name': 'Guam April 15th (7 Years)',
        'description': 'Single day analysis across years'
    },
    {
        'file': 'guam_fof2_april.py',
        'name': 'Guam Full April (7 Years)', 
        'description': 'Complete month analysis'
    },
    {
        'file': 'darwin_april15-28_fof2_7years.py',
        'name': 'Darwin April 15-28 (7 Years)',
        'description': 'Southern ionospheric conditions'
    },
    {
        'file': 'darwin_april15_fof2_7years.py',
        'name': 'Darwin April 15th (7 Years)',
        'description': 'Single day comparative analysis'
    },
    {
        'file': 'darwin_fof2_april.py',
        'name': 'Darwin Full April (7 Years)',
        'description': 'Complete month comparative analysis'
    }
]

def display_latest_chart(script_info):
    """Display the most recently created chart for a script"""

    # Look for the expected chart file pattern
    station = "Guam" if "guam" in script_info['file'] else "Darwin"

    if "april15-28" in script_info['file']:
        pattern = f"{station}_foF2_April_15-28_Combined_Overview_*.png"
    elif "april15_" in script_info['file']:
        pattern = f"{station}_foF2_April_15th_Combined_Overview_*.png"
    elif "april" in script_info['file']:
        pattern = f"{station}_foF2_April_Combined_Overview_*.png"
    else:
        pattern = f"{station}_foF2_*_Combined_Overview_*.png"

    # Find matching files
    chart_dir = "/Users/samanthabutterworth/PycharmProjects/pythonProject3/"
    matching_files = glob.glob(os.path.join(chart_dir, pattern))

    if not matching_files:
        print(f"   ⚠️ No chart file found for {script_info['name']}")
        return False

    # Get the most recent file
    latest_file = max(matching_files, key=os.path.getmtime)

    try:
        # Load and display the image
        img = mpimg.imread(latest_file)

        # Create figure
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111)

        # Display image
        ax.imshow(img)
        ax.axis('off')

        # Add title
        fig.suptitle(f'{script_info["name"]}\n{script_info["description"]}',
                    fontsize=16, fontweight='bold', y=0.95)

        # Add file info
        filename = os.path.basename(latest_file)
        file_size = os.path.getsize(latest_file) / (1024 * 1024)
        plt.figtext(0.02, 0.02, f'File: {filename} ({file_size:.1f} MB)',
                   fontsize=10, alpha=0.7)

        plt.tight_layout()
        plt.subplots_adjust(top=0.88)

        # Show the plot
        plt.show()

        print(f"   📊 Displayed: {filename}")
        return True

    except Exception as e:
        print(f"   ❌ Error displaying chart: {e}")
        return False

def run_single_script(script_info):
    """Run a single foF2 analysis script"""
    
    script_file = script_info['file']
    script_name = script_info['name']
    script_path = f"Mark_paper_2/{script_file}"
    
    print(f"\n📊 Running: {script_name}")
    print(f"📝 {script_info['description']}")
    print(f"🔧 File: {script_file}")
    print("-" * 60)
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_file}")
        return False
    
    try:
        # Run the script
        result = subprocess.run([
            "python",
            script_path
        ], 
        cwd="/Users/samanthabutterworth/PycharmProjects/pythonProject3",
        capture_output=True, 
        text=True, 
        timeout=180)  # 3 minute timeout per script
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {script_name}")

            # Show key output lines
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'Saved:' in line or 'Creating' in line or 'COMPLETE' in line:
                        print(f"   {line}")

            # Display the generated chart
            print(f"   🖼️ Displaying chart...")
            display_success = display_latest_chart(script_info)

            if display_success:
                input("   ⏸️ Press Enter to continue to next chart...")

            return True
        else:
            print(f"❌ FAILED: {script_name}")
            if result.stderr:
                error_lines = result.stderr.strip().split('\n')
                for line in error_lines[-3:]:  # Show last 3 error lines
                    print(f"   Error: {line}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {script_name} (took longer than 3 minutes)")
        return False
    except Exception as e:
        print(f"❌ EXCEPTION: {script_name} - {e}")
        return False

def main():
    """Main function to run all scripts"""
    
    print("🎯 GENERATING AND DISPLAYING ALL 2x2 foF2 ANALYSIS CHARTS")
    print("="*60)
    print("This will create standardized 2x2 combined overview charts")
    print("for all stations and time periods, and display each one")
    print("as it's generated. Press Enter after viewing each chart.")
    print()
    
    start_time = datetime.now()
    successful = []
    failed = []
    
    # Run each script
    for i, script_info in enumerate(SCRIPTS_TO_RUN, 1):
        print(f"\n[{i}/{len(SCRIPTS_TO_RUN)}] Processing...")
        
        success = run_single_script(script_info)
        
        if success:
            successful.append(script_info['name'])
        else:
            failed.append(script_info['name'])
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n🎉 CHART GENERATION COMPLETE!")
    print("="*40)
    print(f"⏱️  Total time: {duration}")
    print(f"✅ Successful: {len(successful)}/{len(SCRIPTS_TO_RUN)}")
    print(f"❌ Failed: {len(failed)}/{len(SCRIPTS_TO_RUN)}")
    
    if successful:
        print(f"\n✅ SUCCESSFULLY GENERATED:")
        for name in successful:
            print(f"  • {name}")
    
    if failed:
        print(f"\n❌ FAILED TO GENERATE:")
        for name in failed:
            print(f"  • {name}")
    
    print(f"\n📁 Charts saved to:")
    print(f"   /Users/samanthabutterworth/PycharmProjects/pythonProject3/")
    
    print(f"\n📊 EXPECTED 2x2 CHART FILES (Combined Script Naming):")
    expected_charts = [
        "Combined_Script_Guam_April_15-28_2x2_Analysis.png",
        "Combined_Script_Guam_April_15th_2x2_Analysis.png",
        "Combined_Script_Guam_Full_April_2x2_Analysis.png",
        "Combined_Script_Darwin_April_15-28_2x2_Analysis.png",
        "Combined_Script_Darwin_April_15th_2x2_Analysis.png",
        "Combined_Script_Darwin_Full_April_2x2_Analysis.png"
    ]
    
    for chart in expected_charts:
        print(f"  • {chart}")
    
    print(f"\n🎯 2x2 CHART LAYOUT:")
    print("  Top-Left:     Daily Average foF2 Progression")
    print("  Top-Right:    Hourly Patterns (24h with day/night)")
    print("  Bottom-Left:  foF2 Distribution by Year (box plots)")
    print("  Bottom-Right: foF2 vs NVIS Frequency Bands")
    
    print(f"\n💡 READY FOR REPORTS:")
    print("  All charts now have consistent 2x2 layout and can be")
    print("  directly used in research reports and presentations.")

if __name__ == "__main__":
    main()
