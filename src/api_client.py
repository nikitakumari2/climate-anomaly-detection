"""
Fetches weather and climate data from Open-Meteo API.
All APIs are free - no keys needed.
"""

import pandas as pd
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

# Handle streamlit import for when running tests
try:
    import streamlit as st
except ImportError:
    class MockStreamlit:
        @staticmethod
        def error(msg):
            print(f"ERROR: {msg}")
        
        @staticmethod
        def cache_data(ttl=None):
            def decorator(func):
                return func
            return decorator
    
    st = MockStreamlit()


@st.cache_data(ttl=3600)
def fetch_current_weather(
    latitude: float, longitude: float
) -> Optional[Dict]:
    """Gets current weather for a location."""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            "timezone": "auto",
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "current" in data:
            return {
                "temperature": data["current"]["temperature_2m"],
                "humidity": data["current"]["relative_humidity_2m"],
                "precipitation": data["current"]["precipitation"],
                "wind_speed": data["current"]["wind_speed_10m"],
                "timestamp": data["current"]["time"],
            }
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching current weather: {str(e)}")
        return None
    except KeyError as e:
        st.error(f"Unexpected API response format: {str(e)}")
        return None


@st.cache_data(ttl=86400)
def fetch_historical_climate(
    latitude: float, longitude: float, years_back: int = 10
) -> Optional[pd.DataFrame]:
    """Fetches historical climate data from ERA5 reanalysis."""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * years_back)
        
        url = "https://archive-api.open-meteo.com/v1/era5"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            "timezone": "auto",
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "hourly" in data:
            df = pd.DataFrame(data["hourly"])
            df["time"] = pd.to_datetime(df["time"])
            df = df.set_index("time")
            return df
        
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching historical climate data: {str(e)}")
        return None
    except (KeyError, ValueError) as e:
        st.error(f"Error processing historical data: {str(e)}")
        return None


def get_coordinates(city_name: str) -> Optional[Tuple[float, float]]:
    """Converts city name to lat/lon coordinates."""
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return (result["latitude"], result["longitude"])
        
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error geocoding city '{city_name}': {str(e)}")
        return None
    except (KeyError, IndexError) as e:
        st.error(f"City '{city_name}' not found. Please check the spelling.")
        return None
