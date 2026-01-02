import pandas as pd
import os
import sys
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def process_weather_data():
    """Process raw weather data and save to processed folder"""
    
    # Get all CSV files from raw data directory
    raw_files = [f for f in os.listdir(Config.RAW_DATA_DIR) if f.endswith('.csv')]
    
    if not raw_files:
        print("No raw data files found!")
        return
    
    all_data = []
    
    # Process each file
    for file in raw_files:
        filepath = os.path.join(Config.RAW_DATA_DIR, file)
        print(f"Processing {file}...")
        
        df = pd.read_csv(filepath)
        
        # Clean and standardize columns
        if 'time' in df.columns and 'date' not in df.columns:
            df['date'] = df['time']
        
        # Ensure required columns exist
        required_cols = ['temperature_2m_mean', 'relative_humidity_2m_mean', 
                        'surface_pressure_mean', 'wind_speed_10m_mean', 
                        'cloud_cover_mean', 'precipitation_sum']
        
        if all(col in df.columns for col in required_cols):
            all_data.append(df)
        else:
            print(f"Skipping {file} - missing required columns")
    
    if not all_data:
        print("No valid data files to process!")
        return
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Remove duplicates and handle missing values
    combined_df = combined_df.drop_duplicates()
    combined_df = combined_df.dropna()
    
    # Save combined raw data
    combined_raw_path = os.path.join(Config.PROCESSED_DATA_DIR, 'combined_weather_data.csv')
    combined_df.to_csv(combined_raw_path, index=False)
    print(f"[OK] Saved combined data: {combined_raw_path}")
    
    # Create processed features
    processed_df = combined_df.copy()
    
    # Encode categorical variables
    location_encoder = LabelEncoder()
    season_encoder = LabelEncoder()
    
    processed_df['location_encoded'] = location_encoder.fit_transform(processed_df['location'].str.lower())
    processed_df['season_encoded'] = season_encoder.fit_transform(processed_df['season'].str.lower())
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_cols = ['temperature_2m_mean', 'relative_humidity_2m_mean', 
                     'surface_pressure_mean', 'wind_speed_10m_mean', 'cloud_cover_mean']
    
    processed_df[numerical_cols] = scaler.fit_transform(processed_df[numerical_cols])
    
    # Save processed data
    processed_path = os.path.join(Config.PROCESSED_DATA_DIR, 'processed_weather_data.csv')
    processed_df.to_csv(processed_path, index=False)
    print(f"[OK] Saved processed data: {processed_path}")
    
    # Save encoders and scaler for later use
    import joblib
    joblib.dump(location_encoder, os.path.join(Config.PROCESSED_DATA_DIR, 'location_encoder.pkl'))
    joblib.dump(season_encoder, os.path.join(Config.PROCESSED_DATA_DIR, 'season_encoder.pkl'))
    joblib.dump(scaler, os.path.join(Config.PROCESSED_DATA_DIR, 'feature_scaler.pkl'))
    
    print("[OK] Data processing completed!")
    print(f"Total records: {len(processed_df)}")
    print(f"Cities: {processed_df['location'].unique()}")
    print(f"Date range: {processed_df['date'].min()} to {processed_df['date'].max()}")

if __name__ == "__main__":
    Config.create_directories()
    process_weather_data()