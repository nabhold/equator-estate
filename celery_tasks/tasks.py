import requests
from celery import shared_task
from weather.weather_client import get_weather
from weather.models import WeatherData


@shared_task
def fetch_weather_data():
    locations = {
        "Kampala": {"lat": 0.3476, "lon": 32.5825},
        "Entebbe": {"lat": 0.0502, "lon": 32.4603},
        "Gulu": {"lat": 2.7724, "lon": 32.2881},
        "Jinja": {"lat": 0.4243, "lon": 33.2042},
        "Mbarara": {"lat": -0.6583, "lon": 30.6758},
        "Mbale": {"lat": 1.0821, "lon": 34.1750},
        "Kasese": {"lat": 0.1833, "lon": 30.0786},
        "Masaka": {"lat": -0.3333, "lon": 31.7341},
        "Fort Portal": {"lat": 0.6646, "lon": 30.2806},
        "Arua": {"lat": 3.0344, "lon": 30.9110},
        "Butaleja": {"lat": 0.8438, "lon": 33.9498},
    }

    for city, coords in locations.items():
        data = get_weather(coords["lat"], coords["lon"])
        if "main" in data and "weather" in data:
            WeatherData.objects.create(
                location=city,
                temp=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                description=data["weather"][0]["description"],
            )
