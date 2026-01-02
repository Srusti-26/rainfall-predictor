import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def load_and_prepare_data():
    """Load and prepare data for training"""
    
    # Load all CSV files from raw data directory
    data_files = []
    for filename in os.listdir(Config.RAW_DATA_DIR):
        if filename.endswith('.csv'):
            filepath = os.path.join(Config.RAW_DATA_DIR, filename)
            df = pd.read_csv(filepath)
            data_files.append(df)
    
    if not data_files:
        print("No data files found. Please run fetch_data.py first.")
        return None, None
    
    # Combine all data
    df = pd.concat(data_files, ignore_index=True)
    
    # Handle missing values
    df = df.dropna()
    
    # Encode categorical variables
    le_location = LabelEncoder()
    le_season = LabelEncoder()
    
    df['location_encoded'] = le_location.fit_transform(df['location'])
    df['season_encoded'] = le_season.fit_transform(df['season'])
    
    # Select features
    feature_columns = [
        'temperature_2m_mean', 'relative_humidity_2m_mean', 'surface_pressure_mean',
        'wind_speed_10m_mean', 'cloud_cover_mean', 'month', 'day',
        'location_encoded', 'season_encoded'
    ]
    
    X = df[feature_columns]
    y = df[Config.TARGET_VARIABLE]
    
    # Save encoders
    joblib.dump(le_location, os.path.join(Config.MODEL_DIR, 'location_encoder.pkl'))
    joblib.dump(le_season, os.path.join(Config.MODEL_DIR, 'season_encoder.pkl'))
    
    print(f"Dataset shape: {X.shape}")
    print(f"Features: {feature_columns}")
    
    return X, y

def train_model():
    """Train the rainfall prediction model"""
    
    # Load and prepare data
    X, y = load_and_prepare_data()
    if X is None:
        return
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=Config.TEST_SIZE, random_state=Config.RANDOM_STATE
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    print("Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=Config.RANDOM_STATE,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    
    # Evaluate model
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"R² Score: {r2:.3f}")
    
    # Feature importance
    feature_names = [
        'Temperature', 'Humidity', 'Pressure', 'Wind Speed', 'Cloud Cover',
        'Month', 'Day', 'Location', 'Season'
    ]
    
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nFeature Importance:")
    print(importance_df)
    
    # Save model and scaler
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(Config.MODEL_DIR, 'rainfall_model.pkl'))
    joblib.dump(scaler, os.path.join(Config.MODEL_DIR, 'scaler.pkl'))
    
    print(f"\nModel saved to {Config.MODEL_DIR}")
    
    return model, scaler

if __name__ == "__main__":
    train_model()