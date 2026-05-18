import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    weather_data = {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "visibility": data.get("visibility", 0) / 1000
    }

    return weather_data


def generate_alerts(weather):

    alerts = []

    if weather["temperature"] > 35:
        alerts.append("🔥 High Temperature Alert")

    if weather["humidity"] > 80:
        alerts.append("💧 High Humidity Alert")

    if weather["wind_speed"] > 10:
        alerts.append("💨 High Wind Speed Alert")

    if "rain" in weather["weather"].lower():
        alerts.append("🌧 Rain Alert")

    return alerts

def get_forecast(city):

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(forecast_url)

    return response.json()

def get_aqi(lat,lon):

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    response = requests.get(url)

    return response.json()

def get_7_day_forecast(city):

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(forecast_url)

    if response.status_code != 200:
        return None

    data = response.json()

    forecast_data = []

    for item in data["list"][:7]:

        forecast_data.append({
            "Datetime": item["dt_txt"],
            "Temperature": item["main"]["temp"],
            "Humidity": item["main"]["humidity"],
            "Weather": item["weather"][0]["description"]
        })

    return forecast_data

def get_aqi(city):

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    response = requests.get(weather_url)

    data = response.json()

    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    aqi_response = requests.get(aqi_url)

    aqi_data = aqi_response.json()

    return aqi_data["list"][0]["main"]["aqi"]