from flask import Flask
from flask_socketio import SocketIO, emit

# Defining the Flask app
app = Flask(__name__)
#app.config.from_object('config.Config')

# Defining the SQLAlchemy database object
#db = SQLAlchemy(app)

# Define SocketIO object
socketio = SocketIO(app)

from flaskr import routes, models