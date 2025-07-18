#!/usr/bin/env python3
"""
Real-time Aurora Tracker with NOAA Data Integration
Enhanced version using live space weather data
"""

import sys
import datetime
from typing import Dict, List, Optional
from noaa_data import NOAASpaceWeather

class RealTimeAuroraTracker:
    def __init__(self):
        self.noaa = NOAASpaceWeather()
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
    
    def get_activity_level(self, kp: float) -> str:
        """Convert KP index to activity level"""
        if kp < 1:
            return "Quiet"
        elif kp < 2:
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
    
    def get_visibility_zone(self, kp: float) -> str:
        """Get visibility zone based on KP index"""
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
    
    def calculate_viewing_probability(self, location: str, kp_index: float) -> float:
        """Calculate probability of seeing aurora at given location"""
        if location not in self.locations:
            return 0
        
        magnetic_lat = self.locations[location]["magnetic_lat"]
        
        # Enhanced formula based on real aurora science
        threshold_lat = 67 - (kp_index * 2.5)  # Approximation
        
        if magnetic_lat >= threshold_lat:
            probability = min(95, (magnetic_lat - threshold_lat + 5) * 10)
        else:
            probability = max(0, (magnetic_lat - threshold_lat + 10) * 2)
        
        return max(0, min(100, probability))
    
    def predict_colors(self, kp_index: float, solar_wind: Optional[Dict] = None) -> List[str]:
        """Predict likely aurora colors based on conditions"""
        predicted_colors = []
        
        # Green is almost always present
        if kp_index >= 1:
            predicted_colors.append("Green")
        
        # Red appears with higher activity or specific solar wind conditions
        if kp_index >= 4 or (solar_wind and solar_wind.get('speed', 0) > 500):
            predicted_colors.append("Red")
        
        # Blue and pink with moderate activity
        if kp_index >= 3:
            predicted_colors.append("Pink")
            if kp_index >= 4:
                predicted_colors.append("Blue")
        
        # Purple is rare but possible in strong storms
        if kp_index >= 6:
            predicted_colors.append("Purple")
        
        return predicted_colors if predicted_colors else ["Green"]
    
    def generate_photography_tips(self, kp_index: float, solar_wind: Optional[Dict] = None) -> List[str]:
        """Generate photography tips based on current conditions"""
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
        
        # Add solar wind specific tips
        if solar_wind:
            if solar_wind.get('bz', 0) < -5:
                tips.append("⚡ Strong southward magnetic field - expect bright displays!")
            if solar_wind.get('speed', 0) > 600:
                tips.append("🌟 High-speed solar wind - aurora may be more active!")
        
        return tips
    
    def generate_comprehensive_report(self) -> None:
        """Generate comprehensive real-time aurora report"""
        print("🌌" * 20)
        print("   REAL-TIME AURORA BOREALIS TRACKER")
        print("🌌" * 20)
        print(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("📡 Data Source: NOAA Space Weather Prediction Center")
        print()
        
        # Fetch real-time data
        print("🔄 Fetching real-time space weather data...")
        try:
            comprehensive_data = self.noaa.get_comprehensive_data()
        except Exception as e:
            print(f"❌ Error fetching NOAA data: {e}")
            print("🔄 Falling back to simulated data...")
            self._generate_fallback_report()
            return
        
        current_kp = comprehensive_data.get('current_kp')
        if not current_kp:
            print("❌ Unable to fetch current KP index")
            return
        
        # Current conditions
        print(f"🔮 CURRENT CONDITIONS")
        print(f"   KP Index: {current_kp:.1f}")
        print(f"   Activity: {self.get_activity_level(current_kp)}")
        print(f"   Visibility: {self.get_visibility_zone(current_kp)}")
        print()
        
        # Solar wind conditions
        solar_wind = comprehensive_data.get('solar_wind')
        if solar_wind:
            print("🌟 SOLAR WIND CONDITIONS")
            print(f"   Speed: {solar_wind['speed']:.1f} km/s")
            print(f"   Density: {solar_wind['density']:.1f} particles/cm³")
            print(f"   Bz: {solar_wind['bz']:.1f} nT")
            print(f"   Aurora Potential: {solar_wind['aurora_potential']}")
            print()
        
        # Geomagnetic alerts
        alerts = comprehensive_data.get('alerts', [])
        if alerts:
            print("🚨 GEOMAGNETIC ALERTS")
            for alert in alerts[:3]:  # Show first 3
                print(f"   {alert['severity']}: {alert['message'][:80]}...")
            print()
        
        # Forecast
        forecast = comprehensive_data.get('kp_forecast', [])
        if forecast:
            print("📊 KP FORECAST (Next 24 Hours)")
            for entry in forecast[:8]:  # Next 24 hours
                print(f"   {entry['date']} {entry['time']}: KP {entry['kp_index']:.1f} - {entry['activity_level']}")
            print()
        
        # Location probabilities
        print("📍 VIEWING PROBABILITIES")
        for location in self.locations:
            prob = self.calculate_viewing_probability(location, current_kp)
            print(f"   {location:<20}: {prob:>3.0f}%")
        print()
        
        # Expected colors
        colors = self.predict_colors(current_kp, solar_wind)
        print("🎨 EXPECTED COLORS")
        for color in colors:
            info = self.aurora_colors[color]
            print(f"   {color}: {info['altitude']} altitude ({info['cause']})")
        print()
        
        # Photography tips
        print("📸 PHOTOGRAPHY TIPS")
        tips = self.generate_photography_tips(current_kp, solar_wind)
        for tip in tips:
            print(f"   {tip}")
        print()
        
        # 3-day forecast
        three_day = comprehensive_data.get('3day_forecast')
        if three_day:
            print("🗓️ 3-DAY SPACE WEATHER FORECAST")
            for date, data in three_day.items():
                print(f"   {date}: {data['aurora_activity']}")
            print()
        
        # Aurora forecast map
        aurora_forecast = comprehensive_data.get('aurora_forecast')
        if aurora_forecast:
            print("🗺️ AURORA FORECAST MAP")
            print(f"   View Line Latitude: {aurora_forecast['viewline_lat']:.1f}°")
            print(f"   Hemispheric Power: {aurora_forecast['hemispheric_power']:.1f} GW")
            print()
        
        print("✨ Happy Aurora Hunting with Real-Time Data! ✨")
        print("🌌" * 20)
    
    def _generate_fallback_report(self) -> None:
        """Generate fallback report if NOAA data is unavailable"""
        print("📊 FALLBACK MODE - Using Simulated Data")
        print("(Check your internet connection for real-time data)")
        print()
        
        # Import and use the original tracker as fallback
        try:
            from aurora_tracker import AuroraTracker
            fallback_tracker = AuroraTracker()
            fallback_tracker.generate_full_report()
        except ImportError:
            print("❌ Fallback tracker not available")
            print("Please ensure aurora_tracker.py is in the same directory")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test mode - just test NOAA API
        print("🧪 Testing NOAA API Connection...")
        noaa = NOAASpaceWeather()
        
        current_kp = noaa.get_current_kp_index()
        if current_kp:
            print(f"✅ Successfully connected to NOAA API")
            print(f"   Current KP Index: {current_kp}")
        else:
            print("❌ Unable to connect to NOAA API")
            print("   Check your internet connection")
        return
    
    # Generate full real-time report
    tracker = RealTimeAuroraTracker()
    tracker.generate_comprehensive_report()

if __name__ == "__main__":
    main()