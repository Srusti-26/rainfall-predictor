from flask import Flask
from config import Config

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Ensure required directories exist
    Config.create_directories()
    
    # Register blueprints (routes)
    from app.routes import main
    app.register_blueprint(main)
    
    # Return the configured app
    return app