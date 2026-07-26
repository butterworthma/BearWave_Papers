#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def display_chart_interactive(chart_path, title):
    """Display a single chart interactively"""
    
    if not os.path.exists(chart_path):
        print(f"❌ Chart not found: {chart_path}")
        return False
    
    try:
        # Load and display the image
        img = mpimg.imread(chart_path)
        
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.imshow(img)
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Add file info
        file_size = os.path.getsize(chart_path) / (1024 * 1024)
        plt.figtext(0.5, 0.02, f'File: {os.path.basename(chart_path)} ({file_size:.1f} MB)', 
                   ha='center', fontsize=10, style='italic')
        
        plt.tight_layout()
        plt.show()
        
        print(f"✅ Displayed: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Error displaying {title}: {e}")
        return False

def interactive_chart_viewer():
    """Interactive chart viewer with menu"""
    
    charts = {
        '1': {
            'path': 'output/best_quality_7_1_MHz.png',
            'title': '7.1 MHz - Best Quality Individual Chart',
            'description': 'Morning period (9h 9m) - Excellent SNR stability (±0.4 dB)'
        },
        '2': {
            'path': 'output/best_quality_10_130_MHz.png',
            'title': '10.130 MHz - Best Quality Individual Chart',
            'description': 'Full day coverage (15h 10m) - Best continuous period'
        },
        '3': {
            'path': 'output/best_quality_5_GHz.png',
            'title': '5 GHz - Best Quality Individual Chart',
            'description': 'Multi-day period (28h 16m) - Highest quality score (0.741)'
        },
        '4': {
            'path': 'output/best_quality_analysis.png',
            'title': 'Best Quality Comparison Chart',
            'description': 'All three frequencies compared - No data loss periods'
        },
        '5': {
            'path': 'output/data_quality_comparison.png',
            'title': 'Data Quality Metrics Chart',
            'description': 'Quality scores, density, and stability comparison'
        },
        '6': {
            'path': 'output/nvis_ionospheric_analysis.png',
            'title': 'NVIS Ionospheric Analysis',
            'description': 'Real ionospheric data correlation with measurements'
        },
        '7': {
            'path': 'output/nvis_propagation_model.png',
            'title': 'NVIS Propagation Model',
            'description': 'Theoretical 24-hour propagation predictions'
        },
        '8': {
            'path': 'output/best_24h_comparison.png',
            'title': 'Previous 24-Hour Comparison',
            'description': 'Earlier analysis with longer periods'
        }
    }
    
    while True:
        print("\n" + "="*70)
        print("🖼️  INTERACTIVE CHART VIEWER")
        print("="*70)
        print("\nAvailable charts:")
        
        available_charts = []
        for key, chart in charts.items():
            if os.path.exists(chart['path']):
                file_size = os.path.getsize(chart['path']) / (1024 * 1024)
                print(f"  {key}. ✅ {chart['title']} ({file_size:.1f} MB)")
                print(f"     📝 {chart['description']}")
                available_charts.append(key)
            else:
                print(f"  {key}. ❌ {chart['title']} (not found)")
        
        print(f"\n  a. 🖼️  Display ALL available charts")
        print(f"  g. 📊 Create chart gallery")
        print(f"  q. 🚪 Quit")
        
        choice = input(f"\nSelect chart to display (1-8, a, g, q): ").strip().lower()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        elif choice == 'a':
            print(f"\n🖼️  Displaying all {len(available_charts)} available charts...")
            for key in available_charts:
                chart = charts[key]
                print(f"\n📊 Showing: {chart['title']}")
                display_chart_interactive(chart['path'], chart['title'])
                if key != available_charts[-1]:  # Not the last chart
                    input("Press Enter for next chart...")
        elif choice == 'g':
            create_chart_gallery(charts, available_charts)
        elif choice in charts:
            if choice in available_charts:
                chart = charts[choice]
                print(f"\n📊 Displaying: {chart['title']}")
                display_chart_interactive(chart['path'], chart['title'])
            else:
                print(f"❌ Chart {choice} not found!")
        else:
            print("❌ Invalid choice! Please select 1-8, a, g, or q")

def create_chart_gallery(charts, available_charts):
    """Create and display a gallery of all available charts"""
    
    if not available_charts:
        print("❌ No charts available for gallery!")
        return
    
    print(f"\n🖼️  Creating gallery with {len(available_charts)} charts...")
    
    # Calculate grid size
    n_charts = len(available_charts)
    if n_charts <= 2:
        rows, cols = 1, n_charts
        figsize = (16, 8)
    elif n_charts <= 4:
        rows, cols = 2, 2
        figsize = (16, 12)
    elif n_charts <= 6:
        rows, cols = 2, 3
        figsize = (20, 12)
    else:
        rows, cols = 3, 3
        figsize = (20, 16)
    
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    
    # Handle single subplot case
    if n_charts == 1:
        axes = [axes]
    elif rows == 1 or cols == 1:
        axes = axes.flatten()
    else:
        axes = axes.flatten()
    
    for i, key in enumerate(available_charts):
        chart = charts[key]
        try:
            img = mpimg.imread(chart['path'])
            axes[i].imshow(img)
            axes[i].set_title(f"{key}. {chart['title']}", fontsize=10, fontweight='bold')
            axes[i].axis('off')
        except Exception as e:
            axes[i].text(0.5, 0.5, f'Error loading\n{chart["title"]}', 
                        ha='center', va='center', transform=axes[i].transAxes)
            axes[i].set_title(f"{key}. {chart['title']}", fontsize=10)
            axes[i].axis('off')
    
    # Hide unused subplots
    for i in range(n_charts, len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.suptitle('NVIS Data Analysis - Complete Chart Gallery', fontsize=16, fontweight='bold', y=0.98)
    plt.subplots_adjust(top=0.93)
    
    # Save gallery
    gallery_file = 'output/interactive_chart_gallery.png'
    plt.savefig(gallery_file, dpi=120, bbox_inches='tight')
    print(f"📁 Gallery saved: {gallery_file}")
    
    plt.show()
    print("✅ Gallery displayed!")

def display_all_charts_slideshow():
    """Display all charts in slideshow mode"""
    
    charts = [
        ('output/best_quality_7_1_MHz.png', '7.1 MHz - Best Quality'),
        ('output/best_quality_10_130_MHz.png', '10.130 MHz - Best Quality'),
        ('output/best_quality_5_GHz.png', '5 GHz - Best Quality'),
        ('output/best_quality_analysis.png', 'Best Quality Comparison'),
        ('output/data_quality_comparison.png', 'Quality Metrics'),
        ('output/nvis_ionospheric_analysis.png', 'NVIS Ionospheric Analysis'),
        ('output/nvis_propagation_model.png', 'NVIS Propagation Model')
    ]
    
    print("🎬 Starting slideshow...")
    
    for i, (chart_path, title) in enumerate(charts):
        if os.path.exists(chart_path):
            print(f"\n📊 Slide {i+1}/{len(charts)}: {title}")
            display_chart_interactive(chart_path, title)
            if i < len(charts) - 1:
                input("Press Enter for next slide...")
        else:
            print(f"❌ Skipping missing chart: {title}")
    
    print("🎬 Slideshow complete!")

def main():
    print("🖼️  CHART DISPLAY SYSTEM")
    print("Choose display mode:")
    print("  1. Interactive menu")
    print("  2. Slideshow (all charts)")
    print("  3. Quick gallery")
    
    choice = input("Select mode (1-3): ").strip()
    
    if choice == '1':
        interactive_chart_viewer()
    elif choice == '2':
        display_all_charts_slideshow()
    elif choice == '3':
        charts = {}  # Simplified for gallery
        available_charts = []
        create_chart_gallery(charts, available_charts)
    else:
        print("❌ Invalid choice, starting interactive menu...")
        interactive_chart_viewer()

if __name__ == "__main__":
    main()
