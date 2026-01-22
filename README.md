# 🌡️ Climate Anomaly Detector

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

> **Live Demo:** [Deploy on Streamlit Cloud](https://share.streamlit.io)

A statistical dashboard that detects climate anomalies by comparing current weather conditions against 10 years of historical ERA5 reanalysis data. Unlike standard weather apps that only show current conditions, this tool provides climate context through Z-score statistical analysis.

---

## 🎯 The Problem

Standard weather applications display current conditions but lack **climate context**. Is 25°C in January normal? Is today's rainfall unusual? Without historical comparison, users can't determine if current conditions are statistically significant anomalies.

## 💡 The Solution

This dashboard uses:
- **Z-Score Statistics** to quantify how unusual current conditions are
- **Seasonal Decomposition** to filter historical data by month and hour (accounting for seasonal patterns)
- **ERA5 Reanalysis Data** from Open-Meteo API (10-year historical baseline)
- **Real-time Anomaly Detection** with severity classification (Normal, Moderate, Extreme)

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** - Interactive web dashboard
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **Open-Meteo API** - Weather and climate data (100% FREE - no API keys, no cost)
- **Pytest** - Unit testing

> **💰 Cost:** This project uses Open-Meteo's completely free tier. No API keys required, no credit card needed, no hidden costs. Perfect for portfolio projects!

---

## 📊 Data Methodology

### Statistical Approach

1. **Data Collection**: Fetch 10 years of hourly historical climate data using ERA5 reanalysis
2. **Seasonal Filtering**: Filter historical data to match the current month and hour
   - Example: For January 15th at 2 PM, compare against all January 15th 2 PM values from the past 10 years
   - This accounts for seasonal patterns (winter vs summer, day vs night)
3. **Z-Score Calculation**: 
   ```
   Z = (Current Value - Historical Mean) / Standard Deviation
   ```
4. **Anomaly Classification**:
   - **Normal**: |Z| < 2.0
   - **Moderate Anomaly**: 2.0 ≤ |Z| < 4.0
   - **Extreme Anomaly**: |Z| ≥ 4.0

### Why Seasonal Decomposition Matters

Simply averaging all historical data would be misleading. A temperature of 30°C in July might be normal, but the same temperature in January would be an extreme anomaly. By filtering to the same month and hour, we ensure accurate statistical comparisons.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/climate_anomaly_detection.git
   cd climate_anomaly_detection
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

---

## 📁 Project Structure

```
climate_anomaly_detection/
├── app.py                 # Streamlit frontend (thin controller)
├── src/
│   ├── __init__.py
│   ├── api_client.py      # Data ingestion from Open-Meteo API
│   └── analysis.py        # Z-score calculation and anomaly detection
├── tests/
│   └── test_analysis.py   # Unit tests for statistical functions
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🧪 Testing

Run unit tests to verify the statistical calculations:

```bash
pytest tests/test_analysis.py -v
```

The test suite covers:
- Basic Z-score calculations
- Seasonal filtering logic
- Edge cases (empty data, zero standard deviation)
- Anomaly detection thresholds
- Full analysis pipeline

---

## 📈 Features

### Current Implementation

- ✅ Real-time weather data fetching
- ✅ 10-year historical climate baseline
- ✅ Z-score anomaly detection
- ✅ Seasonal decomposition (month + hour filtering)
- ✅ Interactive visualizations (histograms, metrics)
- ✅ Multi-metric analysis (temperature, humidity, precipitation, wind speed)
- ✅ Error handling and user feedback
- ✅ API response caching (performance optimization)

### Metrics Analyzed

1. **Temperature** (°C) - Air temperature at 2 meters
2. **Humidity** (%) - Relative humidity at 2 meters
3. **Precipitation** (mm) - Hourly precipitation
4. **Wind Speed** (km/h) - Wind speed at 10 meters

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and branch
   - Set main file to `app.py`
   - Click "Deploy"

3. **Update README**
   - Replace the Streamlit badge URL with your deployed app URL
   - Add the live link to your resume/portfolio

---

## 🔧 Configuration

### API Rate Limiting

The app uses `@st.cache_data` decorators to cache API responses:
- Current weather: 1 hour cache (TTL=3600)
- Historical data: 24 hour cache (TTL=86400)

This respects API rate limits and improves performance.

### Customization

- **Years of History**: Modify `years_back` parameter in `fetch_historical_climate()` (default: 10)
- **Anomaly Threshold**: Adjust `threshold` in `detect_anomaly()` (default: 2.0)
- **Metrics**: Add new metrics by extending the `metrics` dictionary in `analyze_climate_anomalies()`

---

## 📝 Code Quality

This project follows best practices:

- ✅ **Type Hints**: All functions include Python type annotations
- ✅ **Error Handling**: Try/except blocks for API failures and edge cases
- ✅ **Modular Design**: Separation of concerns (API, analysis, UI)
- ✅ **Unit Tests**: Comprehensive test coverage for statistical functions
- ✅ **Documentation**: Inline comments and docstrings
- ✅ **Performance**: API response caching to reduce load

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **Open-Meteo** for providing free weather and climate APIs
- **ERA5** reanalysis data from Copernicus Climate Change Service
- **Streamlit** for the amazing framework

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for climate awareness**
