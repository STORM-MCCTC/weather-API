# API Weather App - Created by Mark Donnadio

import requests as req
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="weather_app")

def get_lat_lon(city, state):
    location = geolocator.geocode(f"{city}, {state}")
    if location:
        return location.latitude, location.longitude
    else:
        return None

def test_get_lat_lon():
    city = input("City: ")
    state = input("State: ")
    lat_lon = get_lat_lon(city, state)

    if isinstance(lat_lon, tuple):
        print(f"The Latitude and Longitude of {city}, {state} is {lat_lon[0]}, {lat_lon[1]}.")
        return city, state, lat_lon[0], lat_lon[1]
    else:
        print("Location not found.")

def get_weather_data(lat, lon):
    base_url = f"https://api.weather.gov/points/{lat},{lon}"
    try:
        response = req.get(base_url)
        response.raise_for_status()
        data = response.json()
        forecast_url = data["properties"]["forecast"]
        forecast_response = req.get(forecast_url)
        forecast_response.raise_for_status()
        return forecast_response.json()
    except req.exceptions.HTTPError as err:
        print(f"Error fetching weather data: {err}")
        return None

weather = {}

def update_weather_data(city, state, lat, lon, weather):
    weather_data = get_weather_data(lat, lon)
    if weather_data:
        period = weather_data["properties"]["periods"][0]
        weather[city] = {
            "state": state,
            "current_temperature": period["temperature"],
            "high_temperature": period.get("temperature"),  
            "low_temperature": period.get("temperature"),
            "weather_conditions": period["detailedForecast"]
        }
        print(f"Weather data for {city}, {state} updated successfully.")
    else:
        print(f"Unable to update weather data for {city}, {state}.")

def display_weather_data(city, weather):
    data = weather.get(city)
    if data:
        print(f"\nCity: {city}, {data['state']}")
        print(f"Current temperature: {data['current_temperature']}")
        print(f"High temperature: {data['high_temperature']}")
        print(f"Low temperature: {data['low_temperature']}")
        print(f"Conditions: {data['weather_conditions']}\n")

        with open("weather_log.txt", "a") as file:
            file.write(f"\nCity: {city}, {data['state']}\n")
            file.write(f"Current temperature: {data['current_temperature']}\n")
            file.write(f"High temperature: {data['high_temperature']}\n")
            file.write(f"Low temperature: {data['low_temperature']}\n")
            file.write(f"Conditions: {data['weather_conditions']}\n")
            
    else:
        print(f"No weather data available for {city}.")

while True:
    result = test_get_lat_lon() 
    if result:
        city, state, lat, lon = result
        update_weather_data(city, state, lat, lon, weather)
        display_weather_data(city, weather)
