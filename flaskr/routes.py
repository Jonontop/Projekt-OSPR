from functools import wraps

from firebase_admin import auth
from flask import redirect, render_template, make_response, session, url_for, request, flash, jsonify

from flaskr import app, socketio
from flaskr import get_firestore_client


db = get_firestore_client()

##### Public Links

@app.route('/')
def index():
    return render_template('index.html') # HomePage

@app.route('/about')
def about():
    return render_template('blog/about.html') # About Us

@app.route('/terms')
def terms():
    return render_template('blog/terms.html') # needs to be added

@app.route('/privacy')
def privacy():
    return render_template('blog/privacy.html') # needs to be added

@app.route('/plans')
def plans():
    return render_template('blog/plans.html') # needs to be added

@app.route('/support')
def support():
    return render_template('blog/support.html')

@app.route('/services')
def services():
    return render_template('blog/services.html') # needs to be added

@app.route('/purchase/<plan>')
def purchase(plan):
    # Logic for handling purchases would go here
    # For now, just redirect back to pricing page
    return f"Processing purchase for {plan} plan..."

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    id_token = request.json.get('idToken')
    username = request.json.get('username')

    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']

        # Store user data in your database (e.g., Firestore or Realtime Database)
        # Example: db.collection('users').document(user_id).set({'username': username})

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/logout')
def logout():
    session.pop('user', None) # None = Privzeta vrednost če 'user' ni v session
    response = make_response(redirect(url_for('login'))) # redirecta na login
    response.set_cookie('session', '', expires=0) # uniči session
    return response


##### Private Links

# Decorator to require authentication
def auth_required(f):
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
            flash(f'Login failed: {str(e)}', 'error')
            return redirect(url_for('login'))
    return decorated_function

@app.route('/dashboard')
@auth_required
def cpanel():
    return render_template('cpanel/cpanel.html') # CPanel


##### Errors

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500


##### Config

# Verify ID Token Endpoint
@app.route('/verify_token', methods=['POST'])
def verify_token():
    id_token = request.json.get('idToken')
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        # Store user ID in session
        session['user_id'] = user_id
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@socketio.on()