#!/usr/bin/env python3
"""
NOAA Space Weather Data Integration
Real-time aurora data from NOAA Space Weather Prediction Center
"""

import json
import urllib.request
import urllib.error
import datetime
import time
import logging
from typing import Dict, List, Optional, Tuple

class NOAASpaceWeather:
    """
    Interface to NOAA Space Weather Prediction Center APIs
    Provides real-time geomagnetic and aurora data
    """
    
    def __init__(self):
        self.base_url = "https://services.swpc.noaa.gov"
        self.endpoints = {
            'kp_index': '/products/noaa-planetary-k-index.json',
            'kp_forecast': '/products/noaa-planetary-k-index-forecast.json',
            '3day_forecast': '/products/3-day-forecast.json',
            'solar_wind': '/products/solar-wind/mag-2-hour.json',
            'geomagnetic_storm': '/products/alerts.json',
            'aurora_forecast': '/products/aurora-forecast-northern-hemisphere.json'
        }
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _make_request(self, endpoint: str, timeout: int = 10) -> Optional[Dict]:
        """
        Make HTTP request to NOAA API with error handling
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            self.logger.info(f"Fetching data from: {url}")
            
            # Set up request with proper headers
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Aurora-Borealis-Toolkit/1.1.0')
            req.add_header('Accept', 'application/json')
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    self.logger.info(f"Successfully fetched {len(data)} records")
                    return data
                else:
                    self.logger.error(f"HTTP {response.getcode()} error")
                    return None
                    
        except urllib.error.URLError as e:
            self.logger.error(f"Network error: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None
    
    def get_current_kp_index(self) -> Optional[float]:
        """
        Get the most recent KP index value
        """
        data = self._make_request(self.endpoints['kp_index'])
        if not data:
            return None
            
        try:
            # Skip header row (first entry contains column names)
            if len(data) > 1:
                latest_entry = data[1]  # Second entry is the most recent data
                kp_value = float(latest_entry[1])  # KP value is in second column
                
                self.logger.info(f"Current KP index: {kp_value}")
                return kp_value
            else:
                self.logger.error("No data entries found")
                return None
                
        except (IndexError, ValueError, KeyError) as e:
            self.logger.error(f"Error parsing KP data: {e}")
            return None
    
    def get_kp_forecast(self, days: int = 3) -> List[Dict]:
        """
        Get KP index forecast for the next few days
        """
        data = self._make_request(self.endpoints['kp_forecast'])
        if not data:
            return []
            
        forecast = []
        try:
            # Skip header row and process forecast data
            for entry in data[1:days * 8 + 1]:  # Skip header, get requested days
                timestamp = entry[0]
                kp_value = float(entry[1])
                
                # Parse timestamp
                dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                
                forecast.append({
                    'timestamp': dt,
                    'date': dt.strftime('%Y-%m-%d'),
                    'time': dt.strftime('%H:%M'),
                    'kp_index': kp_value,
                    'activity_level': self._get_activity_level(kp_value)
                })
                
        except (IndexError, ValueError, KeyError) as e:
            self.logger.error(f"Error parsing forecast data: {e}")
            
        return forecast
    
    def get_3day_forecast(self) -> Optional[Dict]:
        """
        Get the official 3-day space weather forecast
        """
        data = self._make_request(self.endpoints['3day_forecast'])
        if not data:
            return None
            
        try:
            # Process the 3-day forecast data
            forecast = {}
            for entry in data:
                date_str = entry[0]
                
                # Extract forecast values
                forecast[date_str] = {
                    'date': date_str,
                    'radio_blackout': entry[1],
                    'solar_radiation': entry[2],
                    'geomagnetic_storm': entry[3],
                    'aurora_activity': self._map_geomagnetic_to_aurora(entry[3])
                }
                
            return forecast
            
        except (IndexError, KeyError) as e:
            self.logger.error(f"Error parsing 3-day forecast: {e}")
            return None
    
    def get_solar_wind_data(self) -> Optional[Dict]:
        """
        Get current solar wind conditions
        """
        data = self._make_request(self.endpoints['solar_wind'])
        if not data:
            return None
            
        try:
            # Skip header row and get latest data
            if len(data) > 1:
                latest = data[1]
                
                solar_wind = {
                    'timestamp': latest[0],
                    'bx': float(latest[1]) if latest[1] != '' else 0.0,    # nT
                    'by': float(latest[2]) if latest[2] != '' else 0.0,    # nT
                    'bz': float(latest[3]) if latest[3] != '' else 0.0,    # nT (important for aurora)
                    'bt': float(latest[4]) if latest[4] != '' else 0.0,    # nT
                    'speed': float(latest[5]) if latest[5] != '' else 0.0, # km/s
                    'density': float(latest[6]) if latest[6] != '' else 0.0 # particles/cm³
                }
                
                # Calculate aurora potential based on Bz and speed
                solar_wind['aurora_potential'] = self._calculate_aurora_potential(
                    solar_wind['speed'], solar_wind['bz']
                )
                
                return solar_wind
            else:
                self.logger.error("No solar wind data available")
                return None
                
        except (IndexError, ValueError) as e:
            self.logger.error(f"Error parsing solar wind data: {e}")
            return None
    
    def get_geomagnetic_alerts(self) -> List[Dict]:
        """
        Get current geomagnetic storm alerts and warnings
        """
        data = self._make_request(self.endpoints['geomagnetic_storm'])
        if not data:
            return []
            
        alerts = []
        try:
            for alert in data:
                # Filter for geomagnetic alerts
                if 'geomagnetic' in alert.get('message', '').lower():
                    alerts.append({
                        'timestamp': alert['issue_datetime'],
                        'message': alert['message'],
                        'type': alert.get('product_id', 'unknown'),
                        'severity': self._extract_severity(alert['message'])
                    })
                    
        except (KeyError, TypeError) as e:
            self.logger.error(f"Error parsing alerts: {e}")
            
        return alerts
    
    def get_aurora_forecast_map(self) -> Optional[Dict]:
        """
        Get aurora forecast with geographic boundaries
        """
        data = self._make_request(self.endpoints['aurora_forecast'])
        if not data:
            return None
            
        try:
            # Process aurora forecast data
            forecast = {
                'timestamp': data[0]['Forecast_Time'],
                'viewline_lat': float(data[0]['View_Line']),
                'aurora_activity': data[0]['Aurora_Activity'],
                'hemispheric_power': float(data[0]['Hemispheric_Power'])
            }
            
            return forecast
            
        except (KeyError, ValueError, IndexError) as e:
            self.logger.error(f"Error parsing aurora forecast: {e}")
            return None
    
    def _get_activity_level(self, kp: float) -> str:
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
    
    def _map_geomagnetic_to_aurora(self, geo_level: str) -> str:
        """Map geomagnetic storm level to aurora activity"""
        level_map = {
            'G1': 'Minor aurora activity',
            'G2': 'Moderate aurora activity',
            'G3': 'Strong aurora activity',
            'G4': 'Severe aurora activity',
            'G5': 'Extreme aurora activity'
        }
        return level_map.get(geo_level, 'Unknown')
    
    def _calculate_aurora_potential(self, speed: float, bz: float) -> str:
        """Calculate aurora potential from solar wind parameters"""
        # Simplified formula based on solar wind speed and Bz component
        if bz < -10 and speed > 500:
            return "Very High"
        elif bz < -5 and speed > 400:
            return "High"
        elif bz < 0 and speed > 350:
            return "Moderate"
        elif speed > 300:
            return "Low"
        else:
            return "Very Low"
    
    def _extract_severity(self, message: str) -> str:
        """Extract severity level from alert message"""
        message_lower = message.lower()
        if 'extreme' in message_lower or 'g5' in message_lower:
            return "Extreme"
        elif 'severe' in message_lower or 'g4' in message_lower:
            return "Severe"
        elif 'strong' in message_lower or 'g3' in message_lower:
            return "Strong"
        elif 'moderate' in message_lower or 'g2' in message_lower:
            return "Moderate"
        elif 'minor' in message_lower or 'g1' in message_lower:
            return "Minor"
        else:
            return "Unknown"
    
    def get_comprehensive_data(self) -> Dict:
        """
        Get all available data in one comprehensive request
        """
        self.logger.info("Fetching comprehensive NOAA space weather data...")
        
        data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'current_kp': self.get_current_kp_index(),
            'kp_forecast': self.get_kp_forecast(),
            '3day_forecast': self.get_3day_forecast(),
            'solar_wind': self.get_solar_wind_data(),
            'alerts': self.get_geomagnetic_alerts(),
            'aurora_forecast': self.get_aurora_forecast_map()
        }
        
        self.logger.info("Comprehensive data fetch completed")
        return data

def main():
    """
    Demo function to test NOAA data integration
    """
    print("🌌 NOAA Space Weather Data Integration Demo 🌌")
    print("=" * 50)
    
    noaa = NOAASpaceWeather()
    
    # Test current KP index
    print("\n🔮 Current KP Index:")
    current_kp = noaa.get_current_kp_index()
    if current_kp:
        print(f"   KP: {current_kp}")
        print(f"   Activity: {noaa._get_activity_level(current_kp)}")
    else:
        print("   Unable to fetch current KP index")
    
    # Test KP forecast
    print("\n📊 KP Forecast (next 24 hours):")
    forecast = noaa.get_kp_forecast(days=1)
    for entry in forecast[:8]:  # Show first 8 entries (24 hours)
        print(f"   {entry['date']} {entry['time']}: KP {entry['kp_index']} ({entry['activity_level']})")
    
    # Test solar wind
    print("\n🌟 Solar Wind Conditions:")
    solar_wind = noaa.get_solar_wind_data()
    if solar_wind:
        print(f"   Speed: {solar_wind['speed']:.1f} km/s")
        print(f"   Density: {solar_wind['density']:.1f} particles/cm³")
        print(f"   Bz: {solar_wind['bz']:.1f} nT")
        print(f"   Aurora Potential: {solar_wind['aurora_potential']}")
    
    # Test alerts
    print("\n🚨 Geomagnetic Alerts:")
    alerts = noaa.get_geomagnetic_alerts()
    if alerts:
        for alert in alerts[:3]:  # Show first 3 alerts
            print(f"   {alert['severity']}: {alert['message'][:100]}...")
    else:
        print("   No current geomagnetic alerts")
    
    print("\n✨ NOAA data integration demo complete! ✨")

if __name__ == "__main__":
    main()