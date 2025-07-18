#!/usr/bin/env python3
"""
ASCII Art Aurora Generator
Creates beautiful text-based aurora displays
"""

import random
import time
import os

class AuroraArt:
    def __init__(self):
        self.colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'yellow': '\033[93m',
            'reset': '\033[0m'
        }
        
    def create_static_aurora(self):
        """Create a static ASCII aurora display"""
        print(self.colors['cyan'] + "✨" * 50 + self.colors['reset'])
        print(self.colors['blue'] + "    NORTHERN LIGHTS ASCII ART GENERATOR    " + self.colors['reset'])
        print(self.colors['cyan'] + "✨" * 50 + self.colors['reset'])
        print()
        
        # Create layered aurora effect
        aurora_lines = [
            "                    ~~~~~*~~~~~                    ",
            "                ~~~~~~~~*~~~~~~~~                ",
            "            ~~~~~~~~~~~~*~~~~~~~~~~~~            ",
            "        ~~~~~~~~~~~~~~~~*~~~~~~~~~~~~~~~~        ",
            "    ~~~~~~~~~~~~~~~~~~~~*~~~~~~~~~~~~~~~~~~~~    ",
            "~~~~~~~~~~~~~~~~~~~~~~~~*~~~~~~~~~~~~~~~~~~~~~~~~",
            "                    ~~~~~*~~~~~                    ",
            "                ~~~~~~~~*~~~~~~~~                ",
            "            ~~~~~~~~~~~~*~~~~~~~~~~~~            ",
            "        ~~~~~~~~~~~~~~~~*~~~~~~~~~~~~~~~~        ",
            "    ~~~~~~~~~~~~~~~~~~~~*~~~~~~~~~~~~~~~~~~~~    ",
        ]
        
        # Color the aurora
        colors = ['green', 'cyan', 'blue', 'purple']
        for i, line in enumerate(aurora_lines):
            color = colors[i % len(colors)]
            print(self.colors[color] + line + self.colors['reset'])
            
        print()
        print(self.colors['yellow'] + "    ⭐  DANCING ACROSS THE NORTHERN SKY  ⭐    " + self.colors['reset'])
        print()
        
        # Create ground silhouette
        ground_lines = [
            "   /\\    /\\      /\\    /\\    /\\      /\\    /\\   ",
            "  /  \\  /  \\    /  \\  /  \\  /  \\    /  \\  /  \\  ",
            " /    \\/    \\  /    \\/    \\/    \\  /    \\/    \\ ",
            "/____________\\/____________\\/____________\\/____\\",
            "🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲",
        ]
        
        for line in ground_lines:
            print(self.colors['green'] + line + self.colors['reset'])
            
        print()
        print(self.colors['cyan'] + "Generated with love for aurora enthusiasts! 🌌" + self.colors['reset'])
        
    def create_constellation_map(self):
        """Create a simple constellation map"""
        print("\n" + self.colors['yellow'] + "✨ NORTHERN SKY STAR MAP ✨" + self.colors['reset'])
        print(self.colors['cyan'] + "=" * 40 + self.colors['reset'])
        
        sky_map = [
            "                    ⭐ Polaris               ",
            "              ⭐                 ⭐        ",
            "          ⭐        Big Dipper       ⭐    ",
            "        ⭐     ⭐           ⭐           ⭐",
            "      ⭐           ⭐   ⭐       ⭐       ",
            "    ⭐               ⭐               ⭐    ",
            "  ⭐                   ⭐               ⭐  ",
            "⭐         Cassiopeia        ⭐         ⭐",
            "  ⭐               ⭐               ⭐  ",
            "    ⭐           ⭐     ⭐       ⭐      ",
            "      ⭐     ⭐           ⭐           ⭐",
            "        ⭐                         ⭐    ",
            "          ⭐                   ⭐        ",
            "            ⭐               ⭐          ",
            "              ⭐           ⭐            ",
            "                ⭐       ⭐              ",
            "                  ⭐   ⭐                ",
            "                    ⭐                  ",
        ]
        
        for line in sky_map:
            print(self.colors['yellow'] + line + self.colors['reset'])
            
        print("\n" + self.colors['green'] + "🧭 Best viewing direction: NORTH" + self.colors['reset'])
        print(self.colors['blue'] + "🌡️  Optimal temperature: Cold, clear nights" + self.colors['reset'])
        
    def create_aurora_phases(self):
        """Show different phases of aurora activity"""
        phases = [
            ("Quiet Phase", "       ~~~   ~~~       ", 'cyan'),
            ("Active Phase", "    ~~~~~~~*~~~~~~~    ", 'green'),
            ("Substorm Phase", "  ~~~~~~~~~~~~~~~~~  ", 'red'),
            ("Recovery Phase", "    ~~~~~~~*~~~~~~~    ", 'purple'),
        ]
        
        print("\n" + self.colors['blue'] + "🌌 AURORA ACTIVITY PHASES 🌌" + self.colors['reset'])
        print(self.colors['cyan'] + "=" * 35 + self.colors['reset'])
        
        for phase_name, pattern, color in phases:
            print(f"\n{self.colors['yellow']}{phase_name}:{self.colors['reset']}")
            print(self.colors[color] + pattern + self.colors['reset'])
            
    def generate_aurora_poem(self):
        """Generate a short aurora poem"""
        poem_lines = [
            "🌌 Dancing lights across the sky,",
            "   Green and gold, they swirl and fly.",
            "   Solar winds from distant star,",
            "   Paint the heavens near and far.",
            "",
            "   Ancient spirits, legends say,",
            "   Come alive at end of day.",
            "   Northern lights, aurora bright,",
            "   Magic dancing through the night. ✨"
        ]
        
        print("\n" + self.colors['purple'] + "📜 AURORA POEM 📜" + self.colors['reset'])
        print(self.colors['cyan'] + "=" * 25 + self.colors['reset'])
        
        for line in poem_lines:
            if line.strip():
                print(self.colors['green'] + line + self.colors['reset'])
            else:
                print()

def main():
    aurora = AuroraArt()
    
    # Create a comprehensive aurora art display
    aurora.create_static_aurora()
    aurora.create_constellation_map()
    aurora.create_aurora_phases()
    aurora.generate_aurora_poem()
    
    print("\n" + aurora.colors['yellow'] + "🎨 ASCII Aurora Art Complete! 🎨" + aurora.colors['reset'])
    print(aurora.colors['cyan'] + "Share this with fellow aurora enthusiasts!" + aurora.colors['reset'])

if __name__ == "__main__":
    main()