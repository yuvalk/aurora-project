#!/usr/bin/env python3
"""
Aurora Borealis Toolkit Demo
Showcases all features of the toolkit in sequence
"""

import time
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from aurora_tracker import AuroraTracker
from aurora_art import AuroraArt
from aurora_graph import AuroraGraph

def print_banner():
    """Print welcome banner"""
    colors = {
        'cyan': '\033[96m',
        'yellow': '\033[93m',
        'reset': '\033[0m'
    }
    
    print(colors['cyan'] + "=" * 60 + colors['reset'])
    print(colors['yellow'] + "🌌 AURORA BOREALIS TOOLKIT - FULL DEMO 🌌" + colors['reset'])
    print(colors['cyan'] + "=" * 60 + colors['reset'])
    print()
    print("This demo showcases all features of the Aurora Borealis Toolkit.")
    print("Sit back and enjoy the journey through aurora science and art!")
    print()
    input("Press Enter to begin the demo... ")

def wait_for_user():
    """Wait for user input between sections"""
    print("\n" + "─" * 50)
    input("Press Enter to continue to the next section... ")
    print()

def main():
    """Run the complete demo"""
    print_banner()
    
    # Section 1: Aurora Tracker
    print("🔮 SECTION 1: AURORA TRACKING & FORECASTING")
    print("=" * 50)
    tracker = AuroraTracker()
    tracker.generate_full_report()
    wait_for_user()
    
    # Section 2: ASCII Art
    print("🎨 SECTION 2: AURORA ART & VISUALIZATIONS")
    print("=" * 50)
    art = AuroraArt()
    art.create_static_aurora()
    art.create_constellation_map()
    art.create_aurora_phases()
    art.generate_aurora_poem()
    wait_for_user()
    
    # Section 3: Data Visualization
    print("📊 SECTION 3: DATA ANALYSIS & GRAPHS")
    print("=" * 50)
    graph = AuroraGraph()
    data = graph.generate_sample_data(14)
    graph.create_bar_chart(data)
    graph.create_line_graph(data)
    graph.create_statistics_summary(data)
    wait_for_user()
    
    # Final message
    print("🌟 DEMO COMPLETE! 🌟")
    print("=" * 30)
    print()
    print("Thank you for exploring the Aurora Borealis Toolkit!")
    print("This toolkit includes:")
    print("  • Comprehensive aurora tracking and forecasting")
    print("  • Beautiful ASCII art and terminal visualizations")
    print("  • Data analysis with graphs and statistics")
    print("  • Educational content and photography tips")
    print("  • Professional project structure and documentation")
    print()
    print("🌌 Ready to hunt for aurora? Check the current forecast!")
    print("✨ Happy Aurora Hunting! ✨")

if __name__ == "__main__":
    main()