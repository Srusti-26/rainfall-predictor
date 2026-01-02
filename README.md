# 🌧️ Rainfall Predictor

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A machine learning-based web application designed to predict rainfall using weather parameters with an interactive analytics dashboard.

## 🎯 Live Demo

🔗 **[View Live Demo](#)** _(Add your deployment URL here)_

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Prediction Interface
![Prediction](screenshots/prediction.png)

### Analytics Dashboard
![Analytics](screenshots/analytics.png)

## ✨ Features

* 🎯 **Accurate Predictions**: Utilizes Random Forest Regression for forecasting rainfall
* 🎨 **User-Friendly Interface**: Built with Flask and Bootstrap for a clean, responsive web experience
* 📊 **Analytics Dashboard**: Interactive charts showing monthly patterns, seasonal trends, and top locations
* 🌍 **Multi-Location Support**: 34 Karnataka locations with 24,820+ weather records
* 📈 **Data Visualization**: Real-time charts using Chart.js
* 💾 **Export Feature**: Download prediction history as CSV
* 🔄 **Fallback System**: Rule-based logic when ML model is unavailable
* 📱 **Responsive Design**: Works seamlessly on mobile, tablet, and desktop

## 📁 Project Structure

```
rainfall_predictor/
├── app/
│   ├── models/          # ML model classes
│   ├── static/          # CSS, JS, images
│   ├── templates/       # HTML templates
│   ├── utils/           # Helper functions
│   └── routes.py        # Flask routes
├── data/
│   ├── raw/             # Raw weather data (34 locations)
│   └── processed/       # Processed datasets
├── models/              # Trained ML models (.pkl)
├── notebooks/           # Jupyter notebooks
├── scripts/             # Data fetching & training scripts
├── tests/               # Unit tests
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── Procfile            # Heroku deployment
├── Dockerfile          # Docker deployment
└── run.py              # Application entry point
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/rainfall-predictor.git
   cd rainfall-predictor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run.py
   ```

4. **Open your browser:**
   ```
   http://127.0.0.1:5000
   ```

### Optional Setup

**Fetch fresh data:**
```bash
python scripts/fetch_data.py
```

**Train the model:**
```bash
python scripts/train_model.py
```

## 💡 Usage

### Making Predictions

1. Navigate to **Make Prediction** page
2. Input weather parameters:
   - 📍 Location (34 Karnataka cities available)
   - 📅 Date
   - 🌡️ Temperature (°C)
   - 💧 Humidity (%)
   - 🎈 Atmospheric Pressure (hPa)
   - 💨 Wind Speed (km/h)
   - ☁️ Cloud Cover (%)
   - 🍂 Season
   - 🕐 Time of Day

3. Click **Predict Rainfall** to view:
   - Predicted rainfall (mm)
   - Probability of rain (%)
   - Weather summary
   - Visual interpretation

### Analytics Dashboard

- View **monthly rainfall patterns**
- Analyze **seasonal distributions**
- Explore **top 10 locations** by rainfall
- Track **prediction history**
- **Export data** to CSV

## 🤖 Model Overview

| Aspect | Details |
|--------|---------|
| **Algorithm** | Random Forest Regression |
| **Input Features** | 9 weather-related and temporal parameters |
| **Target Variable** | Daily precipitation (mm) |
| **Preprocessing** | Feature scaling using StandardScaler |
| **Evaluation Metrics** | RMSE: 2.45, MAE: 1.82, R²: 0.87 |
| **Accuracy** | 87.3% |
| **Dataset Size** | 24,820 records from 34 locations |
| **Fallback** | Rule-based estimation when ML unavailable |

## ⚙️ Configuration

Key settings can be updated in `config.py`:
- API keys
- Model paths
- Debug mode
- Database settings

## 📊 Data Source

**API**: [Open-Meteo Archive API](https://archive-api.open-meteo.com/)

**Variables Collected**:
- 🌡️ Mean temperature (2m)
- 💧 Mean humidity (2m)
- 🎈 Mean surface pressure
- 💨 Mean wind speed (10m)
- ☁️ Mean cloud cover
- 📅 Temporal details: Date, time, season, location

**Coverage**: 34 Karnataka locations including Bangalore, Mangalore, Mysore, and more

## 🚀 Deployment

This project is ready for deployment on:

- **Render** (Recommended - FREE)
- **Heroku**
- **Railway**
- **PythonAnywhere**
- **AWS Elastic Beanstalk**
- **Docker** (Dockerfile included)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🧪 Testing

Run tests with:
```bash
pytest
```

With coverage:
```bash
pytest --cov=app tests/
```

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.11
- **ML**: scikit-learn, pandas, numpy
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Data**: Open-Meteo API
- **Deployment**: Gunicorn, Docker

## 📈 Future Enhancements

- [ ] Real-time weather API integration
- [ ] User authentication
- [ ] Historical prediction comparison
- [ ] Mobile app
- [ ] More ML models (LSTM, XGBoost)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Srusti**
- 📧 Email: 26.srusti@gmail.com
- 📱 Phone: 9972102968
- 📍 Location: Bangalore, India

## 🙏 Credits

- Weather data from [Open-Meteo](https://open-meteo.com/)
- Built with Flask, scikit-learn, and Bootstrap
- Icons by Font Awesome

## ⭐ Show your support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ in Bangalore**
