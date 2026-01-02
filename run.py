from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode when executed directly
    app.run(debug=app.config['DEBUG'], port=1234)
    
    # Display startup message
    print(f"Rainfall Predictor is running at http://127.0.0.1:1234")