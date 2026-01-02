import requests
import pandas as pd
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def fetch_indian_weather_data():
    """Fetch weather data for major Indian cities"""
    
    # Indian cities with coordinates
    indian_cities = {
        'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
        'Delhi': {'lat': 28.7041, 'lon': 77.1025},
        'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
        'Chennai': {'lat': 13.0827, 'lon': 80.2707},
        'Kolkata': {'lat': 22.5726, 'lon': 88.3639},
        'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
        'Pune': {'lat': 18.5204, 'lon': 73.8567},
        'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714}
    }
    
    # Date range for data
    start_date = '2022-01-01'
    end_date = '2023-12-31'
    
    for city, coords in indian_cities.items():
        print(f"Fetching data for {city}...")
        
        # API URL for Open-Meteo
        url = f"https://archive-api.open-meteo.com/v1/archive"
        params = {
            'latitude': coords['lat'],
            'longitude': coords['lon'],
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
            'timezone': 'Asia/Kolkata'
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'daily' in data:
                # Create DataFrame
                df = pd.DataFrame(data['daily'])
                df['location'] = city
                df['date'] = pd.to_datetime(df['time'])
                df['month'] = df['date'].dt.month
                df['day'] = df['date'].dt.day
                
                # Add season based on Indian climate
                def get_indian_season(month):
                    if month in [12, 1, 2]:
                        return 'winter'
                    elif month in [3, 4, 5]:
                        return 'summer'
                    elif month in [6, 7, 8, 9]:
                        return 'monsoon'
                    else:
                        return 'post-monsoon'
                
                df['season'] = df['month'].apply(get_indian_season)
                
                # Save to CSV
                filename = f"{city.lower()}_weather_data.csv"
                filepath = os.path.join(Config.RAW_DATA_DIR, filename)
                df.to_csv(filepath, index=False)
                print(f"[OK] Saved {city} data to {filename}")
                
        except Exception as e:
            print(f"[ERROR] Error fetching {city} data: {e}")

if __name__ == "__main__":
    Config.create_directories()
    fetch_indian_weather_data()
    print("Indian weather data fetch completed!")