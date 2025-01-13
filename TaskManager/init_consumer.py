from flask import Flask

# Create a Flask instance
app = Flask(__name__)

# Load Flask configurations from config.py
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']

# Setup the Flask SocketIO integration while mapping the Redis Server.
from flask_socketio import SocketIO

socketio = SocketIO(
    app,
    logger=True,
    engineio_logger=True,
    message_queue=app.config['BROKER_URL']
)
