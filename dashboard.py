import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# IMPORT FUNCTIONS
from main import (
    get_weather,
    generate_alerts,
    get_7_day_forecast,
    get_aqi
)

from ai.prediction import predict_temperature

from alerts.email_alert import send_email_alert
from alerts.telegram_alert import send_telegram_alert

from maps.live_map import generate_map

from streamlit_folium import st_folium

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Weather Dashboard",
    page_icon="🌦",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATE FIX
# ---------------------------------------------------

if "weather_loaded" not in st.session_state:
    st.session_state.weather_loaded = False

if "selected_city" not in st.session_state:
    st.session_state.selected_city = "Mumbai"

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #00BFFF;
}

.subtitle {
    text-align: center;
    color: #C0C0C0;
    font-size: 20px;
    margin-bottom: 30px;
}

.alert-box {
    background-color: #ff4b4b;
    padding: 15px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
}

.success-box {
    background-color: #16a34a;
    padding: 15px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    '<div class="title">🌍 AI Weather Forecast & Alert Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Industry-Level Weather Intelligence Platform using Python, AI, APIs & Visualization</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("⚙ Dashboard Controls")

cities = [
    "Mumbai",
    "Delhi",
    "Pune",
    "Nashik",
    "Bangalore",
    "Hyderabad",
    "Chennai"
]

selected_city = st.sidebar.selectbox(
    "🌍 Select City",
    cities
)

# ---------------------------------------------------
# BUTTON FIX
# ---------------------------------------------------

if st.sidebar.button("🚀 Check Weather"):

    st.session_state.weather_loaded = True
    st.session_state.selected_city = selected_city

# ---------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------

if st.session_state.weather_loaded:

    city = st.session_state.selected_city

    weather = get_weather(city)

    if weather is None:

        st.error("❌ Failed to Fetch Weather Data")

    else:

        alerts = generate_alerts(weather)

        # ---------------------------------------------------
        # TOP METRICS
        # ---------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🌡 Temperature",
            f"{weather['temperature']} °C"
        )

        col2.metric(
            "💧 Humidity",
            f"{weather['humidity']} %"
        )

        col3.metric(
            "💨 Wind Speed",
            f"{weather['wind_speed']} m/s"
        )

        col4.metric(
            "👁 Visibility",
            f"{weather['visibility']} km"
        )

        st.markdown("---")

        # ---------------------------------------------------
        # WEATHER SUMMARY
        # ---------------------------------------------------

        st.subheader("📋 Current Weather Summary")

        weather_df = pd.DataFrame({
            "Parameter": [
                "City",
                "Temperature",
                "Humidity",
                "Pressure",
                "Weather",
                "Wind Speed",
                "Visibility",
                "Checked At"
            ],

            "Value": [
                weather["city"],
                f"{weather['temperature']} °C",
                f"{weather['humidity']} %",
                f"{weather['pressure']} hPa",
                weather["weather"],
                f"{weather['wind_speed']} m/s",
                f"{weather['visibility']} km",
                datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            ]
        })

        st.dataframe(
            weather_df,
            use_container_width=True
        )

        st.markdown("---")

        # ---------------------------------------------------
        # AQI MONITORING
        # ---------------------------------------------------

        st.subheader("🌫 Air Quality Index (AQI)")

        try:

            aqi = get_aqi(city)

            if aqi == 1:
                st.success("AQI Status: Good ✅")

            elif aqi == 2:
                st.info("AQI Status: Fair ℹ")

            elif aqi == 3:
                st.warning("AQI Status: Moderate ⚠")

            else:
                st.error("AQI Status: Poor ❌")

        except:
            st.warning("AQI Data Not Available")

        st.markdown("---")

        # ---------------------------------------------------
        # ALERTS
        # ---------------------------------------------------

        st.subheader("🚨 Weather Alerts")

        if alerts:

            for alert in alerts:

                st.markdown(
                    f'<div class="alert-box">{alert}</div>',
                    unsafe_allow_html=True
                )

            alert_message = "\n".join(alerts)

            # EMAIL ALERT BUTTON

            if st.button("📧 Send Email Alert"):

                try:
                    send_email_alert(alert_message)
                    st.success("✅ Email Alert Sent Successfully")

                except Exception as e:
                    st.error(f"Email Error: {e}")

            # TELEGRAM ALERT BUTTON

            if st.button("📲 Send Telegram Alert"):

                try:
                    send_telegram_alert(alert_message)
                    st.success("✅ Telegram Alert Sent Successfully")

                except Exception as e:
                    st.error(f"Telegram Error: {e}")

        else:

            st.markdown(
                '<div class="success-box">✅ No Severe Weather Alerts</div>',
                unsafe_allow_html=True
            )

        st.markdown("---")

        # ---------------------------------------------------
        # AI PREDICTION
        # ---------------------------------------------------

        st.subheader("🤖 AI Temperature Prediction")

        try:

            predicted_temp = predict_temperature(
                weather["temperature"]
            )

            st.info(
                f"📈 Predicted Tomorrow Temperature: {predicted_temp} °C"
            )

        except:
            st.warning("AI Prediction Not Available")

        st.markdown("---")

        # ---------------------------------------------------
        # 7 DAY FORECAST
        # ---------------------------------------------------

        st.subheader("📅 7-Day Forecast")

        try:

            forecast_data = get_7_day_forecast(city)

            if forecast_data:

                forecast_df = pd.DataFrame(forecast_data)

                st.dataframe(
                    forecast_df,
                    use_container_width=True
                )

                forecast_chart = px.line(
                    forecast_df,
                    x="Datetime",
                    y="Temperature",
                    markers=True,
                    title="7-Day Temperature Forecast",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    forecast_chart,
                    use_container_width=True
                )

        except:
            st.warning("Forecast Data Not Available")

        st.markdown("---")

        # ---------------------------------------------------
        # ANALYTICS CHARTS
        # ---------------------------------------------------

        st.subheader("📊 Weather Analytics")

        chart_df = pd.DataFrame({
            "Parameter": [
                "Temperature",
                "Humidity",
                "Wind Speed",
                "Visibility"
            ],

            "Value": [
                weather["temperature"],
                weather["humidity"],
                weather["wind_speed"],
                weather["visibility"]
            ]
        })

        # BAR CHART

        fig = px.bar(
            chart_df,
            x="Parameter",
            y="Value",
            color="Parameter",
            text="Value",
            title="Weather Overview",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # PIE CHART

        pie_fig = px.pie(
            chart_df,
            names="Parameter",
            values="Value",
            title="Weather Distribution",
            template="plotly_dark"
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

        st.markdown("---")

        # ---------------------------------------------------
        # LIVE MAP
        # ---------------------------------------------------

        st.subheader("🗺 Live Weather Location Map")

        try:

            weather_map = generate_map(city)

            st_folium(
                weather_map,
                width=1200,
                height=500
            )

        except:
            st.warning("Map Not Available")

        st.markdown("---")

        # ---------------------------------------------------
        # DOWNLOAD REPORT
        # ---------------------------------------------------

        st.subheader("📥 Download Weather Report")

        csv = weather_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="⬇ Download CSV Report",
            data=csv,
            file_name=f"{city}_weather_report.csv",
            mime='text/csv'
        )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <center>
    <h4>🚀 Developed using Python, Streamlit, AI, APIs & Data Visualization</h4>
    <p>Advanced Industry-Level Weather Intelligence Dashboard</p>
    </center>
    """,
    unsafe_allow_html=True
)