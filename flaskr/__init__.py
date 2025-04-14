

from flask import Flask
from flask_socketio import SocketIO
from flaskr.models import load_server_templates
from flaskr.docker import DockerManager


# Defining the Flask app
app = Flask(__name__)
app.config.from_object('config')
socketio = SocketIO(app)


# Defining the SQLAlchemy database object
# db = SQLAlchemy(app) # data stealing

# Docker
DockerManager = DockerManager()



from flaskr import routes
