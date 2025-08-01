import os
import requests
import json
from datetime import datetime

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = ["Lahore", "Karachi", "Islamabad"]
DATA_DIR = "aqi_data"
DATA_FILE = os.path.join(DATA_DIR, "aqi_data.json")

if not API_KEY:
    raise Exception("Missing OPENWEATHER_API_KEY in environment!")

os.makedirs(DATA_DIR, exist_ok=True)

# Load existing data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

for city in CITIES:
    print(f"Collecting data for {city}...")

    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        print(f"Failed to get weather data for {city}")
        continue

    weather_data = weather_response.json()
    lat = weather_data["coord"]["lat"]
    lon = weather_data["coord"]["lon"]

    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    aqi_response = requests.get(aqi_url)

    if aqi_response.status_code != 200:
        print(f"Failed to get AQI data for {city}")
        continue

    aqi_json = aqi_response.json()
    aqi_main = aqi_json["list"][0]

    entry = {
        "city": city,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "aqi_level": aqi_main["main"]["aqi"],
        "components": aqi_main["components"],
        "weather": {
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "condition": weather_data["weather"][0]["description"]
        }
    }

    existing_data.append(entry)

# Save all collected entries back
with open(DATA_FILE, "w") as f:
    json.dump(existing_data, f, indent=2)

print("✅ AQI & weather data collected and saved for all cities.")
