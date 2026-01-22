"""
Z-score based anomaly detection for climate data.
Filters historical data by month/hour to account for seasonality.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
from datetime import datetime


def calculate_z_score(
    current_value: float,
    historical_data: pd.Series,
    current_datetime: datetime,
) -> Tuple[float, float, float]:
    """
    Calculates Z-score for anomaly detection.
    
    Filters historical data to match current month and hour to handle
    seasonal patterns (e.g., comparing January temps to January, not July).
    """
    if historical_data.empty:
        return 0.0, 0.0, 0.0
    
    month = current_datetime.month
    hour = current_datetime.hour
    
    # Filter to same month and hour
    seasonal_filter = (historical_data.index.month == month) & (
        historical_data.index.hour == hour
    )
    seasonal_data = historical_data[seasonal_filter]
    
    # Fallback to same month only if no exact match
    if seasonal_data.empty:
        seasonal_filter = historical_data.index.month == month
        seasonal_data = historical_data[seasonal_filter]
    
    # Last resort: use all data
    if seasonal_data.empty:
        seasonal_data = historical_data
    
    seasonal_data = seasonal_data.dropna()
    
    if len(seasonal_data) == 0:
        return 0.0, 0.0, 0.0
    
    mean = float(seasonal_data.mean())
    std_dev = float(seasonal_data.std())
    
    if std_dev == 0:
        z_score = 0.0
    else:
        z_score = (current_value - mean) / std_dev
    
    return z_score, mean, std_dev


def detect_anomaly(z_score: float, threshold: float = 2.0) -> Tuple[bool, str]:
    """Classifies Z-score as normal or anomaly with severity level."""
    abs_z = abs(z_score)
    
    if abs_z >= threshold * 2:
        return True, "Extreme"
    elif abs_z >= threshold:
        return True, "Moderate"
    else:
        return False, "Normal"


def analyze_climate_anomalies(
    current_weather: Dict,
    historical_data: pd.DataFrame,
) -> Dict[str, Dict]:
    """Runs anomaly analysis for all climate metrics."""
    if historical_data is None or historical_data.empty:
        return {}
    
    current_time = datetime.now()
    results = {}
    
    metrics = {
        "temperature": "temperature_2m",
        "humidity": "relative_humidity_2m",
        "precipitation": "precipitation",
        "wind_speed": "wind_speed_10m",
    }
    
    for metric_name, column_name in metrics.items():
        if column_name not in historical_data.columns:
            continue
        
        current_value = current_weather.get(metric_name)
        if current_value is None:
            continue
        
        historical_series = historical_data[column_name]
        
        z_score, mean, std_dev = calculate_z_score(
            current_value, historical_series, current_time
        )
        
        is_anomaly, severity = detect_anomaly(z_score)
        
        results[metric_name] = {
            "current": current_value,
            "mean": mean,
            "std_dev": std_dev,
            "z_score": z_score,
            "is_anomaly": is_anomaly,
            "severity": severity,
        }
    
    return results
