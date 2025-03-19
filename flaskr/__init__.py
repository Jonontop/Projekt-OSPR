from datetime import timedelta

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask
from flask_socketio import SocketIO
from flaskr.models import load_server_templates

# Defining the Flask app
app = Flask(__name__)
# app.config.from_object('config.Config')

# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'
app.secret_key = "iojbgisdhjfbisdfljkhviojdbvkfdobgijhndvbiuzhbsdcv"

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
