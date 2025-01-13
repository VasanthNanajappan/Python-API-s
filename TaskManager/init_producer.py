from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Configure app (add your configurations here)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['BROKER_URL'] = 'redis://localhost:6379/0'
