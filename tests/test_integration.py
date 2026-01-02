import unittest
from unittest.mock import patch
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    DEBUG = False

class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
    
    def test_complete_prediction_workflow(self):
        """Test complete prediction workflow from form to result"""
        # Submit prediction form
        response = self.client.post('/predict', data={
            'location': 'Mumbai',
            'date': '2024-07-15',
            'temperature': '28',
            'humidity': '85',
            'pressure': '1008',
            'wind_speed': '12',
            'cloud_cover': '80',
            'season': 'monsoon',
            'time_of_day': 'evening'
        })
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        # Check that prediction results are displayed
        self.assertIn(b'Prediction Results', response.data)
        self.assertIn(b'mm', response.data)  # Should show rainfall amount
        self.assertIn(b'%', response.data)   # Should show probability
    
    def test_api_integration(self):
        """Test API endpoint integration"""
        response = self.client.get('/api/weather-data')
        self.assertEqual(response.status_code, 200)
        
        json_data = response.get_json()
        self.assertIn('locations', json_data)
        self.assertIn('latest_date', json_data)
        
        # Verify data structure
        self.assertIsInstance(json_data['locations'], list)
        self.assertGreater(len(json_data['locations']), 0)
    
    def test_error_handling_integration(self):
        """Test error handling in complete workflow"""
        # Submit form with invalid data
        response = self.client.post('/predict', data={
            'location': 'Test City',
            'date': '2024-06-15',
            'temperature': 'not_a_number',
            'humidity': '70',
            'pressure': '1010',
            'wind_speed': '10',
            'cloud_cover': '60',
            'season': 'summer',
            'time_of_day': 'morning'
        })
        
        # Should handle error gracefully
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'valid numerical values', response.data)

if __name__ == '__main__':
    unittest.main()