import numpy as np
import joblib
import os
import sys
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

# Initialize model and preprocessing components for the rainfall predictor
print("Initializing rainfall prediction model...")

# Create initial model with sample data
model = RandomForestRegressor(n_estimators=10, random_state=42)
X_sample = np.random.rand(100, 9)  # 9 features: temp, humidity, pressure, wind, cloud, month, day, location, season
y_sample = np.random.rand(100) * 20  # rainfall 0-20mm
model.fit(X_sample, y_sample)

# Create feature scaler
scaler = StandardScaler()
scaler.fit(X_sample)

# Create label encoders
location_encoder = LabelEncoder()
location_encoder.fit(['london', 'new york', 'tokyo', 'sydney'])

season_encoder = LabelEncoder()
season_encoder.fit(['spring', 'summer', 'autumn', 'winter', 'monsoon', 'pre-monsoon', 'post-monsoon'])

# Save all components
os.makedirs(Config.MODEL_DIR, exist_ok=True)
joblib.dump(model, os.path.join(Config.MODEL_DIR, 'rainfall_model.pkl'))
joblib.dump(scaler, os.path.join(Config.MODEL_DIR, 'scaler.pkl'))
joblib.dump(location_encoder, os.path.join(Config.MODEL_DIR, 'location_encoder.pkl'))
joblib.dump(season_encoder, os.path.join(Config.MODEL_DIR, 'season_encoder.pkl'))

print("Model initialization completed successfully!")
print("You can now run the app with: python run.py")