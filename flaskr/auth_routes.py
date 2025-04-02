from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from . import auth  # Import your auth module

# Create a blueprint for authentication routes
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')
    return "", 200  # Empty response for POST as it's handled by client-side JS


@bp.route('/register', methods=('POST',))
def register():
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        id_token = data.get('idToken')
        username = data.get('username')
        email = data.get('email')

        if not id_token or not username or not email:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        success, message = auth.register_firebase_user(id_token, username, email)

        return jsonify({"success": success, "message": message})

    return jsonify({"success": False, "message": "Method not allowed"}), 405


@bp.route('/verify_token', methods=('POST',))
def verify_token():
    data = request.json
    if not data or 'idToken' not in data:
        return jsonify({"success": False, "message": "No token provided"}), 400

    id_token = data['idToken']
    success, user_data = auth.verify_firebase_token(id_token)

    if success:
        # Store user info in session
        session['user_id'] = user_data.get('username')
        session['email'] = user_data.get('email')
        return jsonify({"success": True, "message": "Token verified", "user": user_data})
    else:
        return jsonify({"success": False, "message": user_data})


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


# Add this to your main app.py or __init__.py
def register_blueprints(app):
    from . import auth_routes
    app.register_blueprint(auth_routes.bp)
