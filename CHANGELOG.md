# Changelog

All notable changes to the Aurora Borealis Toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-18

### Added
- **Aurora Tracker System** (`aurora_tracker.py`)
  - KP index forecasting with 7-day predictions
  - Viewing probability calculations for 8 major northern cities
  - Photography tips based on current activity levels
  - Aurora color predictions using scientific models
  - Comprehensive reporting with educational facts

- **ASCII Art Generator** (`aurora_art.py`)
  - Colorful terminal-based aurora visualizations
  - Northern sky constellation maps
  - Aurora phase demonstrations (Quiet, Active, Substorm, Recovery)
  - Automated aurora poetry generation
  - Full-color terminal graphics support

- **Data Visualization Tools** (`aurora_graph.py`)
  - Historical KP index trend analysis (14-day periods)
  - ASCII-based bar charts and line graphs
  - Statistical summaries and activity pattern analysis
  - Color-coded activity levels for easy interpretation
  - Storm frequency and viewing opportunity calculations

- **Basic Information System** (`aurora_info.py`)
  - Quick aurora status reports
  - Random KP index generation with classifications
  - Essential viewing tips and camera settings
  - Educational facts about aurora phenomena

- **Project Infrastructure**
  - Comprehensive README with installation and usage instructions
  - Professional project structure with organized directories
  - Setup script for easy installation
  - Requirements management and dependency tracking
  - Git repository initialization with proper commit history

### Features
- **8 Supported Locations** with accurate magnetic latitude coordinates
- **Scientific Accuracy** based on real geomagnetic principles
- **Educational Content** including aurora facts and viewing tips
- **Cross-platform Compatibility** works on Linux, macOS, and Windows
- **No External Dependencies** for core functionality
- **Beautiful Terminal Output** with full color support
- **Professional Documentation** with contributing guidelines

### Technical Details
- **Python 3.7+** compatibility
- **Modular Design** with separate modules for each functionality
- **Type Hints** and comprehensive docstrings
- **Error Handling** for robust operation
- **Configurable Parameters** for customization
- **Extensible Architecture** for future enhancements

### Supported Locations
- Fairbanks, Alaska (65.1° magnetic latitude)
- Yellowknife, Canada (68.6° magnetic latitude)
- Reykjavik, Iceland (64.8° magnetic latitude)
- Tromsø, Norway (66.7° magnetic latitude)
- Anchorage, Alaska (61.8° magnetic latitude)
- Calgary, Canada (58.2° magnetic latitude)
- Seattle, Washington (54.2° magnetic latitude)
- Minneapolis, Minnesota (54.8° magnetic latitude)

### Color Schemes
- **Activity Levels**: Green (Quiet), Yellow (Active), Red (Storm), Purple (Severe)
- **Aurora Colors**: Green (most common), Red (high altitude), Blue (nitrogen), Pink (mixed), Purple (rare)
- **Terminal Output**: Full ANSI color support with fallback for basic terminals

## [Unreleased]

### Planned Features
- Real-time data integration with NOAA Space Weather APIs
- Interactive web interface for mobile devices
- Historical data analysis with machine learning predictions
- Push notifications for high activity periods
- Integration with weather data for cloud coverage analysis
- Social sharing features for aurora photography
- Enhanced location support with international cities
- Advanced statistical analysis and trend prediction
- Multi-language support and internationalization

---

**Legend:**
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes