import requests
import pandas as pd
import os
from datetime import datetime, timedelta
from config import Config

def fetch_weather_data(location='London', start_date='2020-01-01', end_date='2023-12-31'):
    """Fetch historical weather data from Open-Meteo API"""
    
    # Open-Meteo API endpoint
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    # Parameters for the API request
    params = {
        'latitude': 51.5074,  # London coordinates (you can modify for other locations)
        'longitude': -0.1278,
        'start_date': start_date,
        'end_date': end_date,
        'daily': [
            'temperature_2m_mean',
            'relative_humidity_2m_mean', 
            'surface_pressure_mean',
            'wind_speed_10m_mean',
            'cloud_cover_mean',
            'precipitation_sum'
        ],
        'timezone': 'GMT'
    }
    
    try:
        print(f"Fetching weather data for {location}...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Convert to DataFrame
        df = pd.DataFrame(data['daily'])
        df['date'] = pd.to_datetime(df['time'])
        df['location'] = location
        
        # Add derived features
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['season'] = df['month'].apply(get_season)
        
        # Save raw data
        os.makedirs(Config.RAW_DATA_DIR, exist_ok=True)
        filename = f"{location.lower()}_weather_data.csv"
        filepath = os.path.join(Config.RAW_DATA_DIR, filename)
        df.to_csv(filepath, index=False)
        
        print(f"Data saved to {filepath}")
        print(f"Dataset shape: {df.shape}")
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def get_season(month):
    """Convert month to season"""
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'autumn'

if __name__ == "__main__":
    # Fetch data for multiple locations
    locations = [
        ('London', 51.5074, -0.1278),
        ('New York', 40.7128, -74.0060),
        ('Tokyo', 35.6762, 139.6503),
        ('Sydney', -33.8688, 151.2093)
    ]
    
    for location, lat, lon in locations:
        fetch_weather_data(location)