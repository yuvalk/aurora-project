#!/usr/bin/env python3
"""
Aurora API Server - Real-time Data Endpoint
Serves real NOAA space weather data to web dashboard
"""

import json
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time
import logging
from typing import Dict, Optional

from noaa_data import NOAASpaceWeather

class AuroraAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Aurora API"""
    
    def __init__(self, *args, **kwargs):
        self.noaa = NOAASpaceWeather()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        # Set CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        try:
            if path == '/api/current':
                self._handle_current_conditions()
            elif path == '/api/forecast':
                self._handle_forecast(query_params)
            elif path == '/api/probabilities':
                self._handle_probabilities()
            elif path == '/api/solar-wind':
                self._handle_solar_wind()
            elif path == '/api/alerts':
                self._handle_alerts()
            elif path == '/api/comprehensive':
                self._handle_comprehensive()
            elif path == '/api/health':
                self._handle_health_check()
            else:
                self._send_error(404, "Endpoint not found")
        except Exception as e:
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _handle_current_conditions(self):
        """Handle current conditions request"""
        current_kp = self.noaa.get_current_kp_index()
        
        if current_kp is None:
            self._send_error(503, "Unable to fetch current KP index")
            return
        
        response = {
            'timestamp': datetime.datetime.now().isoformat(),
            'kp_index': current_kp,
            'activity_level': self._get_activity_level(current_kp),
            'visibility_zone': self._get_visibility_zone(current_kp),
            'source': 'NOAA Space Weather Prediction Center'
        }
        
        self._send_json_response(response)
    
    def _handle_forecast(self, query_params):
        """Handle forecast request"""
        days = int(query_params.get('days', [3])[0])
        forecast_data = self.noaa.get_kp_forecast(days)
        
        if not forecast_data:
            self._send_error(503, "Unable to fetch forecast data")
            return
        
        # Group by day for easier consumption
        daily_forecast = {}
        for entry in forecast_data:
            date = entry['date']
            if date not in daily_forecast:
                daily_forecast[date] = {
                    'date': date,
                    'max_kp': entry['kp_index'],
                    'activity_level': entry['activity_level'],
                    'hourly': []
                }
            else:
                # Update max KP for the day
                if entry['kp_index'] > daily_forecast[date]['max_kp']:
                    daily_forecast[date]['max_kp'] = entry['kp_index']
                    daily_forecast[date]['activity_level'] = entry['activity_level']
            
            daily_forecast[date]['hourly'].append(entry)
        
        response = {
            'timestamp': datetime.datetime.now().isoformat(),
            'forecast': list(daily_forecast.values()),
            'source': 'NOAA Space Weather Prediction Center'
        }
        
        self._send_json_response(response)
    
    def _handle_probabilities(self):
        """Handle viewing probabilities request"""
        current_kp = self.noaa.get_current_kp_index()
        
        if current_kp is None:
            self._send_error(503, "Unable to fetch current KP index")
            return
        
        locations = {
            "Fairbanks, Alaska": {"magnetic_lat": 65.1},
            "Yellowknife, Canada": {"magnetic_lat": 68.6},
            "Reykjavik, Iceland": {"magnetic_lat": 64.8},
            "Tromsø, Norway": {"magnetic_lat": 66.7},
            "Anchorage, Alaska": {"magnetic_lat": 61.8},
            "Calgary, Canada": {"magnetic_lat": 58.2},
            "Seattle, Washington": {"magnetic_lat": 54.2},
            "Minneapolis, Minnesota": {"magnetic_lat": 54.8}
        }
        
        probabilities = []
        for location, data in locations.items():
            prob = self._calculate_viewing_probability(location, current_kp, data['magnetic_lat'])
            probabilities.append({
                'location': location,
                'probability': round(prob, 1),
                'magnetic_latitude': data['magnetic_lat']
            })
        
        response = {
            'timestamp': datetime.datetime.now().isoformat(),
            'current_kp': current_kp,
            'probabilities': probabilities,
            'source': 'NOAA Space Weather Prediction Center'
        }
        
        self._send_json_response(response)
    
    def _handle_solar_wind(self):
        """Handle solar wind data request"""
        solar_wind = self.noaa.get_solar_wind_data()
        
        if not solar_wind:
            self._send_error(503, "Unable to fetch solar wind data")
            return
        
        response = {
            'timestamp': datetime.datetime.now().isoformat(),
            'solar_wind': solar_wind,
            'source': 'NOAA Space Weather Prediction Center'
        }
        
        self._send_json_response(response)
    
    def _handle_alerts(self):
        """Handle geomagnetic alerts request"""
        alerts = self.noaa.get_geomagnetic_alerts()
        
        response = {
            'timestamp': datetime.datetime.now().isoformat(),
            'alerts': alerts,
            'count': len(alerts),
            'source': 'NOAA Space Weather Prediction Center'
        }
        
        self._send_json_response(response)
    
    def _handle_comprehensive(self):
        """Handle comprehensive data request"""
        try:
            comprehensive_data = self.noaa.get_comprehensive_data()
            
            # Add calculated fields
            if comprehensive_data.get('current_kp'):
                kp = comprehensive_data['current_kp']
                comprehensive_data['activity_level'] = self._get_activity_level(kp)
                comprehensive_data['visibility_zone'] = self._get_visibility_zone(kp)
                comprehensive_data['predicted_colors'] = self._predict_colors(kp)
            
            comprehensive_data['source'] = 'NOAA Space Weather Prediction Center'
            
            self._send_json_response(comprehensive_data)
            
        except Exception as e:
            self._send_error(503, f"Unable to fetch comprehensive data: {str(e)}")
    
    def _handle_health_check(self):
        """Handle health check request"""
        try:
            # Test NOAA API connection
            test_kp = self.noaa.get_current_kp_index()
            status = "healthy" if test_kp is not None else "unhealthy"
            
            response = {
                'status': status,
                'timestamp': datetime.datetime.now().isoformat(),
                'api_accessible': test_kp is not None,
                'version': '1.1.0'
            }
            
            self._send_json_response(response)
            
        except Exception as e:
            self._send_error(503, f"Health check failed: {str(e)}")
    
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
    
    def _get_visibility_zone(self, kp: float) -> str:
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
    
    def _calculate_viewing_probability(self, location: str, kp_index: float, magnetic_lat: float) -> float:
        """Calculate viewing probability"""
        threshold_lat = 67 - (kp_index * 2.5)
        
        if magnetic_lat >= threshold_lat:
            probability = min(95, (magnetic_lat - threshold_lat + 5) * 10)
        else:
            probability = max(0, (magnetic_lat - threshold_lat + 10) * 2)
        
        return max(0, min(100, probability))
    
    def _predict_colors(self, kp_index: float) -> list:
        """Predict likely aurora colors"""
        colors = []
        
        if kp_index >= 1:
            colors.append("Green")
        if kp_index >= 4:
            colors.append("Red")
        if kp_index >= 3:
            colors.append("Pink")
        if kp_index >= 4:
            colors.append("Blue")
        if kp_index >= 6:
            colors.append("Purple")
        
        return colors if colors else ["Green"]
    
    def _send_json_response(self, data: dict):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def _send_error(self, code: int, message: str):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_data = {
            'error': message,
            'timestamp': datetime.datetime.now().isoformat(),
            'code': code
        }
        
        json_data = json.dumps(error_data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        pass

class AuroraAPIServer:
    """Aurora API Server with real-time data caching"""
    
    def __init__(self, host='localhost', port=8001):
        self.host = host
        self.port = port
        self.server = None
        self.running = False
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Start the API server"""
        self.server = HTTPServer((self.host, self.port), AuroraAPIHandler)
        self.running = True
        
        self.logger.info(f"🚀 Aurora API Server starting on {self.host}:{self.port}")
        self.logger.info("📡 Serving real-time NOAA space weather data")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the API server"""
        if self.server:
            self.server.shutdown()
            self.running = False
            self.logger.info("🛑 Aurora API Server stopped")

def main():
    """Main function to start the API server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Aurora API Server with Real-time NOAA Data')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8001, help='Port to bind to')
    parser.add_argument('--test', action='store_true', help='Test NOAA API connection')
    
    args = parser.parse_args()
    
    if args.test:
        # Test NOAA API connection
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
    
    # Start the API server
    server = AuroraAPIServer(args.host, args.port)
    server.start()

if __name__ == "__main__":
    main()