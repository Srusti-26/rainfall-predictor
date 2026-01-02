import unittest
from unittest.mock import patch
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    DEBUG = False

class TestRoutes(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
    
    def test_index_route(self):
        """Test homepage route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Rainfall Predictor', response.data)
    
    def test_predict_get_route(self):
        """Test prediction page GET request"""
        response = self.client.get('/predict')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'predict', response.data.lower())
    
    def test_predict_post_valid_data(self):
        """Test prediction POST with valid data"""
        response = self.client.post('/predict', data={
            'location': 'London',
            'date': '2024-06-15',
            'temperature': '20',
            'humidity': '70',
            'pressure': '1010',
            'wind_speed': '10',
            'cloud_cover': '60',
            'season': 'summer',
            'time_of_day': 'morning'
        })
        
        self.assertEqual(response.status_code, 200)
        # Check that prediction results are in the response
        self.assertIn(b'Prediction Results', response.data)
    
    def test_predict_post_invalid_data(self):
        """Test prediction POST with invalid data"""
        response = self.client.post('/predict', data={
            'location': 'London',
            'date': '2024-06-15',
            'temperature': 'invalid',
            'humidity': '70',
            'pressure': '1010',
            'wind_speed': '10',
            'cloud_cover': '60',
            'season': 'summer',
            'time_of_day': 'morning'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'valid numerical values', response.data)
    
    def test_api_weather_data(self):
        """Test weather data API endpoint"""
        response = self.client.get('/api/weather-data')
        self.assertEqual(response.status_code, 200)
        
        json_data = response.get_json()
        self.assertIn('locations', json_data)
        self.assertIn('latest_date', json_data)
        self.assertIsInstance(json_data['locations'], list)

if __name__ == '__main__':
    unittest.main()