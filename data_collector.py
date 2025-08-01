import os
import requests
import pandas as pd
from datetime import datetime

# Ensure the output directory exists
os.makedirs("aqi_data", exist_ok=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Islamabad"
URL = f"http://api.openweathermap.org/data/2.5/air_pollution?appid={API_KEY}"

# Get coordinates for the city using OpenWeather geocoding API
geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={CITY}&limit=1&appid={API_KEY}"
geo_res = requests.get(geo_url)

if geo_res.status_code != 200 or not geo_res.json():
    raise Exception(f"Failed to fetch geolocation for city {CITY}: {geo_res.text}")

lat = geo_res.json()[0]['lat']
lon = geo_res.json()[0]['lon']

# Now fetch AQI data
aqi_url = f"{URL}&lat={lat}&lon={lon}"
res = requests.get(aqi_url)

if res.status_code != 200:
    raise Exception(f"Failed to fetch AQI data: {res.text}")

data = res.json()
timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")

# Save to JSON
out_path = f"aqi_data/{CITY.lower()}_{timestamp}.json"
with open(out_path, "w") as f:
    f.write(res.text)

print(f"AQI data saved to {out_path}")
