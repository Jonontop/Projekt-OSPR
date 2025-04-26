from firebase_admin import auth
from flask import jsonify, redirect, url_for, session, make_response
from flaskr.docker import db


# Full Authentication Module in Class

class Auth:
    def __init__(self):
        pass

    @staticmethod
    def register(id_token: str, username: str, mail: str):
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token, clock_skew_seconds=60) # Bug fix
            user_id = decoded_token['uid']

            # Store user data in your database (e.g., Firestore or Realtime Database)
            db.collection('users').document(user_id).set({
                'username': username,
                'mail': mail,
                'credits': 100
            })

            return jsonify({'success': True})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def logout(session):
        session.pop('user', None)  # None = Privzeta vrednost če 'user' ni v session
        response = make_response(redirect(url_for('login')))  # redirecta na login
        response.set_cookie('session', '', expires=0)  # uniči session
        return response

    # Verify Token
    @staticmethod
    def TokenVerify(id_token: str) -> jsonify:
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            user_id = decoded_token['uid']
            # Store user ID in session
            session['user_id'] = user_id
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
