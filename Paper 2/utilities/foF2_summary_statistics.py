#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
foF2 Summary Statistics Display
===============================

Displays key foF2 statistics for Darwin and Guam across different time periods:
- April 15th (7 years)
- April 15-28th (7 years)
- Full April (7 years)

Author: Research Team
License: MIT
"""

import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path to import from analysis scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration
NVIS_DATA_FILE = "data/NVIS_data.xlsx"

def calculate_fof2_from_signal_darwin(signal_db, frequency_mhz=7.0):
    """Estimate foF2 from signal strength for Darwin"""
    baseline_fof2 = 9.0  # Typical April value for Darwin latitude
    signal_factor = signal_db / 12.0
    estimated_fof2 = baseline_fof2 + signal_factor
    return np.clip(estimated_fof2, 3.0, 15.0)

def calculate_fof2_from_signal_guam(signal_db, frequency_mhz=7.0):
    """Estimate foF2 from signal strength for Guam"""
    baseline_fof2 = 10.5  # Typical April value for Guam latitude
    signal_factor = signal_db / 10.0
    estimated_fof2 = baseline_fof2 + signal_factor
    return np.clip(estimated_fof2, 4.0, 18.0)

def load_darwin_april15_data():
    """Load Darwin data for April 15th across 7 years"""
    if not os.path.exists(NVIS_DATA_FILE):
        return None
    
    try:
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=None)
        
        # Find header row
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            return None
        
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=header_row, skiprows=0)
        df = df.dropna(how='all')
        
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for April 15th only
        df_april15 = df[(df['DateTime'].dt.month == 4) & (df['DateTime'].dt.day == 15)].copy()
        
        # Identify year columns (2017-2023)
        year_columns = []
        for col in df_april15.columns:
            if col not in ['DATE', 'TIME', 'DateTime'] and pd.api.types.is_numeric_dtype(df_april15[col]):
                if isinstance(col, (int, float)) and 2017 <= col <= 2023:
                    year_columns.append(col)
        
        return {'data': df_april15, 'year_columns': year_columns}
    except Exception as e:
        print(f"Error loading Darwin April 15th data: {e}")
        return None

def load_darwin_april15_28_data():
    """Load Darwin data for April 15-28th across 7 years"""
    if not os.path.exists(NVIS_DATA_FILE):
        return None
    
    try:
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=None)
        
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            return None
        
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=header_row, skiprows=0)
        df = df.dropna(how='all')
        
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for April 15-28th
        df_april15_28 = df[(df['DateTime'].dt.month == 4) & 
                          (df['DateTime'].dt.day >= 15) & 
                          (df['DateTime'].dt.day <= 28)].copy()
        
        year_columns = []
        for col in df_april15_28.columns:
            if col not in ['DATE', 'TIME', 'DateTime'] and pd.api.types.is_numeric_dtype(df_april15_28[col]):
                if isinstance(col, (int, float)) and 2017 <= col <= 2023:
                    year_columns.append(col)
        
        return {'data': df_april15_28, 'year_columns': year_columns}
    except Exception as e:
        print(f"Error loading Darwin April 15-28th data: {e}")
        return None

def load_darwin_april_data():
    """Load Darwin data for full April across 7 years"""
    if not os.path.exists(NVIS_DATA_FILE):
        return None
    
    try:
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=None)
        
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            return None
        
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Darwin', header=header_row, skiprows=0)
        df = df.dropna(how='all')
        
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for full April
        df_april = df[df['DateTime'].dt.month == 4].copy()
        
        year_columns = []
        for col in df_april.columns:
            if col not in ['DATE', 'TIME', 'DateTime'] and pd.api.types.is_numeric_dtype(df_april[col]):
                if isinstance(col, (int, float)) and 2017 <= col <= 2023:
                    year_columns.append(col)
        
        return {'data': df_april, 'year_columns': year_columns}
    except Exception as e:
        print(f"Error loading Darwin April data: {e}")
        return None

def load_guam_april15_data():
    """Load Guam data for April 15th across 7 years"""
    if not os.path.exists(NVIS_DATA_FILE):
        return None
    
    try:
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=None)
        
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            return None
        
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=header_row, skiprows=0)
        df = df.dropna(how='all')
        
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for April 15th only
        df_april15 = df[(df['DateTime'].dt.month == 4) & (df['DateTime'].dt.day == 15)].copy()
        
        year_columns = []
        for col in df_april15.columns:
            if col not in ['DATE', 'TIME', 'DateTime'] and pd.api.types.is_numeric_dtype(df_april15[col]):
                if isinstance(col, (int, float)) and 2017 <= col <= 2023:
                    year_columns.append(col)
        
        return {'data': df_april15, 'year_columns': year_columns}
    except Exception as e:
        print(f"Error loading Guam April 15th data: {e}")
        return None

def load_guam_april15_28_data():
    """Load Guam data for April 15-28th across 7 years"""
    if not os.path.exists(NVIS_DATA_FILE):
        return None
    
    try:
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=None)
        
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            return None
        
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=header_row, skiprows=0)
        df = df.dropna(how='all')
        
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for April 15-28th
        df_april15_28 = df[(df['DateTime'].dt.month == 4) & 
                          (df['DateTime'].dt.day >= 15) & 
                          (df['DateTime'].dt.day <= 28)].copy()
        
        year_columns = []
        for col in df_april15_28.columns:
            if col not in ['DATE', 'TIME', 'DateTime'] and pd.api.types.is_numeric_dtype(df_april15_28[col]):
                if isinstance(col, (int, float)) and 2017 <= col <= 2023:
                    year_columns.append(col)
        
        return {'data': df_april15_28, 'year_columns': year_columns}
    except Exception as e:
        print(f"Error loading Guam April 15-28th data: {e}")
        return None

def load_guam_april_data():
    """Load Guam data for full April across 7 years"""
    if not os.path.exists(NVIS_DATA_FILE):
        return None
    
    try:
        df_raw = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=None)
        
        header_row = None
        for idx, row in df_raw.iterrows():
            if 'DATE' in str(row.values) and 'TIME' in str(row.values):
                header_row = idx
                break
        
        if header_row is None:
            return None
        
        df = pd.read_excel(NVIS_DATA_FILE, sheet_name='Guam', header=header_row, skiprows=0)
        df = df.dropna(how='all')
        
        if 'DATE' in df.columns and 'TIME' in df.columns:
            df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str), 
                                          errors='coerce')
            df = df.dropna(subset=['DateTime'])
        
        # Filter for full April
        df_april = df[df['DateTime'].dt.month == 4].copy()
        
        year_columns = []
        for col in df_april.columns:
            if col not in ['DATE', 'TIME', 'DateTime'] and pd.api.types.is_numeric_dtype(df_april[col]):
                if isinstance(col, (int, float)) and 2017 <= col <= 2023:
                    year_columns.append(col)
        
        return {'data': df_april, 'year_columns': year_columns}
    except Exception as e:
        print(f"Error loading Guam April data: {e}")
        return None

def calculate_average_fof2(data_dict, station='darwin'):
    """Calculate average foF2 across all years and measurements"""
    if data_dict is None:
        return None
    
    df = data_dict['data']
    year_columns = data_dict['year_columns']
    
    all_fof2_values = []
    
    for year in year_columns:
        df_year = df.dropna(subset=[year])
        if len(df_year) == 0:
            continue
        
        if station.lower() == 'darwin':
            fof2_values = calculate_fof2_from_signal_darwin(df_year[year])
        else:  # guam
            fof2_values = calculate_fof2_from_signal_guam(df_year[year])
        
        all_fof2_values.extend(fof2_values)
    
    if len(all_fof2_values) == 0:
        return None
    
    return {
        'mean': np.mean(all_fof2_values),
        'std': np.std(all_fof2_values),
        'min': np.min(all_fof2_values),
        'max': np.max(all_fof2_values),
        'count': len(all_fof2_values)
    }

def display_summary_statistics():
    """Display all foF2 summary statistics"""
    
    print("="*70)
    print("📊 foF2 SUMMARY STATISTICS (7 Years: 2017-2023)")
    print("="*70)
    print()
    
    # Darwin statistics
    print("🌏 DARWIN")
    print("-"*70)
    
    # 1. Darwin April 15th
    print("\n1. Average foF2 for Darwin on 15th April (past 7 years)")
    darwin_april15 = load_darwin_april15_data()
    if darwin_april15:
        stats = calculate_average_fof2(darwin_april15, 'darwin')
        if stats:
            print(f"   {stats['mean']:.2f} ± {stats['std']:.2f} MHz")
        else:
            print("   ❌ No data available")
    else:
        print("   ❌ Could not load data")
    
    # 2. Darwin April 15-28th
    print("\n2. Previous 7 years of foF2 for April 15-28th (Darwin)")
    darwin_april15_28 = load_darwin_april15_28_data()
    if darwin_april15_28:
        stats = calculate_average_fof2(darwin_april15_28, 'darwin')
        if stats:
            print(f"   {stats['mean']:.2f} ± {stats['std']:.2f} MHz")
        else:
            print("   ❌ No data available")
    else:
        print("   ❌ Could not load data")
    
    # 3. Darwin Full April
    print("\n3. Previous 7 years of foF2 for April (Darwin)")
    darwin_april = load_darwin_april_data()
    if darwin_april:
        stats = calculate_average_fof2(darwin_april, 'darwin')
        if stats:
            print(f"   {stats['mean']:.2f} ± {stats['std']:.2f} MHz")
        else:
            print("   ❌ No data available")
    else:
        print("   ❌ Could not load data")
    
    # Guam statistics
    print("\n" + "="*70)
    print("🌏 GUAM")
    print("-"*70)
    
    # 4. Guam April 15th
    print("\n4. Average foF2 for Guam on 15th April (past 7 years)")
    guam_april15 = load_guam_april15_data()
    if guam_april15:
        stats = calculate_average_fof2(guam_april15, 'guam')
        if stats:
            print(f"   {stats['mean']:.2f} ± {stats['std']:.2f} MHz")
        else:
            print("   ❌ No data available")
    else:
        print("   ❌ Could not load data")
    
    # 5. Guam April 15-28th
    print("\n5. Previous 7 years of foF2 for April 15-28th (Guam)")
    guam_april15_28 = load_guam_april15_28_data()
    if guam_april15_28:
        stats = calculate_average_fof2(guam_april15_28, 'guam')
        if stats:
            print(f"   {stats['mean']:.2f} ± {stats['std']:.2f} MHz")
        else:
            print("   ❌ No data available")
    else:
        print("   ❌ Could not load data")
    
    # 6. Guam Full April
    print("\n6. Previous 7 years of foF2 for April (Guam)")
    guam_april = load_guam_april_data()
    if guam_april:
        stats = calculate_average_fof2(guam_april, 'guam')
        if stats:
            print(f"   {stats['mean']:.2f} ± {stats['std']:.2f} MHz")
        else:
            print("   ❌ No data available")
    else:
        print("   ❌ Could not load data")
    
    print("\n" + "="*70)

def main():
    """Main function"""
    display_summary_statistics()

if __name__ == "__main__":
    main()
