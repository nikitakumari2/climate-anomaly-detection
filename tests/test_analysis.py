"""
Unit Tests for Climate Anomaly Detection
Tests the Z-score calculation and anomaly detection logic
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.analysis import calculate_z_score, detect_anomaly, analyze_climate_anomalies


def test_calculate_z_score_basic():
    """Test basic Z-score calculation"""
    # Create simple historical data
    dates = pd.date_range(start="2020-01-01", periods=100, freq="H")
    values = np.random.normal(20, 5, 100)  # Mean=20, Std=5
    historical = pd.Series(values, index=dates)
    
    current_value = 30.0
    current_time = datetime(2024, 1, 1, 12, 0)
    
    z_score, mean, std_dev = calculate_z_score(current_value, historical, current_time)
    
    # Z-score should be approximately (30-20)/5 = 2.0
    assert abs(z_score - 2.0) < 1.0  # Allow some variance due to random data
    assert abs(mean - 20.0) < 2.0
    assert abs(std_dev - 5.0) < 2.0


def test_calculate_z_score_seasonal_filtering():
    """Test that seasonal filtering works correctly"""
    # Create data with clear monthly pattern
    dates = pd.date_range(start="2020-01-01", periods=365 * 2, freq="H")
    
    # January values: mean=10, July values: mean=30
    values = []
    for date in dates:
        if date.month == 1:
            values.append(np.random.normal(10, 2))
        elif date.month == 7:
            values.append(np.random.normal(30, 2))
        else:
            values.append(np.random.normal(20, 2))
    
    historical = pd.Series(values, index=dates)
    
    # Test January (should use January data)
    jan_time = datetime(2024, 1, 15, 12, 0)
    z_score_jan, mean_jan, _ = calculate_z_score(15.0, historical, jan_time)
    
    # Test July (should use July data)
    jul_time = datetime(2024, 7, 15, 12, 0)
    z_score_jul, mean_jul, _ = calculate_z_score(35.0, historical, jul_time)
    
    # January mean should be closer to 10, July mean closer to 30
    assert mean_jan < mean_jul
    assert abs(mean_jan - 10.0) < 3.0
    assert abs(mean_jul - 30.0) < 3.0


def test_calculate_z_score_empty_data():
    """Test handling of empty historical data"""
    empty_series = pd.Series([], dtype=float)
    current_time = datetime(2024, 1, 1, 12, 0)
    
    z_score, mean, std_dev = calculate_z_score(20.0, empty_series, current_time)
    
    assert z_score == 0.0
    assert mean == 0.0
    assert std_dev == 0.0


def test_calculate_z_score_zero_std_dev():
    """Test handling of zero standard deviation"""
    dates = pd.date_range(start="2020-01-01", periods=10, freq="H")
    values = [20.0] * 10  # All same value
    historical = pd.Series(values, index=dates)
    
    current_time = datetime(2024, 1, 1, 12, 0)
    z_score, mean, std_dev = calculate_z_score(25.0, historical, current_time)
    
    assert z_score == 0.0  # Should return 0 when std_dev is 0
    assert mean == 20.0
    assert std_dev == 0.0


def test_detect_anomaly_extreme():
    """Test detection of extreme anomalies"""
    is_anomaly, severity = detect_anomaly(4.5, threshold=2.0)
    assert is_anomaly is True
    assert severity == "Extreme"
    
    is_anomaly, severity = detect_anomaly(-4.5, threshold=2.0)
    assert is_anomaly is True
    assert severity == "Extreme"


def test_detect_anomaly_moderate():
    """Test detection of moderate anomalies"""
    is_anomaly, severity = detect_anomaly(2.5, threshold=2.0)
    assert is_anomaly is True
    assert severity == "Moderate"
    
    is_anomaly, severity = detect_anomaly(-2.5, threshold=2.0)
    assert is_anomaly is True
    assert severity == "Moderate"


def test_detect_anomaly_normal():
    """Test detection of normal values"""
    is_anomaly, severity = detect_anomaly(1.5, threshold=2.0)
    assert is_anomaly is False
    assert severity == "Normal"
    
    is_anomaly, severity = detect_anomaly(0.5, threshold=2.0)
    assert is_anomaly is False
    assert severity == "Normal"


def test_analyze_climate_anomalies():
    """Test full analysis pipeline"""
    # Create mock current weather
    current_weather = {
        "temperature": 25.0,
        "humidity": 60.0,
        "precipitation": 5.0,
        "wind_speed": 15.0,
    }
    
    # Create mock historical data
    dates = pd.date_range(start="2020-01-01", periods=1000, freq="H")
    historical_data = pd.DataFrame(
        {
            "temperature_2m": np.random.normal(20, 5, 1000),
            "relative_humidity_2m": np.random.normal(50, 10, 1000),
            "precipitation": np.random.exponential(2, 1000),
            "wind_speed_10m": np.random.normal(10, 3, 1000),
        },
        index=dates,
    )
    
    results = analyze_climate_anomalies(current_weather, historical_data)
    
    # Check that all metrics are analyzed
    assert "temperature" in results
    assert "humidity" in results
    assert "precipitation" in results
    assert "wind_speed" in results
    
    # Check structure of results
    for metric, data in results.items():
        assert "current" in data
        assert "mean" in data
        assert "std_dev" in data
        assert "z_score" in data
        assert "is_anomaly" in data
        assert "severity" in data


def test_analyze_climate_anomalies_empty_data():
    """Test analysis with empty historical data"""
    current_weather = {"temperature": 25.0}
    empty_data = pd.DataFrame()
    
    results = analyze_climate_anomalies(current_weather, empty_data)
    
    assert results == {}


def test_analyze_climate_anomalies_missing_columns():
    """Test analysis with missing columns in historical data"""
    current_weather = {"temperature": 25.0}
    dates = pd.date_range(start="2020-01-01", periods=100, freq="H")
    historical_data = pd.DataFrame(
        {"other_column": np.random.normal(20, 5, 100)}, index=dates
    )
    
    results = analyze_climate_anomalies(current_weather, historical_data)
    
    # Should not crash, but temperature won't be in results
    assert "temperature" not in results
