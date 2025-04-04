import json
import time

from flask import redirect, render_template, session, url_for, request, jsonify, Response
from jinja2 import TemplateNotFound

from flaskr import db, app, DockerManager
from flaskr.auth import Auth
from flaskr.models import TokenVerify, auth_required, load_server_templates
from flaskr.docker import client
from flaskr.database import Database

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
    return render_template('blog/about_service.html')

# modify
@app.route('/purchase/<plan>')
def purchase(plan):
    # Logic for handling purchases would go here
    # For now, just redirect back to pricing page
    return f"Processing purchase for {plan} plan..."


"""
Services
"""
@app.route('/services/<name>', methods=['GET'])
def get_service(name):
    if name in SERVER_TEMPLATES:
        return render_template(f'blog/about_service.html', services=SERVER_TEMPLATES.get(name))  # Render corresponding HTML file
    return render_template('errors/404.html'), 404  # Render 404 page if service not found


"""
Authentication
"""
@app.route('/register', methods=['GET', 'POST'])
def register() -> str:
    return Auth.register(request.json.get('idToken'), request.json.get('username'), request.json.get('email'))

@app.route('/login', methods=['GET', 'POST'])
def login() -> str:
    return render_template('auth/login.html')

@app.route('/logout')
def logout() -> str:
    return Auth.logout(session)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password() -> str:
    return render_template('auth/forgot_password.html')


##### Private Links

@app.route('/dashboard')
@auth_required
def cpanel():
    # Get user's servers

    user_id = session['user_id']
    server_refs = db.collection('servers').where('user_id', '==', user_id).stream()
    server_loc = db.collection('servers').stream()
    user_data = db.collection('users').document(user_id).get().to_dict()


    servers = []
    for server_ref in server_refs:
        server_data = server_ref.to_dict()
        container = client.containers.get(server_data['container_id']) if server_data['container_id'] else None
        server_data['id'] = server_ref.id
        server_data['status'] = container.status if container else 'stopped'
        servers.append(server_data)

    user = {
        'username': user_data['username'],
        'mail': user_data['mail'],
        'credits': user_data['credits']
    }




    return render_template('cpanel/cpanel.html', servers=servers, templates=SERVER_TEMPLATES, user=user)

# Needs to be fixed
@app.route('/create_server', methods=['GET', 'POST'])
@auth_required
def create_server():
    locations = ["Slovenija, Ljubljana"]
    if not request.method == 'POST':
        return render_template('cpanel/create_server.html', nests=SERVER_TEMPLATES, locations=locations)


    # Get the necessary data (e.g., server name, game type) from the request
    # General
    server_name, server_description = request.form.get('server_name'), request.form.get('server_description')
    # Resources
    server_cpu, server_ram, server_storage = request.form.get('server_cpu'), request.form.get('server_ram'), request.form.get('server_storage')
    # Ports
    server_ports, server_databases, server_backup = request.form.get('server_ports'), request.form.get('server_databases'), request.form.get('server_backup')
    # Location
    server_location, server_nest, server_egg = request.form.get('server_location'), request.form.get('server_nest'), request.form.get('server_egg')

    try:
        # create server in docker
        DockerManager.docker_create(server_name, server_cpu, server_storage, server_ram, server_nest, server_egg)

        # create server in database
        Database.server_create(server_name, server_description, server_cpu, server_ram, server_storage, server_ports, server_databases, server_backup, server_location, server_nest, server_egg)


        return render_template('cpanel/server_details.html', server=DockerManager.container, template=SERVER_TEMPLATES.get(server_nest, {}))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_eggs/<nest>')
def get_eggs(nest):
    eggs = SERVER_TEMPLATES.get(nest, {}).get("eggs", {})
    return jsonify(eggs)

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



def stream_logs(container_id):
    try:
        container = client.containers.get(container_id)
        for line in container.logs(stream=True):
            yield f"data: {line.decode('utf-8')}\n\n"
    except Exception as e:
        yield f"data: Error: {str(e)}\n\n"

@app.route('/stream/<container_id>')
def stream(container_id) -> Response:
    return Response(stream_logs(container_id), mimetype='text/event-stream')


@app.route('/console/<container_id>')
def console(container_id):
    return render_template('cpanel/console.html', container_id=container_id)

##### Errors

@app.errorhandler(404)
@app.errorhandler(TemplateNotFound)
def page_not_found(error):
    return render_template('errors.html', error=404), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors.html', error=500), 500


##### Config

# Verify ID Token Endpoint
@app.route('/verify_token', methods=['POST'])
def verify_token():
    return Auth.TokenVerify(request.json.get('idToken'))
