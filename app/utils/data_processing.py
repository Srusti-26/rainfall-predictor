import pandas as pd
import numpy as np
import joblib
import os
import requests
from config import Config

def load_model_components():
    """Load trained model and preprocessing components"""
    try:
        model_path = os.path.join(Config.MODEL_DIR, 'rainfall_model.pkl')
        scaler_path = os.path.join(Config.MODEL_DIR, 'scaler.pkl')
        location_encoder_path = os.path.join(Config.MODEL_DIR, 'location_encoder.pkl')
        season_encoder_path = os.path.join(Config.MODEL_DIR, 'season_encoder.pkl')
        
        # Check if all files exist and are not empty
        for path in [model_path, scaler_path, location_encoder_path, season_encoder_path]:
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                print(f"Model file missing or empty: {path}")
                return None, None, None, None
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        location_encoder = joblib.load(location_encoder_path)
        season_encoder = joblib.load(season_encoder_path)
        
        return model, scaler, location_encoder, season_encoder
    except (FileNotFoundError, EOFError, Exception) as e:
        print(f"Error loading model files: {e}")
        return None, None, None, None

def preprocess_input(location, date, temperature, humidity, pressure, wind_speed, cloud_cover, season, time_of_day):
    """Preprocess user input for model prediction"""
    
    # Convert date to month and day
    from datetime import datetime
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    month = date_obj.month
    day = date_obj.day
    
    # Load encoders
    _, _, location_encoder, season_encoder = load_model_components()
    
    if location_encoder is None or season_encoder is None:
        # Fallback encoding if models not available
        location_encoded = hash(location.lower()) % 10
        season_encoded = {'spring': 0, 'summer': 1, 'autumn': 2, 'winter': 3}.get(season.lower(), 0)
    else:
        # Use trained encoders
        try:
            location_encoded = location_encoder.transform([location.lower()])[0]
        except ValueError:
            location_encoded = 0  # Default for unknown location
            
        try:
            season_encoded = season_encoder.transform([season.lower()])[0]
        except ValueError:
            season_encoded = 0  # Default for unknown season
    
    # Create feature array
    features = np.array([[
        temperature,
        humidity,
        pressure,
        wind_speed,
        cloud_cover,
        month,
        day,
        location_encoded,
        season_encoded
    ]])
    
    return features

def get_location_coordinates(location_name):
    """Get real coordinates for any location"""
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json&limit=1"
        response = requests.get(url, headers={'User-Agent': 'RainfallPredictor/1.0'}, timeout=5)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None, None

def get_location_climate_factor(location_name):
    """Get climate adjustment factor based on real location data"""
    lat, lon = get_location_coordinates(location_name)
    
    if lat and lon:
        # Latitude-based climate adjustments (more accurate)
        if abs(lat) < 10:  # Tropical zone
            return 1.4
        elif abs(lat) < 23.5:  # Subtropical
            return 1.2
        elif abs(lat) < 35:  # Temperate
            return 1.0
        elif abs(lat) < 50:  # Cool temperate
            return 0.9
        else:  # Polar/subpolar
            return 0.6
    
    return 1.0  # Default if location not found

def predict_rainfall(location, date, temperature, humidity, pressure, wind_speed, cloud_cover, season, time_of_day):
    """Make rainfall prediction using enhanced location-aware system"""
    
    # Use improved rule-based prediction with real location data
    prediction = rule_based_prediction(humidity, cloud_cover, temperature, pressure)
    
    # Add seasonal adjustments (enhanced for Indian monsoon patterns)
    season_multiplier = {
        'winter': 0.7,
        'spring': 1.1, 
        'summer': 0.8,
        'autumn': 1.2,
        'monsoon': 1.8,  # Peak monsoon season
        'pre-monsoon': 1.3,
        'post-monsoon': 1.1
    }.get(season.lower(), 1.0)
    
    # Get real location-based climate factor
    climate_factor = get_location_climate_factor(location)
    
    # Additional keyword-based and regional adjustments
    location_lower = location.lower()
    keyword_multiplier = 1.0
    
    # Karnataka-specific rainfall patterns
    if any(word in location_lower for word in ['mangalore', 'udupi', 'karwar', 'byndoor', 'kundapur', 'honnavar', 'kumta', 'ankola', 'bhatkal']):
        keyword_multiplier = 1.6  # Coastal Karnataka - high monsoon
    elif any(word in location_lower for word in ['puttur', 'sullia', 'sirsi']):
        keyword_multiplier = 1.5  # Western Ghats - very high rainfall
    elif any(word in location_lower for word in ['chikmagalur', 'hassan', 'shimoga']):
        keyword_multiplier = 1.4  # Hill stations - high rainfall
    elif any(word in location_lower for word in ['bangalore', 'mysore', 'mandya', 'tumkur']):
        keyword_multiplier = 1.2  # South Karnataka - moderate rainfall
    elif any(word in location_lower for word in ['hubli', 'dharwad', 'belgaum', 'bagalkot']):
        keyword_multiplier = 1.0  # North Karnataka - moderate rainfall
    elif any(word in location_lower for word in ['bijapur', 'gulbarga', 'bidar', 'raichur', 'bellary']):
        keyword_multiplier = 0.8  # North Karnataka plains - lower rainfall
    elif any(word in location_lower for word in ['karnataka']):
        keyword_multiplier = 1.2  # General Karnataka
    elif any(word in location_lower for word in ['coast', 'beach', 'port', 'bay', 'island', 'sea']):
        keyword_multiplier = 1.2
    elif any(word in location_lower for word in ['mountain', 'hill', 'peak', 'valley']):
        keyword_multiplier = 1.3
    elif any(word in location_lower for word in ['desert', 'arid']):
        keyword_multiplier = 0.3
    
    # Combine climate factor with keyword adjustments
    location_multiplier = climate_factor * keyword_multiplier
    
    prediction = prediction * season_multiplier * location_multiplier
    
    return round(max(0, prediction), 2)

def rule_based_prediction(humidity, cloud_cover, temperature, pressure):
    """Improved rule-based prediction as fallback"""
    
    # Base prediction starts at 0
    base_prediction = 0
    
    # Primary factor: humidity and cloud cover combination
    if humidity > 85 and cloud_cover > 80:
        base_prediction = 12 + (humidity - 85) * 0.4 + (cloud_cover - 80) * 0.3
    elif humidity > 75 and cloud_cover > 70:
        base_prediction = 6 + (humidity - 75) * 0.3 + (cloud_cover - 70) * 0.2
    elif humidity > 65 and cloud_cover > 60:
        base_prediction = 2 + (humidity - 65) * 0.2 + (cloud_cover - 60) * 0.15
    elif humidity > 50 and cloud_cover > 40:
        base_prediction = 0.5 + (humidity - 50) * 0.1 + (cloud_cover - 40) * 0.05
    
    # Temperature adjustments (optimal rain temp 10-25°C)
    if 10 <= temperature <= 25:
        temp_factor = 1.0
    elif temperature < 10:
        temp_factor = 0.8 + (temperature / 50)  # Cold reduces liquid rain
    elif temperature > 25:
        temp_factor = 1.2 - ((temperature - 25) * 0.02)  # Hot can increase evaporation
    else:
        temp_factor = 0.6
    
    base_prediction *= temp_factor
    
    # Pressure adjustments (low pressure = more rain)
    if pressure < 990:
        pressure_factor = 1.4
    elif pressure < 1005:
        pressure_factor = 1.2
    elif pressure < 1015:
        pressure_factor = 1.0
    elif pressure < 1025:
        pressure_factor = 0.8
    else:
        pressure_factor = 0.6
    
    base_prediction *= pressure_factor
    
    # Add some variability based on input combination
    variability = (humidity + cloud_cover + abs(temperature - 20) + abs(pressure - 1013)) % 10
    base_prediction += variability * 0.1
    
    return round(max(0, base_prediction), 2)

def calculate_rain_probability(prediction):
    """Calculate probability of rain based on prediction"""
    if prediction == 0:
        return 0
    elif prediction < 1:
        return 20
    elif prediction < 5:
        return 40
    elif prediction < 10:
        return 60
    elif prediction < 20:
        return 80
    else:
        return 95

def get_weather_description(prediction, humidity, cloud_cover):
    """Get weather description based on prediction and conditions"""
    if prediction == 0:
        if cloud_cover < 30:
            return "Clear skies"
        elif cloud_cover < 60:
            return "Partly cloudy"
        else:
            return "Cloudy but no rain expected"
    elif prediction < 1:
        return "Light drizzle possible"
    elif prediction < 5:
        return "Light rain expected"
    elif prediction < 15:
        return "Moderate rain expected"
    else:
        return "Heavy rain expected"