from functools import wraps

from firebase_admin import auth
from flask import redirect, render_template, make_response, session, url_for, request, flash

from flaskr import app


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

@app.route('/support')
def support():
    return render_template('blog/support.html')

@app.route('/services')
def services():
    return render_template('blog/services.html') # needs to be added

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  # Get username from form
        password = request.form.get('password')  # Get password from form

        try:
            # Authenticate user with Firebase
            user = auth.get_user_by_email(username)  # Firebase uses email as username
            # Note: Firebase doesn't store plaintext passwords, so you'll need to use Firebase Auth for password verification
            # For now, we'll assume authentication is successful
            session['user'] = user.uid  # Store user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        except Exception as e:
            flash('Login failed. Please check your credentials.', 'danger')
            return redirect(url_for('login'))

        return render_template('login.html')

    if 'user' in session:
        return render_template(url_for('dashboard')) # redirect for CPanel
    else:
        return render_template('auth/login.html') # Back to login


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')  # Get email from form
        password = request.form.get('password')  # Get password from form
        username = request.form.get('username')  # Get username from form

        try:
            # Create user with Firebase
            user = auth.create_user(
                email=email,
                password=password,
                display_name=username  # Optional: Store username as display name
            )
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))  # Redirect to login page after registration
        except Exception as e:
            flash('Registration failed. Please try again.', 'danger')
            return redirect(url_for('register'))

    return render_template('login.html')  # Render the same login.html since it contains the register form

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
        # Check if user is authenticated
        if 'user' not in session:
            return redirect(url_for('login'))

        else:
            return f(*args, **kwargs)

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
