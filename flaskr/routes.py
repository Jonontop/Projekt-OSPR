from flask import redirect, render_template, request, make_response, session, abort, jsonify, url_for
from flaskr import app

##### Public Links

@app.route('/')
def index():
    return render_template('index.html') # HomePage

@app.route('/about')
def about():
    return render_template('about.html') # About Us

@app.route('/terms')
def terms():
    return render_template('terms.html') # needs to be added

@app.route('/privacy')
def privacy():
    return render_template('privacy.html') # needs to be added

@app.route('/login')
def login():
    if 'user' in session:
        return render_template(url_for('dashboard')) # redirect for CPanel
    else:
        return render_template('login.html') # Back to login 

@app.route('/logout')
def logout():
    session.pop('user', None) # idk
    response = make_response(redirect(url_for('login'))) # redirecta na login
    response.set_cookie('session', '', expires=0) # uniči session


##### Private Links

@app.route('/dashboard')
@auth_required
def cpanel():
    return render_template('cpanel/cpanel.html') # CPanel


##### Errors

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404