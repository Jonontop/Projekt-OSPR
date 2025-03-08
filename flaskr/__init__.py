from flask import Flask
from flask_socketio import SocketIO, emit
import secrets
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import timedelta
import os

# Defining the Flask app
app = Flask(__name__)
#app.config.from_object('config.Config')

# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'

# Defining the SQLAlchemy database object
#db = SQLAlchemy(app)

# Define SocketIO object
socketio = SocketIO(app)

# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if 'user' not in session:
            return redirect(url_for('login'))
        
        else:
            return f(*args, **kwargs)
        
    return decorated_function

from flaskr import routes, models