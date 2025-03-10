from functools import wraps

from flask import redirect, render_template, make_response, session, url_for

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

@app.route('/login')
def login():
    if 'user' in session:
        return render_template(url_for('dashboard')) # redirect for CPanel
    else:
        return render_template('auth/login.html') # Back to login

@app.route('/logout')
def logout():
    session.pop('user', None) # None = Privzeta vrednost če 'user' ni v session
    response = make_response(redirect(url_for('login'))) # redirecta na login
    response.set_cookie('session', '', expires=0) # uniči session


##### Private Links

## Put in auth.py
def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if 'user' not in session:
            return redirect(url_for('login'))

        else:
            return f(*args, **kwargs)

    return decorated_function
##

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

"""

@app.errorhandler(301)
def redirecting(error):
    return render_template('errors/301.html'), 301

"""