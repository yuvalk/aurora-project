# 🌐 Real-time NOAA Data Integration Setup

This guide explains how to set up and use the real-time NOAA Space Weather data integration in the Aurora Borealis Toolkit.

## 🚀 Quick Start

### 1. Test NOAA API Connection
```bash
# Test if NOAA API is accessible
python3 src/aurora_api.py --test
```

### 2. Run Real-time Aurora Tracker
```bash
# Get live aurora data from NOAA
python3 src/aurora_tracker_real.py
```

### 3. Start API Server (Optional)
```bash
# Start the API server for web dashboard
python3 src/aurora_api.py --host localhost --port 8001
```

### 4. Launch Real-time Web Dashboard
```bash
# Start web server
cd web && python3 -m http.server 8000

# Open in browser
# http://localhost:8000/real-time.html
```

## 🔧 Components

### 📡 NOAA Data Client (`src/noaa_data.py`)
- **NOAASpaceWeather class**: Main API client
- **Real-time KP index**: Current geomagnetic activity
- **KP forecasts**: 3-hour resolution predictions
- **Solar wind data**: Magnetic field and plasma parameters
- **Geomagnetic alerts**: Storm warnings and watches
- **Error handling**: Robust network resilience

### 🎯 Real-time Tracker (`src/aurora_tracker_real.py`)
- **Live data integration**: NOAA API consumption
- **Fallback mode**: Graceful degradation to simulated data
- **Enhanced reporting**: Solar wind conditions and alerts
- **Photography tips**: Adaptive based on real conditions

### 🚀 API Server (`src/aurora_api.py`)
- **RESTful endpoints**: JSON API for web dashboard
- **CORS support**: Cross-origin requests enabled
- **Health monitoring**: API status and connectivity
- **Real-time data serving**: Live space weather data

### 🌐 Web Dashboard (`web/real-time.html`)
- **Live data display**: Real-time NOAA integration
- **Connection monitoring**: API health indicators
- **Enhanced UI**: Solar wind and alerts display
- **Fallback support**: Graceful degradation

## 🔗 API Endpoints

### Current Conditions
```
GET /api/current
```
Returns current KP index and activity level.

### Forecast Data
```
GET /api/forecast?days=3
```
Returns KP forecast for specified number of days.

### Viewing Probabilities
```
GET /api/probabilities
```
Returns viewing probabilities for all locations.

### Solar Wind Data
```
GET /api/solar-wind
```
Returns current solar wind conditions.

### Geomagnetic Alerts
```
GET /api/alerts
```
Returns active geomagnetic storm alerts.

### Comprehensive Data
```
GET /api/comprehensive
```
Returns all available space weather data.

### Health Check
```
GET /api/health
```
Returns API health status.

## 🌟 Data Sources

### NOAA Space Weather Prediction Center
- **Base URL**: https://services.swpc.noaa.gov
- **KP Index**: `/products/noaa-planetary-k-index.json`
- **KP Forecast**: `/products/noaa-planetary-k-index-forecast.json`
- **Solar Wind**: `/products/solar-wind/mag-2-hour.json`
- **Alerts**: `/products/alerts.json`

### Data Update Frequency
- **KP Index**: Every 3 hours
- **KP Forecast**: Every 6 hours
- **Solar Wind**: Every 2 hours
- **Alerts**: Real-time

## 🔬 Scientific Accuracy

### KP Index
- **Scale**: 0-9 (logarithmic)
- **Resolution**: 0.33 steps
- **Update**: 3-hour intervals
- **Source**: Global magnetometer network

### Solar Wind Parameters
- **Speed**: km/s (typical range: 300-800)
- **Density**: particles/cm³ (typical range: 1-20)
- **Bz**: nT (southward component critical for aurora)
- **Bt**: nT (total magnetic field strength)

### Aurora Potential Calculation
```python
def calculate_aurora_potential(speed, bz):
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
```

## 🛠️ Configuration

### Environment Variables
```bash
# Optional: Set custom NOAA API timeout
export NOAA_API_TIMEOUT=10

# Optional: Set custom API server port
export AURORA_API_PORT=8001
```

### Settings File
```json
{
  "noaa_api": {
    "timeout": 10,
    "retry_attempts": 3,
    "base_url": "https://services.swpc.noaa.gov"
  },
  "dashboard": {
    "refresh_interval": 900,
    "fallback_mode": "auto",
    "notifications": false
  }
}
```

## 🚨 Error Handling

### Network Issues
- **Timeout handling**: 10-second timeout on API calls
- **Retry logic**: Automatic retry on network errors
- **Fallback mode**: Graceful degradation to simulated data

### Data Validation
- **Header parsing**: Skip CSV header rows in JSON data
- **Type checking**: Validate numeric values
- **Range validation**: Ensure KP index 0-9 range

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🎯 Use Cases

### Aurora Hunters
- **Real-time monitoring**: Live KP index tracking
- **Forecast planning**: Multi-day aurora predictions
- **Location selection**: Probability-based site selection
- **Photography preparation**: Equipment and settings advice

### Researchers
- **Data export**: JSON format for analysis
- **Historical tracking**: Comprehensive data logging
- **API integration**: Embed in research applications
- **Validation**: Compare with other data sources

### Educators
- **Live demonstrations**: Real-time space weather
- **Scientific accuracy**: Professional-grade data
- **Visual appeal**: Beautiful dashboard interface
- **Educational content**: Aurora science explanation

## 🔧 Troubleshooting

### Common Issues

**API Connection Failed**
```bash
# Check internet connectivity
ping services.swpc.noaa.gov

# Test API endpoint
curl https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json
```

**Data Parsing Errors**
```bash
# Check log output
python3 src/aurora_tracker_real.py 2>&1 | grep ERROR
```

**Web Dashboard Not Loading**
```bash
# Check API server status
python3 src/aurora_api.py --test

# Check web server
curl http://localhost:8000/real-time.html
```

### Debug Mode
```bash
# Enable verbose logging
export PYTHONPATH=$PYTHONPATH:src
python3 -c "import logging; logging.basicConfig(level=logging.DEBUG)"
python3 src/aurora_tracker_real.py
```

## 📈 Performance

### API Response Times
- **Current KP**: ~500ms
- **Forecast**: ~800ms
- **Solar Wind**: ~600ms
- **Comprehensive**: ~2000ms

### Data Size
- **KP Index**: ~10KB
- **Forecast**: ~15KB
- **Solar Wind**: ~20KB
- **Total**: ~50KB per request

### Caching
- **Client-side**: 5-minute cache
- **Server-side**: 2-minute cache
- **Browser**: Standard HTTP caching

## 🌟 Future Enhancements

### Planned Features
- [ ] Real-time notifications
- [ ] Historical data analysis
- [ ] Advanced visualization
- [ ] Mobile app integration
- [ ] Multi-language support
- [ ] Offline mode
- [ ] Custom alerts
- [ ] Social sharing

### Data Sources
- [ ] ESA Space Weather Portal
- [ ] Japanese space weather data
- [ ] Real-time imagery
- [ ] Magnetometer data
- [ ] All-sky cameras

---

**Built with ❤️ for aurora enthusiasts using real-time NOAA data!**

*This integration transforms the Aurora Borealis Toolkit from a simulation into a professional-grade real-time space weather monitoring system.*