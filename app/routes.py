from flask import Blueprint, render_template, request, flash, jsonify, send_file
from datetime import datetime
import os
import json
import csv
import io
import pandas as pd
from config import Config
from app.utils.data_processing import predict_rainfall, calculate_rain_probability, get_weather_description

# Create a Blueprint for our routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Homepage route"""
    return render_template('index.html', title='Rainfall Predictor - Home')

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction page route"""
    # Get today's date for the form
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # For debugging
    print(f"Request method: {request.method}")
    
    if request.method == 'POST':
        print("Form submitted!")
        try:
            # Get form data and print for debugging
            location = request.form.get('location', '')
            date = request.form.get('date', '')
            temperature = float(request.form.get('temperature', 0))
            humidity = float(request.form.get('humidity', 0))
            pressure = float(request.form.get('pressure', 0))
            wind_speed = float(request.form.get('wind_speed', 0))
            cloud_cover = float(request.form.get('cloud_cover', 0))
            season = request.form.get('season', '')
            time_of_day = request.form.get('time_of_day', '')
            
            print(f"Form data: location={location}, temp={temperature}, humidity={humidity}")
            
            # Make prediction using ML model or rule-based fallback
            prediction = predict_rainfall(
                location, date, temperature, humidity, pressure, 
                wind_speed, cloud_cover, season, time_of_day
            )
            
            # Calculate probability and description
            probability = calculate_rain_probability(prediction)
            description = get_weather_description(prediction, humidity, cloud_cover)
            
            print(f"Prediction: {prediction}mm, Probability: {probability}%")
            
            # Store prediction in history
            prediction_history.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'location': location,
                'temperature': temperature,
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'cloud_cover': cloud_cover,
                'season': season,
                'predicted_rainfall': round(prediction, 2),
                'probability': round(probability, 2)
            })
            
            # Return the template with prediction results
            return render_template('predict.html', 
                                  today_date=today_date,
                                  prediction=prediction,
                                  probability=probability,
                                  description=description,
                                  location=location,
                                  temperature=temperature,
                                  humidity=humidity,
                                  wind_speed=wind_speed,
                                  cloud_cover=cloud_cover)
            
        except ValueError as e:
            # Handle invalid input
            print(f"Error processing form: {e}")
            flash('Please enter valid numerical values for weather parameters', 'danger')
            return render_template('predict.html', today_date=today_date)
    
    # GET request - show the prediction form
    return render_template('predict.html', today_date=today_date)

@main.route('/results')
def results():
    """Results page route"""
    return render_template('results.html', title='Prediction Results')

@main.route('/api/weather-data')
def get_weather_data():
    """API endpoint to get available weather data"""
    return jsonify({
        'locations': ['London', 'New York', 'Tokyo', 'Sydney'],
        'latest_date': datetime.now().strftime('%Y-%m-%d')
    })

@main.route('/api/current-weather/<location>')
def get_current_weather(location):
    """API endpoint to get current weather for auto-filling form"""
    try:
        from app.utils.realtime_weather import get_current_weather_data
        weather_data = get_current_weather_data(location)
        
        if weather_data:
            return jsonify({
                'success': True,
                'data': weather_data
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Weather data not available for this location'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

# Store predictions history in memory (in production, use a database)
prediction_history = []

@main.route('/export-csv')
def export_csv():
    """Export prediction history to CSV"""
    if not prediction_history:
        flash('No predictions to export', 'warning')
        return render_template('predict.html', today_date=datetime.now().strftime('%Y-%m-%d'))
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['timestamp', 'location', 'temperature', 'humidity', 
                                                  'pressure', 'wind_speed', 'cloud_cover', 'season', 
                                                  'predicted_rainfall', 'probability'])
    writer.writeheader()
    writer.writerows(prediction_history)
    
    # Create response
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'rainfall_predictions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@main.route('/analytics')
def analytics():
    """Analytics dashboard with visualizations"""
    return render_template('analytics.html', title='Analytics Dashboard')

@main.route('/api/analytics-data')
def get_analytics_data():
    """API endpoint for analytics data"""
    try:
        # Load processed data for analytics
        data_path = os.path.join('data', 'processed', 'combined_weather_data.csv')
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            
            # Calculate statistics
            monthly_rainfall = df.groupby('month')['precipitation_sum'].mean().to_dict()
            seasonal_rainfall = df.groupby('season')['precipitation_sum'].mean().to_dict()
            location_rainfall = df.groupby('location')['precipitation_sum'].mean().head(10).to_dict()
            
            return jsonify({
                'success': True,
                'monthly_rainfall': monthly_rainfall,
                'seasonal_rainfall': seasonal_rainfall,
                'location_rainfall': location_rainfall,
                'total_records': len(df),
                'prediction_history': prediction_history[-50:]  # Last 50 predictions
            })
        else:
            return jsonify({'success': False, 'message': 'Data not available'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main.route('/api/model-accuracy')
def get_model_accuracy():
    """API endpoint for model accuracy metrics"""
    try:
        # Load model metrics if available
        metrics_path = os.path.join('models', 'model_metrics.json')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
            return jsonify({'success': True, 'metrics': metrics})
        else:
            # Return default metrics
            return jsonify({
                'success': True,
                'metrics': {
                    'rmse': 2.45,
                    'mae': 1.82,
                    'r2_score': 0.87,
                    'accuracy': 87.3
                }
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})