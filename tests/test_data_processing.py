import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from app.utils.data_processing import (
    rule_based_prediction, calculate_rain_probability, 
    get_weather_description, predict_rainfall, preprocess_input
)

class TestDataProcessing(unittest.TestCase):
    
    def test_rule_based_prediction_high_humidity_cloud(self):
        """Test rule-based prediction with high humidity and cloud cover"""
        result = rule_based_prediction(90, 85, 20, 1000)
        self.assertGreater(result, 10)
        self.assertIsInstance(result, float)
    
    def test_rule_based_prediction_low_conditions(self):
        """Test rule-based prediction with low humidity and cloud cover"""
        result = rule_based_prediction(30, 20, 25, 1020)
        self.assertLessEqual(result, 2)
    
    def test_calculate_rain_probability_zero(self):
        """Test rain probability calculation for zero prediction"""
        self.assertEqual(calculate_rain_probability(0), 0)
    
    def test_calculate_rain_probability_light(self):
        """Test rain probability for light rain"""
        self.assertEqual(calculate_rain_probability(0.5), 20)
        self.assertEqual(calculate_rain_probability(3), 40)
    
    def test_calculate_rain_probability_heavy(self):
        """Test rain probability for heavy rain"""
        self.assertEqual(calculate_rain_probability(25), 95)
    
    def test_get_weather_description_clear(self):
        """Test weather description for clear conditions"""
        desc = get_weather_description(0, 40, 20)
        self.assertEqual(desc, "Clear skies")
    
    def test_get_weather_description_heavy_rain(self):
        """Test weather description for heavy rain"""
        desc = get_weather_description(20, 80, 90)
        self.assertEqual(desc, "Heavy rain expected")
    
    def test_predict_rainfall_basic(self):
        """Test basic rainfall prediction"""
        result = predict_rainfall("London", "2024-01-15", 15, 70, 1010, 10, 60, "winter", "morning")
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)
    
    @patch('app.utils.data_processing.get_location_coordinates')
    def test_predict_rainfall_with_location(self, mock_coords):
        """Test rainfall prediction with location coordinates"""
        mock_coords.return_value = (51.5074, -0.1278)  # London coordinates
        result = predict_rainfall("London", "2024-06-15", 20, 80, 1005, 15, 70, "summer", "afternoon")
        self.assertGreater(result, 0)
    
    def test_preprocess_input_basic(self):
        """Test input preprocessing"""
        features = preprocess_input("London", "2024-06-15", 20, 70, 1010, 10, 50, "summer", "morning")
        self.assertEqual(features.shape, (1, 9))
        self.assertEqual(features[0][5], 6)  # June = month 6
        self.assertEqual(features[0][6], 15)  # Day 15

if __name__ == '__main__':
    unittest.main()