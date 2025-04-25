
from datetime import timedelta
from flaskr import app
import os
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()

# Configure session cookie settings and security
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'
app.secret_key = os.getenv("API_KEY")


# Google OAuth Credentials
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


# Firebase configuration
firebaseConfig = {
  "apiKey": f"{os.getenv('FIREBASE_API_KEY')}",
  "authDomain": "ospr-6320a.firebaseapp.com",
  "projectId": "ospr-6320a",
  "storageBucket": "ospr-6320a.firebasestorage.app",
  "messagingSenderId": f"{os.getenv('FIREBASE_SENDER_ID')}",
  "appId": f"{os.getenv('FIREBASE_APP_ID')}",
  "measurementId": f"{os.getenv('FIREBASE_MEASUREMENT_ID')}"
}
