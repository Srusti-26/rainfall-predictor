#!/usr/bin/env python3
"""
Setup script for Rainfall Predictor
Run this script to set up the project and train the initial model.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("✗ Failed to install requirements")
        return False
    return True

def fetch_sample_data():
    """Fetch sample weather data"""
    print("Fetching sample weather data...")
    try:
        from scripts.fetch_data import fetch_weather_data
        # Fetch data for London only (smaller dataset for demo)
        fetch_weather_data('London', '2022-01-01', '2023-12-31')
        print("✓ Sample data fetched successfully!")
    except Exception as e:
        print(f"✗ Failed to fetch data: {e}")
        return False
    return True

def train_initial_model():
    """Train the initial ML model"""
    print("Training initial machine learning model...")
    try:
        from scripts.train_model import train_model
        train_model()
        print("✓ Model trained successfully!")
    except Exception as e:
        print(f"✗ Failed to train model: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("=" * 50)
    print("Rainfall Predictor Setup")
    print("=" * 50)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("Setup failed at requirements installation")
        return
    
    # Step 2: Fetch sample data
    if not fetch_sample_data():
        print("Setup failed at data fetching")
        print("The app will still work with rule-based predictions")
    
    # Step 3: Train model
    if not train_initial_model():
        print("Setup failed at model training")
        print("The app will still work with rule-based predictions")
    
    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print("To run the application:")
    print("  python run.py")
    print("\nThen open your browser to: http://127.0.0.1:5000")
    print("=" * 50)

if __name__ == "__main__":
    main()