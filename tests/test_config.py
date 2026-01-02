import unittest
import os
import tempfile
import shutil
from config import Config

class TestConfig(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_base_dir = Config.BASE_DIR
        Config.BASE_DIR = self.test_dir
    
    def tearDown(self):
        """Clean up test environment"""
        Config.BASE_DIR = self.original_base_dir
        shutil.rmtree(self.test_dir)
    
    def test_config_attributes(self):
        """Test configuration attributes exist"""
        self.assertTrue(hasattr(Config, 'SECRET_KEY'))
        self.assertTrue(hasattr(Config, 'DEBUG'))
        self.assertTrue(hasattr(Config, 'WEATHER_API_URL'))
        self.assertTrue(hasattr(Config, 'MODEL_FEATURES'))
        self.assertTrue(hasattr(Config, 'TARGET_VARIABLE'))
    
    def test_config_values(self):
        """Test configuration values are correct types"""
        self.assertIsInstance(Config.SECRET_KEY, str)
        self.assertIsInstance(Config.DEBUG, bool)
        self.assertIsInstance(Config.MODEL_FEATURES, list)
        self.assertIsInstance(Config.TEST_SIZE, float)
        self.assertIsInstance(Config.RANDOM_STATE, int)
    
    def test_create_directories(self):
        """Test directory creation"""
        Config.create_directories()
        
        expected_dirs = [
            Config.RAW_DATA_DIR,
            Config.PROCESSED_DATA_DIR,
            Config.MODEL_DIR
        ]
        
        for directory in expected_dirs:
            self.assertTrue(os.path.exists(directory))
            self.assertTrue(os.path.isdir(directory))
    
    def test_model_features_content(self):
        """Test model features contain expected items"""
        expected_features = [
            'temperature_2m_mean', 'relative_humidity_2m_mean', 
            'surface_pressure_mean', 'wind_speed_10m_mean', 
            'cloud_cover_mean', 'month', 'day'
        ]
        
        for feature in expected_features:
            self.assertIn(feature, Config.MODEL_FEATURES)

if __name__ == '__main__':
    unittest.main()