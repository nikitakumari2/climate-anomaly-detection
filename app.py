"""
Climate Anomaly Detector - Streamlit Frontend
A thin controller that orchestrates the UI and calls backend functions
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from src.api_client import (
    get_coordinates,
    fetch_current_weather,
    fetch_historical_climate,
)
from src.analysis import analyze_climate_anomalies

# Page configuration
st.set_page_config(
    page_title="Climate Anomaly Detector",
    page_icon="🌡️",
    layout="wide",
)

# Title and description
st.title("🌡️ Climate Anomaly Detector")
st.markdown(
    """
    **Statistical dashboard using ERA5 reanalysis data to detect climate anomalies.**
    
    Standard weather apps don't provide climate context. This tool compares current 
    conditions against 10 years of historical data to identify statistically significant anomalies.
    """
)

# Sidebar for user input
st.sidebar.header("📍 Location Settings")

city_name = st.sidebar.text_input(
    "Enter City Name",
    value="New York",
    help="Enter a city name (e.g., 'New York', 'London', 'Tokyo')",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 About")
st.sidebar.markdown(
    """
    This dashboard uses:
    - **Z-Score Statistics** for anomaly detection
    - **Seasonal Decomposition** to account for monthly/hourly patterns
    - **ERA5 Reanalysis Data** from Open-Meteo API
    - **10-Year Historical Baseline** for accurate comparisons
    """
)

# Main content area
if st.sidebar.button("🔍 Analyze Climate", type="primary") or city_name:
    with st.spinner("Fetching climate data..."):
        # Get coordinates
        coords = get_coordinates(city_name)
        
        if coords is None:
            st.error(f"❌ Could not find city '{city_name}'. Please check the spelling and try again.")
        else:
            latitude, longitude = coords
            
            # Fetch data
            current_weather = fetch_current_weather(latitude, longitude)
            historical_data = fetch_historical_climate(latitude, longitude, years_back=10)
            
            if current_weather is None:
                st.error("❌ Failed to fetch current weather data. Please try again later.")
            elif historical_data is None or historical_data.empty:
                st.error("❌ Failed to fetch historical climate data. Please try again later.")
            else:
                # Display location info
                st.success(f"✅ Analyzing climate for: **{city_name}** ({latitude:.2f}°, {longitude:.2f}°)")
                
                # Perform analysis
                anomalies = analyze_climate_anomalies(current_weather, historical_data)
                
                if not anomalies:
                    st.warning("⚠️ Could not perform analysis. Historical data may be incomplete.")
                else:
                    # Display metrics in columns
                    cols = st.columns(4)
                    
                    metric_names = {
                        "temperature": "🌡️ Temperature",
                        "humidity": "💧 Humidity",
                        "precipitation": "🌧️ Precipitation",
                        "wind_speed": "💨 Wind Speed",
                    }
                    
                    units = {
                        "temperature": "°C",
                        "humidity": "%",
                        "precipitation": "mm",
                        "wind_speed": "km/h",
                    }
                    
                    for idx, (metric_key, metric_display) in enumerate(metric_names.items()):
                        if metric_key in anomalies:
                            data = anomalies[metric_key]
                            with cols[idx]:
                                # Determine color based on anomaly status
                                if data["is_anomaly"]:
                                    if data["severity"] == "Extreme":
                                        delta_color = "inverse"
                                        delta_prefix = "⚠️ "
                                    else:
                                        delta_color = "off"
                                        delta_prefix = "📊 "
                                else:
                                    delta_color = "normal"
                                    delta_prefix = "✅ "
                                
                                # Calculate delta (difference from mean)
                                delta_value = data["current"] - data["mean"]
                                
                                st.metric(
                                    label=metric_display,
                                    value=f"{data['current']:.1f} {units[metric_key]}",
                                    delta=f"{delta_prefix}{delta_value:+.1f} {units[metric_key]}",
                                    delta_color=delta_color,
                                )
                                
                                # Show Z-score and severity
                                st.caption(
                                    f"Z-Score: {data['z_score']:.2f} | "
                                    f"Severity: {data['severity']}"
                                )
                    
                    # Detailed analysis section
                    st.markdown("---")
                    st.subheader("📈 Detailed Analysis")
                    
                    # Create tabs for each metric
                    tabs = st.tabs(list(metric_names.values()))
                    
                    for tab_idx, (metric_key, _) in enumerate(metric_names.items()):
                        if metric_key in anomalies:
                            with tabs[tab_idx]:
                                data = anomalies[metric_key]
                                
                                # Display statistics
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Current Value", f"{data['current']:.2f} {units[metric_key]}")
                                
                                with col2:
                                    st.metric("Historical Mean", f"{data['mean']:.2f} {units[metric_key]}")
                                
                                with col3:
                                    st.metric("Standard Deviation", f"{data['std_dev']:.2f} {units[metric_key]}")
                                
                                # Z-score interpretation
                                st.markdown("### 📊 Statistical Analysis")
                                
                                z_score = data["z_score"]
                                interpretation = ""
                                
                                if abs(z_score) >= 3:
                                    interpretation = "**Extreme Anomaly** - This value is extremely unusual (|Z| ≥ 3)"
                                elif abs(z_score) >= 2:
                                    interpretation = "**Moderate Anomaly** - This value is significantly different (|Z| ≥ 2)"
                                elif abs(z_score) >= 1:
                                    interpretation = "**Slight Deviation** - This value is somewhat unusual (|Z| ≥ 1)"
                                else:
                                    interpretation = "**Normal** - This value is within expected range (|Z| < 1)"
                                
                                st.info(interpretation)
                                
                                # Visualization
                                if not historical_data.empty and metric_key in ["temperature", "humidity"]:
                                    st.markdown("### 📉 Historical Distribution")
                                    
                                    # Get seasonal data for visualization
                                    current_time = datetime.now()
                                    month = current_time.month
                                    hour = current_time.hour
                                    
                                    column_name = {
                                        "temperature": "temperature_2m",
                                        "humidity": "relative_humidity_2m",
                                        "precipitation": "precipitation",
                                        "wind_speed": "wind_speed_10m",
                                    }[metric_key]
                                    
                                    if column_name in historical_data.columns:
                                        seasonal_filter = (
                                            (historical_data.index.month == month)
                                            & (historical_data.index.hour == hour)
                                        )
                                        seasonal_data = historical_data[seasonal_filter][column_name].dropna()
                                        
                                        if seasonal_data.empty:
                                            seasonal_data = historical_data[
                                                historical_data.index.month == month
                                            ][column_name].dropna()
                                        
                                        if not seasonal_data.empty:
                                            # Create histogram
                                            fig = go.Figure()
                                            
                                            fig.add_trace(
                                                go.Histogram(
                                                    x=seasonal_data,
                                                    nbinsx=30,
                                                    name="Historical Distribution",
                                                    marker_color="lightblue",
                                                )
                                            )
                                            
                                            # Add current value as vertical line
                                            fig.add_vline(
                                                x=data["current"],
                                                line_dash="dash",
                                                line_color="red",
                                                annotation_text=f"Current: {data['current']:.1f}",
                                                annotation_position="top",
                                            )
                                            
                                            # Add mean line
                                            fig.add_vline(
                                                x=data["mean"],
                                                line_dash="dot",
                                                line_color="green",
                                                annotation_text=f"Mean: {data['mean']:.1f}",
                                                annotation_position="top",
                                            )
                                            
                                            fig.update_layout(
                                                title=f"Historical Distribution for {metric_names[metric_key]} "
                                                f"(Month {month}, Hour {hour})",
                                                xaxis_title=f"{metric_names[metric_key]} ({units[metric_key]})",
                                                yaxis_title="Frequency",
                                                height=400,
                                            )
                                            
                                            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Built with Python, Streamlit, and Open-Meteo API | Data: ERA5 Reanalysis</p>
    </div>
    """,
    unsafe_allow_html=True,
)
