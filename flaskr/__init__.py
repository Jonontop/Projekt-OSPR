
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask
from flask_socketio import SocketIO
from flaskr.models import load_server_templates
from flaskr.docker import DockerManager


# Defining the Flask app
app = Flask(__name__)
app.config.from_object('config')
socketio = SocketIO(app)

# Docker
DockerManager = DockerManager()

# Defining the SQLAlchemy database object
# db = SQLAlchemy(app) # data stealing


# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


from flaskr import routes
