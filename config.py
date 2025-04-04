
from datetime import timedelta
from flaskr import app

# Configure session cookie settings and security
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'
app.secret_key = "iojbgisdhjfbisdfljkhviojdbvkfdobgijhndvbiuzhbsdcv"


# Google OAuth Credentials
GOOGLE_CLIENT_ID = "895371472700-so2hqv67c4fvipff2f8r4strcrmmg1ao.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"


# Firebase configuration
firebaseConfig = {
  "apiKey": "AIzaSyAjuk6RqUEDLReXaW1vNryZdR2BDRXydKs",
  "authDomain": "ospr-6320a.firebaseapp.com",
  "projectId": "ospr-6320a",
  "storageBucket": "ospr-6320a.firebasestorage.app",
  "messagingSenderId": "929635361328",
  "appId": "1:929635361328:web:752e995da1ccdfe8bf83f5",
  "measurementId": "G-GLB8DD7GTC"
}
