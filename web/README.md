# 🌐 Aurora Borealis Web Dashboard

A beautiful, interactive web interface for real-time aurora tracking and forecasting.

## 🚀 Quick Start

1. **Start the local server:**
   ```bash
   # From the project root directory
   cd web
   python3 -m http.server 8000
   ```

2. **Open your browser:**
   ```
   http://localhost:8000
   ```

3. **Enjoy the aurora dashboard!**

## ✨ Features

### 🔮 Real-time Aurora Tracking
- **Live KP Index Display**: Large, glowing display of current geomagnetic activity
- **Activity Level Classification**: Automatic categorization from Quiet to Extreme Storm
- **Visibility Zone Mapping**: Shows how far south aurora might be visible
- **Timestamp Tracking**: Last updated information for data freshness

### 📊 Interactive 7-Day Forecast
- **Color-coded Activity Levels**: Visual indicators for each day's predicted activity
- **Dynamic Data Generation**: Realistic KP index forecasting with natural variations
- **Storm Predictions**: Highlights moderate to severe geomagnetic storms
- **Trend Analysis**: Easy-to-read forecast progression

### 📍 Viewing Probabilities
- **8 Major Northern Locations**: From Fairbanks to Minneapolis
- **Percentage Calculations**: Based on magnetic latitude and current KP index
- **Color-coded Badges**: Green for high probability, gradient for lower chances
- **Geographic Coverage**: Spanning Alaska, Canada, Iceland, and northern US

### 🎨 Aurora Color Predictions
- **Scientific Accuracy**: Based on altitude ranges and atmospheric composition
- **Visual Color Swatches**: Actual aurora colors with explanations
- **Dynamic Prediction**: Colors change based on current activity levels
- **Educational Content**: Altitude ranges and scientific causes

### 📸 Adaptive Photography Tips
- **Activity-based Advice**: Tips expand for higher KP indices
- **Camera Settings**: Specific ISO, aperture, and exposure recommendations
- **Practical Guidance**: Battery tips, focus advice, and timing recommendations
- **Professional Techniques**: Time-lapse and composition suggestions

### 🛠️ Interactive Controls
- **Refresh Data**: Generate new realistic aurora forecasts
- **Export Report**: Download current data as JSON for analysis
- **Settings Panel**: Customize units, themes, and refresh intervals
- **Auto-refresh**: Configurable automatic data updates

## 🎨 Design Features

### 🌌 Aurora-Themed Design
- **Dark Space Background**: Perfect for night-time aurora viewing
- **Aurora-Inspired Colors**: Green, blue, purple, and pink accents
- **Gradient Backgrounds**: Smooth transitions mimicking aurora displays
- **Professional Typography**: Clean, readable Inter font family

### 📱 Responsive Layout
- **Mobile-First Design**: Optimized for smartphones and tablets
- **CSS Grid & Flexbox**: Modern layout techniques for all screen sizes
- **Hover Effects**: Smooth transitions and interactive feedback
- **Card-Based Layout**: Organized information in digestible sections

### ⚡ Performance Optimized
- **Zero Dependencies**: Pure HTML, CSS, and JavaScript
- **Lightweight**: Fast loading with minimal resource usage
- **Cross-browser**: Compatible with all modern browsers
- **Accessibility**: Semantic HTML and keyboard navigation support

## 🔧 Technical Implementation

### 📋 File Structure
```
web/
├── index.html          # Main HTML structure
├── style.css           # Aurora-themed CSS styles
├── script.js           # Interactive JavaScript functionality
└── README.md           # This documentation
```

### 🎯 Core JavaScript Classes
- **AuroraDashboard**: Main application controller
- **Data Generation**: Realistic KP index and probability calculations
- **UI Management**: Dynamic content updates and user interactions
- **Settings Handling**: Local storage and preference management

### 🎨 CSS Architecture
- **CSS Custom Properties**: Centralized color and spacing variables
- **Responsive Breakpoints**: Mobile (480px), tablet (768px), desktop (1024px+)
- **Animation System**: Smooth transitions and aurora wave effects
- **Grid Layouts**: Flexible, responsive card arrangements

### 🔬 Aurora Physics Simulation
- **Magnetic Latitude Calculations**: Accurate viewing probability formulas
- **KP Index Generation**: Realistic geomagnetic activity simulation
- **Color Prediction Logic**: Based on atmospheric science
- **Activity Level Mapping**: Standard geomagnetic classification system

## 🌟 Usage Examples

### 📊 Data Refresh
Click the "🔄 Refresh Data" button to generate new aurora forecasts with:
- Updated KP index values
- New viewing probabilities
- Fresh aurora color predictions
- Adaptive photography tips

### 📁 Export Functionality
Use "📊 Export Report" to download current data including:
- Complete forecast information
- All location probabilities
- Photography recommendations
- Timestamp and metadata

### ⚙️ Settings Customization
Access the settings panel to configure:
- **Units**: Metric or Imperial measurements
- **Theme**: Dark (Aurora Night) or Light (Arctic Day)
- **Refresh Interval**: Automatic update frequency

## 🎓 Educational Value

### 🔬 Scientific Accuracy
- **Real Physics**: Based on actual aurora formation principles
- **Magnetic Field Science**: Proper magnetic latitude calculations
- **Atmospheric Chemistry**: Accurate color formation explanations
- **Geomagnetic Indices**: Standard KP index classification system

### 📚 Learning Features
- **Aurora Facts**: Educational content about aurora phenomena
- **Photography Education**: Professional aurora photography techniques
- **Location Science**: Magnetic latitude vs. geographic latitude
- **Space Weather**: Understanding solar-terrestrial interactions

## 🤝 Contributing

This web dashboard is part of the larger Aurora Borealis Project. Contributions welcome for:
- **UI/UX Improvements**: Enhanced design and user experience
- **New Features**: Additional functionality and capabilities
- **Performance Optimization**: Faster loading and smoother interactions
- **Accessibility**: Better support for screen readers and keyboard navigation
- **Mobile Enhancement**: Improved mobile experience and touch interactions

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**Built with ❤️ for aurora enthusiasts worldwide! 🌌**

*Experience the magic of the Northern Lights from anywhere with real-time tracking and beautiful visualizations.*