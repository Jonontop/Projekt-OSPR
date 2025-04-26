import json
from functools import wraps

import requests
from firebase_admin import auth
from flask import redirect, session, url_for, flash, jsonify


# Load server templates from JSON file
def load_server_templates() -> dict:
    try:
        with open('flaskr/templates.json', 'r') as file:
            #print("Templates loaded")
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading server templates: {e}")
        return {}

# Decorator to require authentication
def auth_required(f:callable) -> callable:
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in (e.g., via session or token)
        if 'user_id' not in session:
            flash('Login failed!', 'error')
            return redirect(url_for('login'))

        try:
            # Verify the user exists in Firebase Authentication
            user = auth.get_user(session['user_id'])
            return f(*args, **kwargs)
        except auth.UserNotFoundError:
            flash('Login failed! User not found.', 'error')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Login failed!: {str(e)}', 'error')
            return redirect(url_for('login'))
    return decorated_function

# Verify Token
def TokenVerify(id_token:str) -> jsonify:
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        # Store user ID in session
        session['user_id'] = user_id
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# Testing webhook for future use
def Webhook(webhook_url, message, username):
    data = {
        "content": f"{message}",
        "username": f"{username}",
    }

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        return True
    else:
        return False

