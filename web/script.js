// Aurora Borealis Dashboard JavaScript

class AuroraDashboard {
    constructor() {
        this.locations = {
            "Fairbanks, Alaska": { lat: 64.8, lon: -147.7, magnetic_lat: 65.1 },
            "Yellowknife, Canada": { lat: 62.5, lon: -114.3, magnetic_lat: 68.6 },
            "Reykjavik, Iceland": { lat: 64.1, lon: -21.9, magnetic_lat: 64.8 },
            "Tromsø, Norway": { lat: 69.6, lon: 18.9, magnetic_lat: 66.7 },
            "Anchorage, Alaska": { lat: 61.2, lon: -149.9, magnetic_lat: 61.8 },
            "Calgary, Canada": { lat: 51.0, lon: -114.1, magnetic_lat: 58.2 },
            "Seattle, Washington": { lat: 47.6, lon: -122.3, magnetic_lat: 54.2 },
            "Minneapolis, Minnesota": { lat: 44.98, lon: -93.3, magnetic_lat: 54.8 }
        };

        this.auroraFacts = [
            "The aurora borealis is caused by charged particles from the sun colliding with Earth's magnetic field.",
            "The best time to see the Northern Lights is during the winter months in the Northern Hemisphere.",
            "Aurora can appear in various colors including green, pink, red, yellow, and blue.",
            "Green is the most common color, produced by oxygen atoms about 60 miles above Earth.",
            "The aurora follows an oval-shaped zone around the magnetic poles called the auroral oval.",
            "The phenomenon was named after Aurora, the Roman goddess of dawn.",
            "Solar wind speed can reach up to 900 km/s during geomagnetic storms.",
            "The aurora can extend from 80 to 640 kilometers above Earth's surface.",
            "Indigenous peoples have many legends about the aurora, often seeing them as spirits dancing.",
            "The aurora australis is the Southern Hemisphere equivalent of the aurora borealis."
        ];

        this.auroraColors = {
            "Green": { altitude: "80-150 km", cause: "Oxygen atoms", frequency: 60, color: "#00ff88" },
            "Red": { altitude: "150-300 km", cause: "High altitude oxygen", frequency: 15, color: "#ff0088" },
            "Blue": { altitude: "80-120 km", cause: "Nitrogen molecules", frequency: 10, color: "#0088ff" },
            "Pink": { altitude: "80-150 km", cause: "Nitrogen + oxygen mix", frequency: 10, color: "#ff0088" },
            "Purple": { altitude: "80-120 km", cause: "Nitrogen at lower altitudes", frequency: 5, color: "#8800ff" }
        };

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.startAutoRefresh();
    }

    setupEventListeners() {
        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshData();
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

    loadInitialData() {
        this.refreshData();
    }

    refreshData() {
        // Add loading state
        document.body.classList.add('loading');
        
        // Simulate API call delay
        setTimeout(() => {
            this.updateCurrentConditions();
            this.updateForecast();
            this.updateProbabilities();
            this.updateColors();
            this.updateFact();
            this.updatePhotographyTips();
            
            document.body.classList.remove('loading');
        }, 1000);
    }

    updateCurrentConditions() {
        const currentKp = this.generateKpIndex();
        const activityLevel = this.getActivityLevel(currentKp);
        const visibilityZone = this.getVisibilityZone(currentKp);
        const lastUpdated = new Date().toLocaleString();

        document.getElementById('currentKp').textContent = currentKp.toFixed(1);
        document.getElementById('activityLevel').textContent = activityLevel;
        document.getElementById('visibilityZone').textContent = visibilityZone;
        document.getElementById('lastUpdated').textContent = `Last updated: ${lastUpdated}`;

        // Update activity level styling
        const activityElement = document.getElementById('activityLevel');
        activityElement.className = `activity-level activity-${activityLevel.toLowerCase().replace(' ', '-')}`;
    }

    updateForecast() {
        const forecastList = document.getElementById('forecastList');
        forecastList.innerHTML = '';

        const forecast = this.generateForecast(7);
        
        forecast.forEach(day => {
            const forecastItem = document.createElement('div');
            forecastItem.className = 'forecast-item';
            
            forecastItem.innerHTML = `
                <div class="forecast-date">${day.date}</div>
                <div class="forecast-kp">KP ${day.kp_index}</div>
                <div class="forecast-activity">${day.activity_level}</div>
            `;
            
            forecastList.appendChild(forecastItem);
        });
    }

    updateProbabilities() {
        const locationList = document.getElementById('locationList');
        locationList.innerHTML = '';

        const currentKp = this.generateKpIndex();

        Object.entries(this.locations).forEach(([location, data]) => {
            const probability = this.calculateViewingProbability(location, currentKp);
            
            const locationItem = document.createElement('div');
            locationItem.className = 'location-item';
            
            locationItem.innerHTML = `
                <div class="location-name">${location}</div>
                <div class="location-probability">${probability.toFixed(0)}%</div>
            `;
            
            locationList.appendChild(locationItem);
        });
    }

    updateColors() {
        const colorList = document.getElementById('colorList');
        colorList.innerHTML = '';

        const currentKp = this.generateKpIndex();
        const predictedColors = this.predictColors(currentKp);

        predictedColors.forEach(colorName => {
            const colorInfo = this.auroraColors[colorName];
            
            const colorItem = document.createElement('div');
            colorItem.className = 'color-item';
            
            colorItem.innerHTML = `
                <div class="color-swatch color-${colorName.toLowerCase()}" style="background-color: ${colorInfo.color}"></div>
                <div class="color-info">
                    <div class="color-name">${colorName}</div>
                    <div class="color-details">${colorInfo.altitude} - ${colorInfo.cause}</div>
                </div>
            `;
            
            colorList.appendChild(colorItem);
        });
    }

    updateFact() {
        const factContent = document.getElementById('factContent');
        const randomFact = this.auroraFacts[Math.floor(Math.random() * this.auroraFacts.length)];
        
        factContent.textContent = randomFact;
    }

    updatePhotographyTips() {
        const currentKp = this.generateKpIndex();
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

        baseTips.forEach(tip => {
            const tipElement = document.createElement('div');
            tipElement.className = 'tip';
            tipElement.textContent = tip;
            tipsList.appendChild(tipElement);
        });
    }

    generateKpIndex() {
        // Generate realistic KP index between 0 and 9
        const baseKp = Math.random() * 6 + 1; // 1-7 range
        const variation = (Math.random() - 0.5) * 2; // -1 to 1
        return Math.max(0, Math.min(9, baseKp + variation));
    }

    getActivityLevel(kp) {
        if (kp < 2) return "Quiet";
        if (kp < 3) return "Unsettled";
        if (kp < 4) return "Active";
        if (kp < 5) return "Minor Storm";
        if (kp < 6) return "Moderate Storm";
        if (kp < 7) return "Strong Storm";
        if (kp < 8) return "Severe Storm";
        return "Extreme Storm";
    }

    getVisibilityZone(kp) {
        if (kp < 2) return "Arctic Circle only";
        if (kp < 3) return "Northern Canada, Alaska";
        if (kp < 4) return "Northern border states";
        if (kp < 5) return "Northern US, southern Canada";
        if (kp < 6) return "Most of northern US";
        if (kp < 7) return "Central US states";
        if (kp < 8) return "Southern US possible";
        return "Visible to southern latitudes";
    }

    generateForecast(days) {
        const forecast = [];
        let currentKp = this.generateKpIndex();
        
        for (let i = 0; i < days; i++) {
            const dailyChange = (Math.random() - 0.5) * 3;
            currentKp = Math.max(0, Math.min(9, currentKp + dailyChange));
            
            const date = new Date();
            date.setDate(date.getDate() + i);
            
            forecast.push({
                date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                kp_index: currentKp.toFixed(1),
                activity_level: this.getActivityLevel(currentKp)
            });
        }
        
        return forecast;
    }

    calculateViewingProbability(location, kpIndex) {
        const locationData = this.locations[location];
        if (!locationData) return 0;
        
        const magneticLat = locationData.magnetic_lat;
        const thresholdLat = 67 - (kpIndex * 2.5);
        
        if (magneticLat >= thresholdLat) {
            return Math.min(95, (magneticLat - thresholdLat + 5) * 10);
        } else {
            return Math.max(0, (magneticLat - thresholdLat + 10) * 2);
        }
    }

    predictColors(kpIndex) {
        const predictedColors = [];
        
        // Green is almost always present
        if (kpIndex >= 1) {
            predictedColors.push("Green");
        }
        
        // Red appears with higher activity
        if (kpIndex >= 4) {
            predictedColors.push("Red");
        }
        
        // Blue and pink with moderate activity
        if (kpIndex >= 3) {
            if (Math.random() < 0.6) {
                predictedColors.push("Pink");
            }
            if (Math.random() < 0.4) {
                predictedColors.push("Blue");
            }
        }
        
        // Purple is rare but possible in strong storms
        if (kpIndex >= 6 && Math.random() < 0.3) {
            predictedColors.push("Purple");
        }
        
        return predictedColors.length > 0 ? predictedColors : ["Green"];
    }

    exportReport() {
        const reportData = {
            timestamp: new Date().toISOString(),
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
            }))
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

        // Save to localStorage
        localStorage.setItem('auroraSettings', JSON.stringify({
            units,
            updateInterval,
            theme
        }));

        // Apply settings
        this.applySettings();
        this.hideSettings();
    }

    applySettings() {
        const settings = JSON.parse(localStorage.getItem('auroraSettings') || '{}');
        
        // Apply theme
        if (settings.theme === 'light') {
            document.body.classList.add('light-theme');
        } else {
            document.body.classList.remove('light-theme');
        }

        // Update refresh interval
        if (settings.updateInterval) {
            this.stopAutoRefresh();
            this.startAutoRefresh(parseInt(settings.updateInterval) * 60 * 1000);
        }
    }

    startAutoRefresh(interval = 15 * 60 * 1000) { // Default 15 minutes
        this.autoRefreshInterval = setInterval(() => {
            this.refreshData();
        }, interval);
    }

    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new AuroraDashboard();
});

// Add some fun easter eggs
document.addEventListener('keydown', (e) => {
    // Press 'A' for aurora animation
    if (e.key === 'a' || e.key === 'A') {
        const waves = document.querySelectorAll('.aurora-wave');
        waves.forEach(wave => {
            wave.style.animationDuration = '2s';
            setTimeout(() => {
                wave.style.animationDuration = '6s';
            }, 3000);
        });
    }
});

// Add hover effects for cards
document.addEventListener('mouseover', (e) => {
    if (e.target.classList.contains('card')) {
        e.target.style.transform = 'translateY(-4px) scale(1.02)';
    }
});

document.addEventListener('mouseout', (e) => {
    if (e.target.classList.contains('card')) {
        e.target.style.transform = 'translateY(0) scale(1)';
    }
});