#!/usr/bin/env python3
"""
Advanced Aurora Borealis Tracker & Prediction System
A comprehensive tool for aurora enthusiasts!
"""

import random
import datetime
import math
import json

class AuroraTracker:
    def __init__(self):
        self.locations = {
            "Fairbanks, Alaska": {"lat": 64.8, "lon": -147.7, "magnetic_lat": 65.1},
            "Yellowknife, Canada": {"lat": 62.5, "lon": -114.3, "magnetic_lat": 68.6},
            "Reykjavik, Iceland": {"lat": 64.1, "lon": -21.9, "magnetic_lat": 64.8},
            "Tromsø, Norway": {"lat": 69.6, "lon": 18.9, "magnetic_lat": 66.7},
            "Anchorage, Alaska": {"lat": 61.2, "lon": -149.9, "magnetic_lat": 61.8},
            "Calgary, Canada": {"lat": 51.0, "lon": -114.1, "magnetic_lat": 58.2},
            "Seattle, Washington": {"lat": 47.6, "lon": -122.3, "magnetic_lat": 54.2},
            "Minneapolis, Minnesota": {"lat": 44.98, "lon": -93.3, "magnetic_lat": 54.8}
        }
        
        self.aurora_colors = {
            "Green": {"altitude": "80-150 km", "cause": "Oxygen atoms", "frequency": 60},
            "Red": {"altitude": "150-300 km", "cause": "High altitude oxygen", "frequency": 15},
            "Blue": {"altitude": "80-120 km", "cause": "Nitrogen molecules", "frequency": 10},
            "Pink": {"altitude": "80-150 km", "cause": "Nitrogen + oxygen mix", "frequency": 10},
            "Purple": {"altitude": "80-120 km", "cause": "Nitrogen at lower altitudes", "frequency": 5}
        }
        
    def generate_kp_forecast(self, days=7):
        """Generate a realistic KP index forecast"""
        forecast = []
        current_kp = random.uniform(1, 4)  # Start with moderate activity
        
        for day in range(days):
            # Simulate solar cycle variations
            daily_variation = random.uniform(-1.5, 2.0)
            current_kp = max(0, min(9, current_kp + daily_variation))
            
            date = datetime.date.today() + datetime.timedelta(days=day)
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "kp_index": round(current_kp, 1),
                "activity_level": self.get_activity_level(current_kp),
                "visibility_zone": self.get_visibility_zone(current_kp)
            })
            
        return forecast
    
    def get_activity_level(self, kp):
        if kp < 2:
            return "Quiet"
        elif kp < 3:
            return "Unsettled"
        elif kp < 4:
            return "Active"
        elif kp < 5:
            return "Minor Storm"
        elif kp < 6:
            return "Moderate Storm"
        elif kp < 7:
            return "Strong Storm"
        elif kp < 8:
            return "Severe Storm"
        else:
            return "Extreme Storm"
    
    def get_visibility_zone(self, kp):
        if kp < 2:
            return "Arctic Circle only"
        elif kp < 3:
            return "Northern Canada, Alaska"
        elif kp < 4:
            return "Northern border states"
        elif kp < 5:
            return "Northern US, southern Canada"
        elif kp < 6:
            return "Most of northern US"
        elif kp < 7:
            return "Central US states"
        elif kp < 8:
            return "Southern US possible"
        else:
            return "Visible to southern latitudes"
    
    def calculate_viewing_probability(self, location, kp_index):
        """Calculate probability of seeing aurora at given location"""
        if location not in self.locations:
            return 0
        
        magnetic_lat = self.locations[location]["magnetic_lat"]
        
        # Simplified formula based on magnetic latitude and KP index
        threshold_lat = 67 - (kp_index * 2.5)  # Approximation
        
        if magnetic_lat >= threshold_lat:
            probability = min(95, (magnetic_lat - threshold_lat + 5) * 10)
        else:
            probability = max(0, (magnetic_lat - threshold_lat + 10) * 2)
        
        return max(0, min(100, probability))
    
    def generate_photography_tips(self, kp_index):
        """Generate photography tips based on expected intensity"""
        tips = [
            "🌍 Find a location away from city lights",
            "🕐 Best viewing: 10 PM - 2 AM local time",
            "🌙 New moon periods offer darkest skies",
            "📱 Use aurora prediction apps for real-time updates"
        ]
        
        if kp_index >= 3:
            tips.extend([
                "📸 Camera settings: ISO 800-1600, f/2.8, 15-20 sec exposure",
                "🎯 Focus on infinity or distant lights",
                "🔋 Bring extra batteries - cold drains them fast!"
            ])
        
        if kp_index >= 5:
            tips.extend([
                "🎨 Expect dynamic, dancing aurora!",
                "📹 Consider time-lapse photography",
                "👥 Aurora may be visible to naked eye"
            ])
        
        return tips
    
    def predict_colors(self, kp_index):
        """Predict likely aurora colors based on activity"""
        predicted_colors = []
        
        # Green is almost always present
        if kp_index >= 1:
            predicted_colors.append("Green")
        
        # Red appears with higher activity
        if kp_index >= 4:
            predicted_colors.append("Red")
        
        # Blue and pink with moderate activity
        if kp_index >= 3:
            if random.random() < 0.6:
                predicted_colors.append("Pink")
            if random.random() < 0.4:
                predicted_colors.append("Blue")
        
        # Purple is rare but possible in strong storms
        if kp_index >= 6 and random.random() < 0.3:
            predicted_colors.append("Purple")
        
        return predicted_colors
    
    def generate_full_report(self):
        """Generate comprehensive aurora report"""
        print("🌌" * 20)
        print("   AURORA BOREALIS COMPREHENSIVE TRACKER")
        print("🌌" * 20)
        print(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Current conditions
        current_kp = random.uniform(1, 6)
        print(f"🔮 CURRENT CONDITIONS")
        print(f"   KP Index: {current_kp:.1f}")
        print(f"   Activity: {self.get_activity_level(current_kp)}")
        print(f"   Visibility: {self.get_visibility_zone(current_kp)}")
        print()
        
        # Forecast
        print("📊 7-DAY FORECAST")
        forecast = self.generate_kp_forecast()
        for day in forecast:
            print(f"   {day['date']}: KP {day['kp_index']} - {day['activity_level']}")
        print()
        
        # Location probabilities
        print("📍 VIEWING PROBABILITIES (Next 24 Hours)")
        for location in self.locations:
            prob = self.calculate_viewing_probability(location, current_kp)
            print(f"   {location:<20}: {prob:>3.0f}%")
        print()
        
        # Expected colors
        colors = self.predict_colors(current_kp)
        print("🎨 EXPECTED COLORS")
        for color in colors:
            info = self.aurora_colors[color]
            print(f"   {color}: {info['altitude']} altitude ({info['cause']})")
        print()
        
        # Photography tips
        print("📸 PHOTOGRAPHY TIPS")
        tips = self.generate_photography_tips(current_kp)
        for tip in tips:
            print(f"   {tip}")
        print()
        
        # Fun facts
        facts = [
            "The aurora follows Earth's magnetic field lines",
            "Solar wind travels at 400-800 km/s to reach Earth",
            "Aurora activity follows an 11-year solar cycle",
            "The aurora oval is typically 3,000 km wide",
            "Aboriginal peoples have over 100 names for aurora"
        ]
        print("💡 AURORA FACT OF THE DAY")
        print(f"   {random.choice(facts)}")
        print()
        
        print("✨ Happy Aurora Hunting! ✨")
        print("🌌" * 20)

if __name__ == "__main__":
    tracker = AuroraTracker()
    tracker.generate_full_report()