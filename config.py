import os

class Config:
    """Configuration settings for the Rainfall Predictor application"""
    
    # Flask configuration
    SECRET_KEY = 'srrain@prediction#'  
    DEBUG = True
    
    # Open-source weather data configuration
    WEATHER_API_URL = 'https://archive-api.open-meteo.com/v1/archive'
    
    # Data paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
    PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    
    # Model parameters
    MODEL_FEATURES = [
        'temperature_2m_mean', 'relative_humidity_2m_mean', 'surface_pressure_mean', 
        'wind_speed_10m_mean', 'cloud_cover_mean', 'month', 'day'
    ]
    TARGET_VARIABLE = 'precipitation_sum'
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    # Ensure directories exist
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        for directory in [cls.RAW_DATA_DIR, cls.PROCESSED_DATA_DIR, cls.MODEL_DIR]:
            os.makedirs(directory, exist_ok=True)