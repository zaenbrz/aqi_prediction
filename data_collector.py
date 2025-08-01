import datetime
import os
import json
import requests

# ==== CONFIGURATION ====
cities = {
    "Karachi": {"lat": 24.8607, "lon": 67.0011},
    "Lahore": {"lat": 31.5497, "lon": 74.3436},
    "Islamabad": {"lat": 33.6844, "lon": 73.0479}
}
OPENWEATHER_API_KEY = os.environ["OPENWEATHER_API_KEY"]
if not OPENWEATHER_API_KEY:
    raise EnvironmentError("❌ OPENWEATHER_API_KEY not found in environment variables.")
DATA_DIR = "aqi_data"
os.makedirs(DATA_DIR, exist_ok=True) 

# Create storage directory if not exists
os.makedirs(DATA_DIR, exist_ok=True)

# ==== HELPER FUNCTION ====
def fetch_weather_data(lat, lon):
    open_meteo_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,wind_speed_10m,shortwave_radiation,direct_radiation"
        f"&daily=dominant_wind_direction_10m_dominant"
        f"&timezone=Asia/Karachi"
    )
    response = requests.get(open_meteo_url)
    return response.json()

def fetch_pollution_data(lat, lon):
    openweather_url = (
        f"http://api.openweathermap.org/data/2.5/air_pollution/forecast"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    )
    response = requests.get(openweather_url)
    return response.json()

# ==== MAIN SCRIPT ====
today = datetime.datetime.now().strftime("%Y-%m-%d")
data_output = {}

for city, coords in cities.items():
    print(f"Fetching data for {city}...")

    # Fetch weather and pollution data
    weather = fetch_weather_data(coords["lat"], coords["lon"])
    pollution = fetch_pollution_data(coords["lat"], coords["lon"])

    # Combine results
    data_output[city] = {
        "date": today,
        "weather": weather,
        "pollution": pollution
    }

# Save data to file
output_file = os.path.join(DATA_DIR, f"aqi_data_{today}.json")
with open(output_file, "w") as f:
    json.dump(data_output, f, indent=2)

print(f"✅ Data saved to {output_file}")