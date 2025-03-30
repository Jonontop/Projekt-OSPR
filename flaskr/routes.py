from functools import wraps
import firebase_admin
from firebase_admin import auth, firestore, credentials
from flask import redirect, render_template, make_response, session, url_for, request, flash, jsonify
from flask_socketio import emit
from flaskr import get_firestore_client, app, socketio
from flaskr.models import TokenVerify, load_server_templates, create_server_instance, auth_required, load_server_templates
import subprocess
import uuid
import json
import time
import os


db = get_firestore_client()

SERVER_TEMPLATES = load_server_templates()

##### Public Links

"""
Main Page
"""
# Needs to be updated
@app.route('/')
def index():
    return render_template('index.html') # HomePage


"""
All routes in /Blog/
"""
@app.route('/<path:path>')
def blog(path):
    if path != 'about_service.html':
        return render_template(f'blog/{path}.html') # needs to be added
    else:
        return render_template('blog/about_service.html')


"""
Plans
"""
@app.route('/plans')
def plans():
    return render_template('blog/plans.html') # needs to be added


@app.route('/purchase/<plan>')
def purchase(plan):
    # Logic for handling purchases would go here
    # For now, just redirect back to pricing page
    return f"Processing purchase for {plan} plan..."


"""
Services
"""

# Example services data
# Load services from JSON file
def load_services():
    with open('flaskr/templates.json') as f:
        return json.load(f)


@app.route('/services/<name>', methods=['GET'])
def get_service(name):
    services = load_services()
    service = services.get(name)

    if name in services:
        return render_template(f'blog/about_service.html', services=service)  # Render corresponding HTML file
    else:
        return render_template('errors/404.html'), 404  # Render 404 page if service not found


"""
Authentication
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    id_token = request.json.get('idToken')
    # username = request.json.get('username')

    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']

        # Store user data in your database (e.g., Firestore or Realtime Database)
        # Example: db.collection('users').document(user_id).set({'username': username})

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.pop('user', None) # None = Privzeta vrednost če 'user' ni v session
    response = make_response(redirect(url_for('login'))) # redirecta na login
    response.set_cookie('session', '', expires=0) # uniči session
    return response


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('auth/forgot_password.html')


##### Private Links

@app.route('/dashboard')
@auth_required
def cpanel():
    # Get user's servers
    user_id = session['user_id']
    server_refs = db.collection('servers').where('user_id', '==', user_id).stream()

    servers = []
    for server_ref in server_refs:
        server_data = server_ref.to_dict()
        server_data['id'] = server_ref.id
        servers.append(server_data)

    return render_template('cpanel/cpanel.html', servers=servers, templates=SERVER_TEMPLATES)

# Needs to be fixed
@app.route('/create_server', methods=['GET', 'POST'])
@auth_required
def create_server():
    if request.method == 'POST':
        user_id = session['user_id']
        server_type = request.form.get('server_type')
        # print(user_id, server_type) # Testing

        # Validate server type exists in templates
        if server_type not in SERVER_TEMPLATES:
            return render_template('create_server.html',
                                   templates=SERVER_TEMPLATES,
                                   error="Invalid server type selected")

        server_name = request.form.get('server_name')
        ram = int(request.form.get('ram', SERVER_TEMPLATES[server_type]['ram_default']))
        port = int(request.form.get('port', SERVER_TEMPLATES[server_type]['port_default']))

        # Generate a unique server ID
        server_id = str(uuid.uuid4())

        # Create server configuration
        server_config = {
            'id': server_id,
            'type': server_type,
            'name': server_name,
            'user_id': user_id,
            'ram': ram,
            'port': port,
            'status': 'creating',
            'created_at': firestore.SERVER_TIMESTAMP,
            'ip_address': '127.0.0.1',  # This would be assigned dynamically in production
        }

        # Save to Firebase
        db.collection('servers').document(server_id).set(server_config)

        # Queue server creation task (in a real app, this would be handled by a background worker)
        # For demo, we'll just simulate the server creation
        create_server_instance(server_id, server_type, server_config)

        return redirect(url_for('server_details', server_id=server_id))

    # Get the server type from query parameter if provided
    server_type = request.args.get('type')
    if server_type and server_type not in SERVER_TEMPLATES:
        server_type = next(iter(SERVER_TEMPLATES), None)  # Default to first template

    return render_template('cpanel/create_server.html', templates=SERVER_TEMPLATES, default_type=server_type)

# Needs to be fixed
@app.route('/server/<server_id>')
@auth_required
def server_details(server_id):
    user_id = session['user_id']

    # Get server details
    server_ref = db.collection('servers').document(server_id)
    server = server_ref.get()

    if not server.exists or server.to_dict()['user_id'] != user_id:
        return redirect(url_for('dashboard'))

    server_data = server.to_dict()

    return render_template('cpanel/server_details.html', server=server_data,
                           template=SERVER_TEMPLATES.get(server_data['type'], {}))

# Needs to be fixed
@app.route('/server/<server_id>/start', methods=['POST'])
@auth_required
def start_server(server_id):
    user_id = session['user_id']

    # Get server details
    server_ref = db.collection('servers').document(server_id)
    server = server_ref.get()

    if not server.exists or server.to_dict()['user_id'] != user_id:
        return jsonify({'success': False, 'error': 'Server not found'})

    # Update server status
    server_ref.update({'status': 'starting'})

    # In a real application, you would trigger your server start script here
    server_type = server.to_dict()['type']
    template = SERVER_TEMPLATES.get(server_type, {})

    if not template:
        server_ref.update({'status': 'error', 'error_message': 'Invalid server type'})
        return jsonify({'success': False, 'error': 'Invalid server type'})

    # Simulate server startup (in a real app, this would be a background task)
    # Example: subprocess.Popen(['bash', template['startup_script'], server_id])

    # For demo, we'll just update the status after a delay
    time.sleep(2)  # Simulating server startup time
    server_ref.update({'status': 'running'})

    return jsonify({'success': True}) # Needs to be fixed

# Needs to be fixed
@app.route('/server/<server_id>/stop', methods=['POST'])
@auth_required
def stop_server(server_id):
    user_id = session['user_id']

    # Get server details
    server_ref = db.collection('servers').document(server_id)
    server = server_ref.get()

    if not server.exists or server.to_dict()['user_id'] != user_id:
        return jsonify({'success': False, 'error': 'Server not found'})

    # Update server status
    server_ref.update({'status': 'stopping'})

    # In a real application, you would trigger your server stop script here
    # Example: subprocess.Popen(['bash', 'stop_server.sh', server_id])

    # For demo, we'll just update the status after a delay
    time.sleep(2)  # Simulating server shutdown time
    server_ref.update({'status': 'stopped'})

    return jsonify({'success': True}) # Needs to be fixed

# Needs to be fixed
@app.route('/admin/templates', methods=['GET', 'POST'])
@auth_required
def manage_templates():
    # In a real app, check if user is admin
    # For demo purposes we'll skip this check

    if request.method == 'POST':
        # Update templates
        new_templates = request.json

        # Validate new templates (basic validation)
        for key, template in new_templates.items():
            required_fields = ['name', 'ram_min', 'ram_default', 'ram_max', 'port_default',
                               'startup_script', 'config_files', 'base_folder']
            for field in required_fields:
                if field not in template:
                    return jsonify({'success': False, 'error': f'Missing required field: {field} in template {key}'})

        # Save to JSON file
        with open('server_templates.json', 'w') as file:
            json.dump(new_templates, file, indent=2)

        # Reload templates
        global SERVER_TEMPLATES
        SERVER_TEMPLATES = SERVER_TEMPLATES

        return jsonify({'success': True})

    return render_template('admin_templates.html', templates=SERVER_TEMPLATES)



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
    return TokenVerify(id_token)
