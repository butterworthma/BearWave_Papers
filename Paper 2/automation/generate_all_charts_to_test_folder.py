#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate ALL foF2 Charts to Desktop/test Folder
===============================================

This script generates all foF2 analysis charts using the standardized
layout enforcer and saves them to ~/Desktop/test/ folder.

Author: Research Team
License: MIT
"""

import subprocess
import os
import sys
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_fof2_script_with_test_folder(script_name, description):
    """Run a foF2 analysis script and capture its output"""
    
    script_path = f"Mark_paper_2/{script_name}"
    
    print(f"\n📊 Running: {script_name}")
    print(f"📝 {description}")
    print("-" * 60)
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_name}")
        return False
    
    try:
        # Run the script using the virtual environment
        result = subprocess.run([
            "python",
            script_path
        ], 
        cwd="/Users/samanthabutterworth/PycharmProjects/pythonProject3",
        capture_output=True, 
        text=True, 
        timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {script_name}")
            
            # Show key output lines
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'Saved' in line or 'Created' in line or 'test folder' in line:
                        print(f"   {line}")
            
            return True
        else:
            print(f"❌ FAILED: {script_name}")
            if result.stderr:
                error_lines = result.stderr.strip().split('\n')
                for line in error_lines[-3:]:  # Show last 3 error lines
                    print(f"   Error: {line}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {script_name} (took longer than 5 minutes)")
        return False
    except Exception as e:
        print(f"❌ EXCEPTION: {script_name} - {e}")
        return False

def generate_all_fof2_charts():
    """Generate all foF2 charts and save to test folder"""
    
    print("🎯 GENERATING ALL foF2 CHARTS TO DESKTOP/test FOLDER")
    print("="*65)
    print("This will create all foF2 analysis charts with standardized")
    print("layout and save them to ~/Desktop/test/ folder.")
    print()
    
    # Create test folder if it doesn't exist
    test_folder = "output"
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
        print(f"📁 Created test folder: {test_folder}")
    else:
        print(f"📁 Using existing test folder: {test_folder}")
    
    # List of all foF2 scripts to run
    scripts_to_run = [
        {
            'file': 'guam_april15-28_fof2_7years.py',
            'description': 'Guam April 15-28 (7 Years) - Northern Pacific ionospheric conditions'
        },
        {
            'file': 'guam_april15_fof2_7years.py',
            'description': 'Guam April 15th (7 Years) - Single day analysis across years'
        },
        {
            'file': 'guam_fof2_april.py',
            'description': 'Guam Full April (7 Years) - Complete month analysis'
        },
        {
            'file': 'darwin_april15-28_fof2_7years.py',
            'description': 'Darwin April 15-28 (7 Years) - Southern ionospheric conditions'
        },
        {
            'file': 'darwin_april15_fof2_7years.py',
            'description': 'Darwin April 15th (7 Years) - Single day comparative analysis'
        },
        {
            'file': 'darwin_fof2_april.py',
            'description': 'Darwin Full April (7 Years) - Complete month comparative analysis'
        }
    ]
    
    # Also generate test charts using the standardized layout enforcer
    print(f"\n🧪 First, generating test charts using standardized layout enforcer...")
    try:
        from generate_desktop_charts import create_multiple_test_charts
        create_multiple_test_charts()
        print("✅ Test charts generated successfully")
    except Exception as e:
        print(f"⚠️ Could not generate test charts: {e}")
    
    start_time = datetime.now()
    successful = []
    failed = []
    
    # Run each foF2 script
    for i, script_info in enumerate(scripts_to_run, 1):
        print(f"\n[{i}/{len(scripts_to_run)}] Processing...")
        
        success = run_fof2_script_with_test_folder(script_info['file'], script_info['description'])
        
        if success:
            successful.append(script_info['file'])
        else:
            failed.append(script_info['file'])
    
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n🎉 CHART GENERATION COMPLETE!")
    print("="*40)
    print(f"⏱️  Total time: {duration}")
    print(f"✅ Successful: {len(successful)}/{len(scripts_to_run)}")
    print(f"❌ Failed: {len(failed)}/{len(scripts_to_run)}")
    
    if successful:
        print(f"\n✅ SUCCESSFULLY GENERATED:")
        for script in successful:
            print(f"  • {script}")
    
    if failed:
        print(f"\n❌ FAILED TO GENERATE:")
        for script in failed:
            print(f"  • {script}")
    
    # Check what files were created
    check_test_folder_contents()

def check_test_folder_contents():
    """Check and list contents of the test folder"""
    
    print(f"\n📁 CHECKING TEST FOLDER CONTENTS")
    print("="*35)
    
    test_folder = "output"
    
    if not os.path.exists(test_folder):
        print("❌ Test folder does not exist")
        return
    
    # List all PNG files in test folder
    png_files = [f for f in os.listdir(test_folder) if f.endswith('.png')]
    
    if png_files:
        print(f"📊 Found {len(png_files)} PNG files in test folder:")
        print()
        
        # Group by type
        new_standard_files = [f for f in png_files if f.startswith('new_standard_')]
        other_files = [f for f in png_files if not f.startswith('new_standard_')]
        
        if new_standard_files:
            print(f"🎯 NEW STANDARD CHARTS ({len(new_standard_files)}):")
            for file in sorted(new_standard_files):
                file_path = os.path.join(test_folder, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                print(f"  • {file} ({file_size:.1f} MB)")
            print()
        
        if other_files:
            print(f"📊 OTHER CHARTS ({len(other_files)}):")
            for file in sorted(other_files):
                file_path = os.path.join(test_folder, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                print(f"  • {file} ({file_size:.1f} MB)")
            print()
        
        print(f"📁 Test folder location: {test_folder}")
        print(f"🖼️ To view all charts: open {test_folder}")
        
    else:
        print("❌ No PNG files found in test folder")
        print("   Charts may have been saved elsewhere or generation failed")

def clean_test_folder():
    """Clean the test folder (remove all PNG files)"""
    
    print("🧹 CLEANING TEST FOLDER")
    print("="*25)
    
    test_folder = "output"
    
    if not os.path.exists(test_folder):
        print("❌ Test folder does not exist")
        return
    
    png_files = [f for f in os.listdir(test_folder) if f.endswith('.png')]
    
    if not png_files:
        print("✅ Test folder is already clean (no PNG files)")
        return
    
    print(f"⚠️ Found {len(png_files)} PNG files to remove:")
    for file in png_files:
        print(f"  • {file}")
    
    response = input(f"\nRemove all {len(png_files)} PNG files? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        removed_count = 0
        for file in png_files:
            try:
                file_path = os.path.join(test_folder, file)
                os.remove(file_path)
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {file}: {e}")
        
        print(f"✅ Removed {removed_count} PNG files from test folder")
    else:
        print("❌ Cleaning cancelled")

def main():
    """Main function"""
    
    print("🖥️ foF2 CHART GENERATOR FOR DESKTOP/test FOLDER")
    print("="*50)
    print("Options:")
    print("1. Generate all foF2 charts to test folder")
    print("2. Check test folder contents")
    print("3. Clean test folder (remove PNG files)")
    print("4. Open test folder in Finder")
    print()
    
    choice = input("Select option (1-4, default 1): ").strip()
    
    if choice == "2":
        check_test_folder_contents()
    elif choice == "3":
        clean_test_folder()
    elif choice == "4":
        test_folder = "output"
        try:
            subprocess.run(['open', test_folder], check=True)
            print(f"✅ Opened test folder in Finder")
        except Exception as e:
            print(f"❌ Error opening test folder: {e}")
    else:
        # Default: generate all charts
        generate_all_fof2_charts()

if __name__ == "__main__":
    main()
