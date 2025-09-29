from __future__ import print_function
import os
import time
from datetime import date, timedelta
from pprint import pprint
from dotenv import load_dotenv

# --- Imports that are known to work with the standard WeatherAPI Python SDK structure ---
from weatherapi.configuration import Configuration
from weatherapi.api_client import ApiClient
from weatherapi.api.apis_api import APIsApi
from weatherapi.rest import ApiException

# --- 1. ENVIRONMENT SETUP ---
# Load variables from .env file (assuming it contains WEATHER_API_KEY=your_key_here)
load_dotenv()

# Configure API key authorization: ApiKeyAuth
configuration = Configuration()

# Check if the key is available before proceeding
API_KEY = os.getenv('WEATHER_API_KEY')
if not API_KEY:
    print("Error: WEATHER_API_KEY is not set in your environment or .env file.")
    exit()

configuration.api_key['key'] = API_KEY

# --- 2. API INSTANCE AND PARAMETERS ---

# Create an instance of the API class
api_instance = APIsApi(ApiClient(configuration))

# Define location (q) and future date (dt)
# CHANGED: Setting the location to Trichy, Tamil Nadu, India
q = 'Jaipur'  # str | Example: 'London', '90210', '48.8582,2.2945'

# Calculate a future date (30 days from today) in yyyy-MM-dd format
future_date = date.today() + timedelta(days=30)
dt = future_date.strftime('%Y-%m-%d') # date | Must be 14-300 days in the future

print(f"\n--- Weather Forecast for {q} on {dt} ---")

# --- 3. API CALL AND ERROR HANDLING ---
try:
    # Future API call
    api_response = api_instance.future_weather(q, dt=dt) 
    
    # Access response data using dictionary keys for stability
    forecast_data = api_response.get('forecast')
    location_data = api_response.get('location')
    
    if forecast_data and forecast_data.get('forecastday') and location_data:
        # Navigate to the daily summary and hourly data
        forecast_day_data = forecast_data['forecastday'][0]
        day_summary = forecast_day_data['day']
        hourly_data = forecast_day_data['hour']
        
        # --- Print Daily Summary ---
        print(f"Location: {location_data.get('name')}, {location_data.get('country')}")
        print("-" * 50)
        print(f"Daily Condition: {day_summary.get('condition', {}).get('text')}")
        print(f"Max Temp: {day_summary.get('maxtemp_c')}°C / Min Temp: {day_summary.get('mintemp_c')}°C")
        print(f"Average Humidity: {day_summary.get('avghumidity')}%")
        print("-" * 50)

        # --- Print Hourly Summary ---
        print("HOURLY BREAKDOWN:")
        # UPDATED HEADER to include HMD
        print(" Time | Temp | PoP | HMD | Condition")
        print("------|------|-----|-----|---------------------------------")
        
        # Loop through all 24 hourly forecasts
        for hour_forecast in hourly_data:
            # Extract time string and format it for cleaner display
            time_str = hour_forecast.get('time', 'N/A').split(' ')[-1]
            temp_c = hour_forecast.get('temp_c', 'N/A')
            # Extract the chance of rain (PoP)
            rain_chance = hour_forecast.get('chance_of_rain', 'N/A')
            # NEW: Extract the humidity percentage (HMD)
            humidity_percent = hour_forecast.get('humidity', 'N/A')
            condition = hour_forecast.get('condition', {}).get('text', 'N/A')
            
            # Print the formatted hourly entry, including all four metrics
            print(f" {time_str} | {temp_c:<4}°C | {rain_chance:>3}% | {humidity_percent:>3}% | {condition}")

    else:
        print("Error: Forecast data structure is incomplete or missing in the response.")


except ApiException as e:
    # Handle API-specific errors (e.g., invalid date range, invalid key)
    print(f"API Error: Failed to fetch weather data. Details: {e}")
except Exception as e:
    # Handle general Python exceptions
    print(f"General Error: An unexpected error occurred: {e}")
