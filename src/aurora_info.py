#!/usr/bin/env python3
"""
Aurora Borealis Information Generator
A fun script to generate facts about the Northern Lights
"""

import random
import datetime

# Fun facts about Aurora Borealis
aurora_facts = [
    "The aurora borealis is caused by charged particles from the sun colliding with Earth's magnetic field.",
    "The best time to see the Northern Lights is during the winter months in the Northern Hemisphere.",
    "The aurora can appear in various colors including green, pink, red, yellow, and blue.",
    "Green is the most common color, produced by oxygen atoms about 60 miles above Earth.",
    "The aurora follows an oval-shaped zone around the magnetic poles called the auroral oval.",
    "The phenomenon was named after Aurora, the Roman goddess of dawn.",
    "Solar wind speed can reach up to 900 km/s during geomagnetic storms.",
    "The aurora can extend from 80 to 640 kilometers above Earth's surface.",
    "Indigenous peoples have many legends about the aurora, often seeing them as spirits dancing.",
    "The aurora australis is the Southern Hemisphere equivalent of the aurora borealis."
]

def generate_aurora_report():
    """Generate a random aurora report with current information"""
    print("🌌 AURORA BOREALIS INFORMATION REPORT 🌌")
    print("=" * 50)
    print(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Generate random KP index (0-9 scale)
    kp_index = random.randint(0, 9)
    
    print(f"Current KP Index: {kp_index}/9")
    
    if kp_index <= 2:
        visibility = "Low - Visible only in polar regions"
    elif kp_index <= 4:
        visibility = "Moderate - Visible in northern Canada and Alaska"
    elif kp_index <= 6:
        visibility = "High - Visible in northern US states"
    else:
        visibility = "Very High - Visible in southern Canada and northern US"
    
    print(f"Visibility: {visibility}")
    print()
    
    # Random fact
    fact = random.choice(aurora_facts)
    print("🔍 Random Aurora Fact:")
    print(f"   {fact}")
    print()
    
    # Generate viewing tips
    print("👀 Viewing Tips:")
    print("   • Look north, away from city lights")
    print("   • Best viewing time: 10 PM - 2 AM")
    print("   • Clear, dark skies are essential")
    print("   • Be patient - activity can change quickly")
    print("   • Camera settings: ISO 800-3200, wide angle lens")
    print()
    
    print("✨ Happy aurora hunting! ✨")

if __name__ == "__main__":
    generate_aurora_report()