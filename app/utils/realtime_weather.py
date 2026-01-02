import requests
from datetime import datetime

def get_current_weather_data(location_name):
    """Get current weather data for auto-filling the form"""
    try:
        # Get coordinates first
        geocode_url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json&limit=1"
        geo_response = requests.get(geocode_url, headers={'User-Agent': 'RainfallPredictor/1.0'}, timeout=5)
        geo_data = geo_response.json()
        
        if not geo_data:
            return None
            
        lat = float(geo_data[0]['lat'])
        lon = float(geo_data[0]['lon'])
        
        # Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': True,
            'hourly': ['temperature_2m', 'relative_humidity_2m', 'surface_pressure', 
                      'wind_speed_10m', 'cloud_cover'],
            'timezone': 'auto'
        }
        
        weather_response = requests.get(weather_url, params=params, timeout=10)
        weather_data = weather_response.json()
        
        if 'current_weather' in weather_data and 'hourly' in weather_data:
            current = weather_data['current_weather']
            hourly = weather_data['hourly']
            
            # Get current hour index
            current_time = datetime.now().hour
            
            return {
                'temperature': round(current.get('temperature', 20), 1),
                'humidity': round(hourly['relative_humidity_2m'][current_time] if current_time < len(hourly['relative_humidity_2m']) else 70, 1),
                'pressure': round(hourly['surface_pressure'][current_time] if current_time < len(hourly['surface_pressure']) else 1013, 1),
                'wind_speed': round(current.get('windspeed', 10), 1),
                'cloud_cover': round(hourly['cloud_cover'][current_time] if current_time < len(hourly['cloud_cover']) else 50, 1),
                'location': location_name,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            
    except Exception as e:
        print(f"Error fetching real-time weather: {e}")
        return None

def get_weather_alerts(lat, lon):
    """Get weather alerts and warnings"""
    try:
        # Using Open-Meteo alerts (if available)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': ['precipitation_sum', 'precipitation_probability_max'],
            'timezone': 'auto'
        }
        
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if 'daily' in data:
            today_precip = data['daily']['precipitation_sum'][0]
            today_prob = data['daily']['precipitation_probability_max'][0]
            
            alerts = []
            if today_precip > 50:
                alerts.append("Heavy rainfall expected today")
            elif today_prob > 80:
                alerts.append("High probability of rain today")
                
            return alerts
            
    except:
        pass
    return []