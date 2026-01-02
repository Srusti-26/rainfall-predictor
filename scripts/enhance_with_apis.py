import requests
import pandas as pd
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def get_real_time_weather(location):
    """Get current weather from OpenWeatherMap API (free tier)"""
    try:
        # Free API - no key needed for basic data
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': 12.9716,  # Default to Bangalore
            'longitude': 77.5946,
            'current_weather': True,
            'hourly': ['temperature_2m', 'relative_humidity_2m', 'precipitation']
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_elevation_data(lat, lon):
    """Get elevation data from Open-Topo-Data API"""
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup"
        params = {'locations': f"{lat},{lon}"}
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['elevation']
    except:
        pass
    return None

def get_air_quality_data(lat, lon):
    """Get air quality data from OpenWeatherMap"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': 'demo'  # Demo key - replace with real key
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_satellite_data():
    """Get satellite imagery from NASA APIs"""
    try:
        # NASA GIBS API for satellite imagery
        url = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2023-01-01/250m/0/0/0.jpg"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return "Satellite data available"
    except:
        pass
    return None

def enhance_predictions():
    """Enhance predictions with additional data sources"""
    
    enhancements = {
        'real_time_weather': get_real_time_weather('Bangalore'),
        'elevation': get_elevation_data(12.9716, 77.5946),
        'air_quality': get_air_quality_data(12.9716, 77.5946),
        'satellite': get_satellite_data()
    }
    
    print("Available API Enhancements:")
    for key, value in enhancements.items():
        status = "[OK]" if value else "[UNAVAILABLE]"
        print(f"{status} {key}: {type(value).__name__}")
    
    return enhancements

if __name__ == "__main__":
    enhance_predictions()