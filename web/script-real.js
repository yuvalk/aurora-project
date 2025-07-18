// Real-time Aurora Dashboard with NOAA Data Integration
// Enhanced JavaScript for live space weather data

class RealTimeAuroraDashboard {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8001/api';
        this.fallbackMode = false;
        this.refreshInterval = 15 * 60 * 1000; // 15 minutes
        this.autoRefreshTimer = null;
        
        this.locations = {
            "Fairbanks, Alaska": { magnetic_lat: 65.1 },
            "Yellowknife, Canada": { magnetic_lat: 68.6 },
            "Reykjavik, Iceland": { magnetic_lat: 64.8 },
            "Tromsø, Norway": { magnetic_lat: 66.7 },
            "Anchorage, Alaska": { magnetic_lat: 61.8 },
            "Calgary, Canada": { magnetic_lat: 58.2 },
            "Seattle, Washington": { magnetic_lat: 54.2 },
            "Minneapolis, Minnesota": { magnetic_lat: 54.8 }
        };

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAPIHealth();
        this.loadRealTimeData();
        this.startAutoRefresh();
    }

    setupEventListeners() {
        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadRealTimeData();
        });

        // Export button
        document.getElementById('exportBtn').addEventListener('click', () => {
            this.exportReport();
        });

        // Settings button
        document.getElementById('settingsBtn').addEventListener('click', () => {
            this.showSettings();
        });

        // Settings modal
        document.getElementById('closeSettings').addEventListener('click', () => {
            this.hideSettings();
        });

        // Save settings
        document.getElementById('saveSettings').addEventListener('click', () => {
            this.saveSettings();
        });

        // Close modal on outside click
        document.getElementById('settingsModal').addEventListener('click', (e) => {
            if (e.target === document.getElementById('settingsModal')) {
                this.hideSettings();
            }
        });
    }

    async checkAPIHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.showDataSource('🌐 Live NOAA Data');
                this.fallbackMode = false;
            } else {
                this.showDataSource('⚠️ API Issues - Using Fallback');
                this.fallbackMode = true;
            }
        } catch (error) {
            console.warn('API server not available, using fallback mode');
            this.showDataSource('📱 Simulated Data');
            this.fallbackMode = true;
        }
    }

    async loadRealTimeData() {
        if (this.fallbackMode) {
            this.loadFallbackData();
            return;
        }

        try {
            // Show loading state
            document.body.classList.add('loading');
            
            // Fetch comprehensive real-time data
            const response = await fetch(`${this.apiBaseUrl}/comprehensive`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Update all dashboard sections with real data
            this.updateCurrentConditions(data);
            this.updateForecast(data);
            this.updateProbabilities(data);
            this.updateColors(data);
            this.updatePhotographyTips(data);
            this.updateSolarWind(data);
            this.updateAlerts(data);
            
            // Update data source indicator
            this.showDataSource('🌐 Live NOAA Data');
            
        } catch (error) {
            console.error('Failed to fetch real-time data:', error);
            this.showDataSource('⚠️ Connection Error');
            this.loadFallbackData();
        } finally {
            document.body.classList.remove('loading');
        }
    }

    updateCurrentConditions(data) {
        const currentKp = data.current_kp || 0;
        const activityLevel = data.activity_level || 'Unknown';
        const visibilityZone = data.visibility_zone || 'Unknown';
        const timestamp = new Date(data.timestamp).toLocaleString();

        document.getElementById('currentKp').textContent = currentKp.toFixed(1);
        document.getElementById('activityLevel').textContent = activityLevel;
        document.getElementById('visibilityZone').textContent = visibilityZone;
        document.getElementById('lastUpdated').textContent = `Last updated: ${timestamp}`;

        // Update activity level styling
        const activityElement = document.getElementById('activityLevel');
        activityElement.className = `activity-level activity-${activityLevel.toLowerCase().replace(/\s+/g, '-')}`;
    }

    updateForecast(data) {
        const forecastList = document.getElementById('forecastList');
        forecastList.innerHTML = '';

        const forecast = data.kp_forecast || [];
        
        // Group forecast by day
        const dailyForecast = {};
        forecast.forEach(entry => {
            const date = entry.date;
            if (!dailyForecast[date]) {
                dailyForecast[date] = {
                    date: date,
                    max_kp: entry.kp_index,
                    activity_level: entry.activity_level,
                    entries: []
                };
            } else {
                if (entry.kp_index > dailyForecast[date].max_kp) {
                    dailyForecast[date].max_kp = entry.kp_index;
                    dailyForecast[date].activity_level = entry.activity_level;
                }
            }
            dailyForecast[date].entries.push(entry);
        });

        // Display daily forecast
        Object.values(dailyForecast).slice(0, 7).forEach(day => {
            const forecastItem = document.createElement('div');
            forecastItem.className = 'forecast-item';
            
            const date = new Date(day.date).toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric' 
            });
            
            forecastItem.innerHTML = `
                <div class="forecast-date">${date}</div>
                <div class="forecast-kp">KP ${day.max_kp.toFixed(1)}</div>
                <div class="forecast-activity">${day.activity_level}</div>
            `;
            
            forecastList.appendChild(forecastItem);
        });
    }

    updateProbabilities(data) {
        const locationList = document.getElementById('locationList');
        locationList.innerHTML = '';

        const currentKp = data.current_kp || 0;

        Object.entries(this.locations).forEach(([location, locationData]) => {
            const probability = this.calculateViewingProbability(location, currentKp, locationData.magnetic_lat);
            
            const locationItem = document.createElement('div');
            locationItem.className = 'location-item';
            
            locationItem.innerHTML = `
                <div class="location-name">${location}</div>
                <div class="location-probability">${probability.toFixed(0)}%</div>
            `;
            
            locationList.appendChild(locationItem);
        });
    }

    updateColors(data) {
        const colorList = document.getElementById('colorList');
        colorList.innerHTML = '';

        const predictedColors = data.predicted_colors || ['Green'];
        
        const colorInfo = {
            "Green": { altitude: "80-150 km", cause: "Oxygen atoms", color: "#00ff88" },
            "Red": { altitude: "150-300 km", cause: "High altitude oxygen", color: "#ff0088" },
            "Blue": { altitude: "80-120 km", cause: "Nitrogen molecules", color: "#0088ff" },
            "Pink": { altitude: "80-150 km", cause: "Nitrogen + oxygen mix", color: "#ff0088" },
            "Purple": { altitude: "80-120 km", cause: "Nitrogen at lower altitudes", color: "#8800ff" }
        };

        predictedColors.forEach(colorName => {
            const info = colorInfo[colorName];
            if (!info) return;
            
            const colorItem = document.createElement('div');
            colorItem.className = 'color-item';
            
            colorItem.innerHTML = `
                <div class="color-swatch" style="background-color: ${info.color}; border-radius: 50%; width: 24px; height: 24px;"></div>
                <div class="color-info">
                    <div class="color-name">${colorName}</div>
                    <div class="color-details">${info.altitude} - ${info.cause}</div>
                </div>
            `;
            
            colorList.appendChild(colorItem);
        });
    }

    updatePhotographyTips(data) {
        const currentKp = data.current_kp || 0;
        const solarWind = data.solar_wind || {};
        const tipsList = document.getElementById('tipsList');
        
        // Clear existing tips
        tipsList.innerHTML = '';
        
        // Base tips
        const baseTips = [
            "🌍 Find a location away from city lights",
            "🕐 Best viewing: 10 PM - 2 AM local time",
            "🌙 New moon periods offer darkest skies",
            "📱 Use aurora prediction apps for real-time updates"
        ];

        // Add KP-specific tips
        if (currentKp >= 3) {
            baseTips.push("📸 Camera settings: ISO 800-1600, f/2.8, 15-20 sec exposure");
            baseTips.push("🎯 Focus on infinity or distant lights");
            baseTips.push("🔋 Bring extra batteries - cold drains them fast!");
        }

        if (currentKp >= 5) {
            baseTips.push("🎨 Expect dynamic, dancing aurora!");
            baseTips.push("📹 Consider time-lapse photography");
            baseTips.push("👥 Aurora may be visible to naked eye");
        }

        // Add solar wind specific tips
        if (solarWind.bz && solarWind.bz < -5) {
            baseTips.push("⚡ Strong southward magnetic field - expect bright displays!");
        }
        if (solarWind.speed && solarWind.speed > 600) {
            baseTips.push("🌟 High-speed solar wind - aurora may be more active!");
        }

        baseTips.forEach(tip => {
            const tipElement = document.createElement('div');
            tipElement.className = 'tip';
            tipElement.textContent = tip;
            tipsList.appendChild(tipElement);
        });
    }

    updateSolarWind(data) {
        const solarWind = data.solar_wind;
        if (!solarWind) return;

        // Add solar wind information to the dashboard
        const solarWindInfo = document.createElement('div');
        solarWindInfo.innerHTML = `
            <div class="solar-wind-info">
                <h3>🌟 Solar Wind Conditions</h3>
                <div>Speed: ${solarWind.speed.toFixed(1)} km/s</div>
                <div>Density: ${solarWind.density.toFixed(1)} particles/cm³</div>
                <div>Bz: ${solarWind.bz.toFixed(1)} nT</div>
                <div>Aurora Potential: ${solarWind.aurora_potential}</div>
            </div>
        `;
        
        // Add to tips section or create new section
        const tipsList = document.getElementById('tipsList');
        tipsList.appendChild(solarWindInfo);
    }

    updateAlerts(data) {
        const alerts = data.alerts || [];
        
        if (alerts.length > 0) {
            const alertsInfo = document.createElement('div');
            alertsInfo.innerHTML = `
                <div class="alerts-info">
                    <h3>🚨 Space Weather Alerts</h3>
                    ${alerts.slice(0, 3).map(alert => `
                        <div class="alert-item">
                            <span class="alert-severity">${alert.severity}</span>
                            <span class="alert-message">${alert.message.substring(0, 100)}...</span>
                        </div>
                    `).join('')}
                </div>
            `;
            
            const factContent = document.getElementById('factContent');
            factContent.appendChild(alertsInfo);
        }
    }

    calculateViewingProbability(location, kpIndex, magneticLat) {
        const thresholdLat = 67 - (kpIndex * 2.5);
        
        if (magneticLat >= thresholdLat) {
            return Math.min(95, (magneticLat - thresholdLat + 5) * 10);
        } else {
            return Math.max(0, (magneticLat - thresholdLat + 10) * 2);
        }
    }

    loadFallbackData() {
        // Use original simulation logic when real data is unavailable
        console.log('Loading fallback data...');
        
        // Import original dashboard logic
        const originalDashboard = new AuroraDashboard();
        originalDashboard.refreshData();
    }

    showDataSource(source) {
        // Update data source indicator
        let indicator = document.getElementById('dataSourceIndicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'dataSourceIndicator';
            indicator.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 1000;
            `;
            document.body.appendChild(indicator);
        }
        indicator.textContent = source;
    }

    exportReport() {
        // Enhanced export with real-time data
        const reportData = {
            timestamp: new Date().toISOString(),
            dataSource: this.fallbackMode ? 'Simulated' : 'NOAA Real-time',
            currentKp: document.getElementById('currentKp').textContent,
            activityLevel: document.getElementById('activityLevel').textContent,
            visibilityZone: document.getElementById('visibilityZone').textContent,
            locations: Array.from(document.querySelectorAll('.location-item')).map(item => ({
                name: item.querySelector('.location-name').textContent,
                probability: item.querySelector('.location-probability').textContent
            })),
            forecast: Array.from(document.querySelectorAll('.forecast-item')).map(item => ({
                date: item.querySelector('.forecast-date').textContent,
                kp: item.querySelector('.forecast-kp').textContent,
                activity: item.querySelector('.forecast-activity').textContent
            })),
            realTimeData: !this.fallbackMode
        };

        const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `aurora-report-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    showSettings() {
        document.getElementById('settingsModal').style.display = 'block';
    }

    hideSettings() {
        document.getElementById('settingsModal').style.display = 'none';
    }

    saveSettings() {
        const units = document.getElementById('unitsSelect').value;
        const updateInterval = document.getElementById('updateInterval').value;
        const theme = document.getElementById('themeSelect').value;

        localStorage.setItem('auroraSettings', JSON.stringify({
            units,
            updateInterval,
            theme
        }));

        this.applySettings();
        this.hideSettings();
    }

    applySettings() {
        const settings = JSON.parse(localStorage.getItem('auroraSettings') || '{}');
        
        if (settings.theme === 'light') {
            document.body.classList.add('light-theme');
        } else {
            document.body.classList.remove('light-theme');
        }

        if (settings.updateInterval) {
            this.refreshInterval = parseInt(settings.updateInterval) * 60 * 1000;
            this.stopAutoRefresh();
            this.startAutoRefresh();
        }
    }

    startAutoRefresh() {
        this.autoRefreshTimer = setInterval(() => {
            this.loadRealTimeData();
        }, this.refreshInterval);
    }

    stopAutoRefresh() {
        if (this.autoRefreshTimer) {
            clearInterval(this.autoRefreshTimer);
        }
    }
}

// Initialize the real-time dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new RealTimeAuroraDashboard();
});

// Add keyboard shortcuts for real-time features
document.addEventListener('keydown', (e) => {
    // Press 'R' to refresh real-time data
    if (e.key === 'r' || e.key === 'R') {
        const dashboard = new RealTimeAuroraDashboard();
        dashboard.loadRealTimeData();
    }
    
    // Press 'A' for aurora animation (enhanced)
    if (e.key === 'a' || e.key === 'A') {
        const waves = document.querySelectorAll('.aurora-wave');
        waves.forEach(wave => {
            wave.style.animationDuration = '2s';
            wave.style.opacity = '0.8';
            setTimeout(() => {
                wave.style.animationDuration = '6s';
                wave.style.opacity = '0.3';
            }, 5000);
        });
    }
});