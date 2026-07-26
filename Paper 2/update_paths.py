#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Personal Paths to Relative Paths
=======================================

This script automatically updates all hardcoded personal paths in the 
ionospheric foF2 analysis scripts to use relative paths that work 
in any environment.

Author: Research Team
License: MIT
"""

import os
import glob
import re
from pathlib import Path

def update_paths_in_file(filepath):
    """Update hardcoded paths in a single file"""
    
    print(f"🔧 Updating: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Path replacements
        replacements = [
            # NVIS data file paths
            (r'/Users/[^/]+/Desktop/Marks_phD/NVIS_data\.xlsx', 'data/NVIS_data.xlsx'),
            (r'/Users/[^/]+/Desktop/NVIS_data\.xlsx', 'data/NVIS_data.xlsx'),

            # Output directory paths
            (r'/Users/[^/]+/Desktop/test/test2/corrected', 'output/corrected'),
            (r'/Users/[^/]+/Desktop/test/test2', 'output'),
            (r'/Users/[^/]+/Desktop/test', 'output'),
            (r'/Users/samanthabutterworth/Desktop/Marks_phD', 'output'),
            
            # Desktop path (general)
            (r'/Users/samanthabutterworth/Desktop', 'output'),
            
            # Project path references
            (r'/Users/samanthabutterworth/PycharmProjects/pythonProject3/Mark_paper_2/', ''),
            (r'/Users/samanthabutterworth/PycharmProjects/pythonProject3/venv/bin/python', 'python'),
            
            # Other data file paths
            (r'/Users/samanthabutterworth/Desktop/final7\.1_new\.xlsx', 'data/final7.1_new.xlsx'),
            (r'/Users/samanthabutterworth/Desktop/Marks_phD/final_7\.1\.xlsx', 'data/final_7.1.xlsx'),
            (r'/Users/samanthabutterworth/Desktop/Marks_phD/final_10\.130\.xlsx', 'data/final_10.130.xlsx'),
            (r'/Users/samanthabutterworth/Desktop/Marks_phD/5_GHZ_Standardized_data_preview__first_200_rows_\.csv', 'data/5_GHZ_Standardized_data_preview__first_200_rows_.csv'),
        ]
        
        # Apply replacements
        changes_made = 0
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                changes_made += 1
                content = new_content
                print(f"  ✅ Replaced: {pattern} → {replacement}")
        
        # Special case: Update save functions to use output directory
        if 'save_standardized_chart' in content:
            # Update the save function to use output directory
            save_function_pattern = r'desktop_path = "/Users/samanthabutterworth/Desktop"\s*\n\s*test_folder = os\.path\.join\(desktop_path, "test"\)'
            save_function_replacement = 'output_dir = "output"\n    if not os.path.exists(output_dir):\n        os.makedirs(output_dir)\n    test_folder = output_dir'
            
            new_content = re.sub(save_function_pattern, save_function_replacement, content)
            if new_content != content:
                content = new_content
                changes_made += 1
                print(f"  ✅ Updated save function to use output directory")
        
        # Write back if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  📝 {changes_made} changes saved to {filepath}")
        else:
            print(f"  ℹ️  No changes needed in {filepath}")
            
        return changes_made
        
    except Exception as e:
        print(f"  ❌ Error updating {filepath}: {e}")
        return 0

def create_output_directories():
    """Create necessary output directories"""
    
    directories = [
        'output',
        'output/corrected',
        'data'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"📁 Directory exists: {directory}")

def main():
    """Main function to update all paths"""
    
    print("🚀 UPDATING PERSONAL PATHS TO RELATIVE PATHS")
    print("=" * 50)
    
    # Create output directories
    print("\n📁 Creating output directories...")
    create_output_directories()
    
    # Find all Python files
    python_files = []
    
    # Search in all subdirectories
    for pattern in ['**/*.py']:
        for filepath in glob.glob(pattern, recursive=True):
            # Skip this update script itself
            if not filepath.endswith('update_paths.py'):
                python_files.append(filepath)
    
    print(f"\n🔍 Found {len(python_files)} Python files to update:")
    for f in python_files:
        print(f"  • {f}")
    
    # Update each file
    print(f"\n🔧 Updating paths in files...")
    total_changes = 0
    
    for filepath in python_files:
        changes = update_paths_in_file(filepath)
        total_changes += changes
    
    # Summary
    print(f"\n🎉 PATH UPDATE COMPLETE!")
    print("=" * 30)
    print(f"📊 Files processed: {len(python_files)}")
    print(f"🔧 Total changes made: {total_changes}")
    
    print(f"\n📋 UPDATED PATHS:")
    print(f"  • NVIS data: data/NVIS_data.xlsx")
    print(f"  • Output charts: output/")
    print(f"  • Corrected charts: output/corrected/")
    
    print(f"\n✅ All scripts now use relative paths!")
    print(f"📁 Make sure your data files are in the 'data/' directory")
    print(f"📊 Charts will be saved to the 'output/' directory")
    
    # Test one script
    print(f"\n🧪 TESTING UPDATED SCRIPT:")
    print(f"Try running: python generators/generate_corrected_charts.py")

if __name__ == "__main__":
    main()
