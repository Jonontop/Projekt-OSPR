from datetime import timedelta

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask
from flask_socketio import SocketIO
from flaskr.models import load_server_templates
import docker

# Load Docker client
client = docker.from_env()

# Defining the Flask app
app = Flask(__name__)
app.config.from_object('config')


# Defining the SQLAlchemy database object
# db = SQLAlchemy(app) # data stealing

# Define SocketIO object
socketio = SocketIO(app)

# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


## FireBase - Client Function
def get_firestore_client():
    return db

from flaskr import routes
