#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Run and Show Charts
==========================

Run one foF2 script at a time and show the results.

Author: Research Team
License: MIT
"""

import subprocess
import os
import glob

def run_script_and_show_files(script_name):
    """Run a script and show what files were created"""
    
    script_path = f"Mark_paper_2/{script_name}"
    
    print(f"🚀 Running: {script_name}")
    print("="*50)
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_name}")
        return
    
    # Get list of PNG files before running
    before_files = set(glob.glob("*.png"))
    
    try:
        # Run the script
        result = subprocess.run([
            "python",
            script_path
        ], 
        cwd="/Users/samanthabutterworth/PycharmProjects/pythonProject3",
        capture_output=True, 
        text=True, 
        timeout=120)
        
        if result.returncode == 0:
            print("✅ Script completed successfully!")
            
            # Get list of PNG files after running
            after_files = set(glob.glob("*.png"))
            new_files = after_files - before_files
            
            if new_files:
                print(f"\n📊 NEW CHARTS CREATED:")
                for file in sorted(new_files):
                    file_size = os.path.getsize(file) / (1024 * 1024)
                    print(f"  • {file} ({file_size:.1f} MB)")
                
                print(f"\n🖼️ TO VIEW CHARTS:")
                for file in sorted(new_files):
                    print(f"  open {file}")
                
                # Try to open the first new file
                if new_files:
                    first_file = sorted(new_files)[0]
                    print(f"\n🎯 Opening: {first_file}")
                    try:
                        subprocess.run(['open', first_file])
                        print("✅ Chart opened in Preview")
                    except:
                        print("❌ Could not open automatically")
            else:
                print("⚠️ No new chart files detected")
                
        else:
            print("❌ Script failed!")
            if result.stderr:
                print(f"Error: {result.stderr}")
                
    except subprocess.TimeoutExpired:
        print("⏰ Script timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    
    scripts = [
        "guam_april15-28_fof2_7years.py",
        "guam_april15_fof2_7years.py", 
        "guam_fof2_april.py",
        "darwin_april15-28_fof2_7years.py",
        "darwin_april15_fof2_7years.py",
        "darwin_fof2_april.py"
    ]
    
    print("🎯 SIMPLE foF2 CHART GENERATOR")
    print("="*35)
    print("Select a script to run:")
    print()
    
    for i, script in enumerate(scripts, 1):
        name = script.replace('_', ' ').replace('.py', '').title()
        print(f"  {i}. {name}")
    
    print(f"  {len(scripts)+1}. Run all scripts")
    print()
    
    try:
        choice = input(f"Select option (1-{len(scripts)+1}): ").strip()
        
        if choice == str(len(scripts)+1):
            # Run all scripts
            for script in scripts:
                run_script_and_show_files(script)
                print("\n" + "="*60 + "\n")
        else:
            # Run selected script
            script_index = int(choice) - 1
            if 0 <= script_index < len(scripts):
                run_script_and_show_files(scripts[script_index])
            else:
                print("❌ Invalid selection")
                
    except ValueError:
        print("❌ Invalid input")
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")

if __name__ == "__main__":
    main()
