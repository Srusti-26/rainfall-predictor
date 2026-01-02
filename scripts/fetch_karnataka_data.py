import requests
import pandas as pd
import os
import sys
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def get_karnataka_locations():
    """Karnataka districts and major taluks with coordinates"""
    return {
        # Coastal Karnataka
        'Mangalore': {'lat': 12.9141, 'lon': 74.8560, 'district': 'Dakshina Kannada'},
        'Udupi': {'lat': 13.3409, 'lon': 74.7421, 'district': 'Udupi'},
        'Karwar': {'lat': 14.8142, 'lon': 74.1297, 'district': 'Uttara Kannada'},
        'Sirsi': {'lat': 14.6186, 'lon': 74.8370, 'district': 'Uttara Kannada'},
        
        # Bangalore Division
        'Bangalore': {'lat': 12.9716, 'lon': 77.5946, 'district': 'Bangalore Urban'},
        'Mysore': {'lat': 12.2958, 'lon': 76.6394, 'district': 'Mysore'},
        'Mandya': {'lat': 12.5218, 'lon': 76.8951, 'district': 'Mandya'},
        'Hassan': {'lat': 13.0033, 'lon': 76.0977, 'district': 'Hassan'},
        'Tumkur': {'lat': 13.3379, 'lon': 77.1022, 'district': 'Tumkur'},
        'Kolar': {'lat': 13.1378, 'lon': 78.1294, 'district': 'Kolar'},
        'Chikkaballapur': {'lat': 13.4355, 'lon': 77.7315, 'district': 'Chikkaballapur'},
        'Ramanagara': {'lat': 12.7206, 'lon': 77.2817, 'district': 'Ramanagara'},
        
        # North Karnataka
        'Hubli': {'lat': 15.3647, 'lon': 75.1240, 'district': 'Dharwad'},
        'Dharwad': {'lat': 15.4589, 'lon': 75.0078, 'district': 'Dharwad'},
        'Belgaum': {'lat': 15.8497, 'lon': 74.4977, 'district': 'Belgaum'},
        'Bagalkot': {'lat': 16.1875, 'lon': 75.6972, 'district': 'Bagalkot'},
        'Bijapur': {'lat': 16.8302, 'lon': 75.7100, 'district': 'Bijapur'},
        'Gulbarga': {'lat': 17.3297, 'lon': 76.8343, 'district': 'Gulbarga'},
        'Bidar': {'lat': 17.9104, 'lon': 77.5199, 'district': 'Bidar'},
        'Raichur': {'lat': 16.2120, 'lon': 77.3439, 'district': 'Raichur'},
        'Koppal': {'lat': 15.3512, 'lon': 76.1549, 'district': 'Koppal'},
        'Gadag': {'lat': 15.4318, 'lon': 75.6306, 'district': 'Gadag'},
        
        # South Karnataka
        'Shimoga': {'lat': 13.9299, 'lon': 75.5681, 'district': 'Shimoga'},
        'Chikmagalur': {'lat': 13.3161, 'lon': 75.7720, 'district': 'Chikmagalur'},
        'Davangere': {'lat': 14.4644, 'lon': 75.9218, 'district': 'Davangere'},
        'Chitradurga': {'lat': 14.2251, 'lon': 76.3980, 'district': 'Chitradurga'},
        'Bellary': {'lat': 15.1394, 'lon': 76.9214, 'district': 'Bellary'},
        
        # Additional Major Taluks
        'Puttur': {'lat': 12.7596, 'lon': 75.2068, 'district': 'Dakshina Kannada'},
        'Sullia': {'lat': 12.5622, 'lon': 75.3931, 'district': 'Dakshina Kannada'},
        'Kundapur': {'lat': 13.6269, 'lon': 74.6951, 'district': 'Udupi'},
        'Byndoor': {'lat': 13.8667, 'lon': 74.6333, 'district': 'Udupi'},
        'Honnavar': {'lat': 14.2833, 'lon': 74.4500, 'district': 'Uttara Kannada'},
        'Kumta': {'lat': 14.4167, 'lon': 74.4167, 'district': 'Uttara Kannada'},
        'Ankola': {'lat': 14.6667, 'lon': 74.3000, 'district': 'Uttara Kannada'},
        'Bhatkal': {'lat': 13.9667, 'lon': 74.5667, 'district': 'Uttara Kannada'},
        
        # More Taluks
        'Channapatna': {'lat': 12.6518, 'lon': 77.2067, 'district': 'Ramanagara'},
        'Kanakapura': {'lat': 12.5449, 'lon': 77.4188, 'district': 'Ramanagara'},
        'Magadi': {'lat': 12.9581, 'lon': 77.2244, 'district': 'Ramanagara'},
        'Doddaballapur': {'lat': 13.2218, 'lon': 77.5463, 'district': 'Bangalore Rural'},
        'Devanahalli': {'lat': 13.2419, 'lon': 77.7081, 'district': 'Bangalore Rural'},
        'Hoskote': {'lat': 13.0681, 'lon': 77.7981, 'district': 'Bangalore Rural'},
        'Nelamangala': {'lat': 13.1022, 'lon': 77.3932, 'district': 'Bangalore Rural'},
    }

def fetch_karnataka_weather_data():
    """Fetch weather data for Karnataka locations"""
    
    locations = get_karnataka_locations()
    start_date = '2022-01-01'
    end_date = '2023-12-31'
    
    print(f"Fetching weather data for {len(locations)} Karnataka locations...")
    
    for location, coords in locations.items():
        print(f"Fetching data for {location} ({coords['district']})...")
        
        url = "https://archive-api.open-meteo.com/v1/archive"
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
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if 'daily' in data:
                df = pd.DataFrame(data['daily'])
                df['location'] = location
                df['district'] = coords['district']
                df['date'] = pd.to_datetime(df['time'])
                df['month'] = df['date'].dt.month
                df['day'] = df['date'].dt.day
                
                # Karnataka-specific seasons
                def get_karnataka_season(month):
                    if month in [12, 1, 2]:
                        return 'winter'
                    elif month in [3, 4, 5]:
                        return 'summer'
                    elif month in [6, 7, 8, 9]:
                        return 'monsoon'
                    else:
                        return 'post-monsoon'
                
                df['season'] = df['month'].apply(get_karnataka_season)
                
                # Save individual file
                filename = f"karnataka_{location.lower().replace(' ', '_')}_weather_data.csv"
                filepath = os.path.join(Config.RAW_DATA_DIR, filename)
                df.to_csv(filepath, index=False)
                print(f"[OK] Saved {location} data")
                
            time.sleep(0.5)  # Rate limiting
                
        except Exception as e:
            print(f"[ERROR] Error fetching {location} data: {e}")
            continue

if __name__ == "__main__":
    Config.create_directories()
    fetch_karnataka_weather_data()
    print("Karnataka weather data fetch completed!")