# Climate Anomaly Detector

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://climate-anomaly-detection-nikitak.streamlit.app/)

**Live App:** [climate-anomaly-detection-nikitak.streamlit.app](https://climate-anomaly-detection-nikitak.streamlit.app/)

A dashboard that compares current weather conditions against 10 years of historical data to detect climate anomalies using statistical analysis.

## What It Does

Regular weather apps tell you it's 25°C, but they don't tell you if that's normal for this time of year. This tool uses Z-score statistics to determine if current conditions are unusual compared to historical patterns.

The key difference: instead of comparing against the whole year's average, it filters historical data to match the current month and hour. So a 30°C day in January gets compared to other January days, not July days.

## How It Works

1. Fetches current weather data from Open-Meteo API
2. Retrieves 10 years of historical climate data (ERA5 reanalysis)
3. Filters historical data to match current month and hour
4. Calculates Z-score: `(current - mean) / standard_deviation`
5. Classifies anomalies: Normal (|Z| < 2), Moderate (2 ≤ |Z| < 4), Extreme (|Z| ≥ 4)

## Tech Stack

- Python 3.8+
- Streamlit for the web interface
- Pandas for data processing
- Plotly for visualizations
- Open-Meteo API (free, no API keys needed)
- Pytest for testing

## Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/climate_anomaly_detection.git
cd climate_anomaly_detection

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Project Structure

```
climate_anomaly_detection/
├── app.py                 # Streamlit UI
├── src/
│   ├── api_client.py      # Open-Meteo API calls
│   └── analysis.py        # Z-score calculations
├── tests/
│   └── test_analysis.py   # Unit tests
└── requirements.txt
```

## Testing

```bash
pytest tests/test_analysis.py -v
```

## Features

- Real-time weather data fetching
- 10-year historical baseline
- Seasonal filtering (month + hour)
- Z-score anomaly detection
- Interactive visualizations
- Multiple metrics: temperature, humidity, precipitation, wind speed

## API Caching

The app caches API responses to reduce load:
- Current weather: 1 hour cache
- Historical data: 24 hour cache

## Configuration

- **Years of history**: Change `years_back` in `fetch_historical_climate()` (default: 10)
- **Anomaly threshold**: Adjust `threshold` in `detect_anomaly()` (default: 2.0)

## Deployment

Deployed on Streamlit Cloud. To deploy your own:

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repository and set main file to `app.py`
5. Deploy

## License

MIT License
