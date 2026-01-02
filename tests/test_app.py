import unittest
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    DEBUG = False

class TestApp(unittest.TestCase):
    
    def test_create_app(self):
        """Test Flask app creation"""
        app = create_app(TestConfig)
        self.assertIsNotNone(app)
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['DEBUG'])
    
    def test_app_config(self):
        """Test app configuration loading"""
        app = create_app(TestConfig)
        self.assertEqual(app.config['TESTING'], True)
        self.assertIn('SECRET_KEY', app.config)
    
    def test_blueprints_registered(self):
        """Test that blueprints are registered"""
        app = create_app(TestConfig)
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        self.assertIn('main', blueprint_names)
    
    def test_app_context(self):
        """Test app context functionality"""
        app = create_app(TestConfig)
        with app.app_context():
            from flask import current_app
            self.assertEqual(app, current_app)

if __name__ == '__main__':
    unittest.main()