import os

from flask import redirect, render_template, session, url_for, request, jsonify, Response, send_file
from jinja2 import TemplateNotFound

from flaskr import app, DockerManager
from flaskr.auth import Auth
from flaskr.docker import client, DockerFiles, Database, db
from flaskr.models import auth_required, load_server_templates
from werkzeug.utils import secure_filename


SERVER_TEMPLATES = load_server_templates()

"""
##### Public Links #####
"""

"""
###### Main Routes ######
"""
# Needs to be updated
@app.route('/')
def index():
    return render_template('index.html') # HomePage

@app.route('/<path:path>')
def blog(path):
    return render_template(f'blog/{path}.html') if path != 'about_service.html' else render_template('blog/about_service.html')

@app.route('/services/<name>', methods=['GET'])
def get_service(name):
    return render_template(f'blog/about_service.html', services=SERVER_TEMPLATES.get(name)) if name in SERVER_TEMPLATES else render_template('errors/404.html'), 404

@app.route('/loading')
def loading():
    return render_template('cpanel/loading.html')

"""
###### Authentication ######
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

"""
##### Private Links #####
"""
@app.route('/stream/<container_id>')
@auth_required
def stream(container_id) -> Response:
    return Response(DockerManager.stream_logs(container_id), mimetype='text/event-stream')

@app.route('/container_stats/<container_id>')
@auth_required
def container_stats(container_id) -> Response:
    return jsonify(DockerManager.container_stats(container_id))

@app.route('/account')
@auth_required
def account():
    return render_template('cpanel/account.html')

"""
##### Server Management #####
"""
# console
@app.route('/server/<container_id>/console')
@auth_required
def console(container_id):
    return render_template('cpanel/server/console.html', container_id=container_id)

# settings
@app.route('/server/<container_id>/settings')
@auth_required
def settings(container_id):
    pass

# analytics
@app.route('/server/<container_id>/analytics')
@auth_required
def analytics(container_id):
    pass

# scheduler
@app.route('/server/<container_id>/scheduler')
@auth_required
def scheduler(container_id):
    pass

# users
@app.route('/server/<container_id>/users')
@auth_required
def users(container_id):
    pass

# backup
@app.route('/server/<container_id>/backup')
@auth_required
def backup(container_id):
    pass

# edit
@app.route('/server/<container_id>/edit')
def edit(container_id):
    # Logic for handling server edit would go here
    # For now, just redirect back to dashboard
    return redirect(url_for('dashboard'))


### Files ###
# files access - dela
@app.route('/server/<container_id>/files')
@auth_required
def files(container_id):
    return render_template('cpanel/server/file_explorer.html', file_tree=DockerFiles.docker_display_files(container_id), container_id=container_id)

# files download - ne dela
@app.route('/server/<container_id>/files/download/<path:file_path>')
@auth_required
def files_download(container_id, file_path):
    return send_file(DockerFiles.docker_download_file(container_id, file_path), as_attachment=True)

# files upload - ne dela
@app.route('/server/<container_id>/files/upload', methods=['POST'])
@auth_required
def files_upload(container_id):
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    target_path = request.form.get('target_path', '')
    filename = secure_filename(file.filename)
    file.save('/tmp/' + filename)  # Temporarily save

    success = DockerFiles.docker_upload_file(container_id, '/tmp/' + filename, os.path.join(target_path, filename))
    os.remove('/tmp/' + filename)  # Clean up

    return ('', 204) if success else ('Upload failed', 500)

# files delete - ne dela
@app.route('/server/<container_id>/files/delete', methods=['POST'])
@auth_required
def files_delete(container_id):
    file_path = request.form.get('file_path')
    success = DockerFiles.docker_delete_file(container_id, file_path)
    return ('', 204) if success else ('Delete failed', 500)

# files edit - ne dela
@app.route('/server/<container_id>/files/edit', methods=['POST'])
@auth_required
def files_edit(container_id):
    file_path = request.form.get('file_path')
    new_content = request.form.get('content')
    success = DockerFiles.docker_edit_file(container_id, file_path, new_content)
    return ('', 204) if success else ('Edit failed', 500)

# files create - ne dela
@app.route('/server/<container_id>/files/create', methods=['POST'])
@auth_required
def files_create(container_id):
    pass

#### Docker ####
@app.route('/server/<container_id>/stop')
@auth_required
def stop_server(container_id):
    DockerManager.docker_stop(container_id)
    return Response(status=204)

@app.route('/server/<container_id>/start')
@auth_required
def start_server(container_id):
    DockerManager.docker_start(container_id)
    return Response(status=204)

@app.route('/server/<container_id>/restart')
@auth_required
def restart_server(container_id):
    DockerManager.docker_restart(container_id)
    return Response(status=204)

@app.route('/server/<container_id>/delete')
@auth_required
def delete_server(container_id):
    # Stop the container
    DockerManager.docker_delete(container_id)
    # Delete server from Firestore
    Database.server_delete(container_id)
    return redirect(url_for('cpanel'))



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



#### To fix / remove / transform

# modify
@app.route('/purchase/<plan>')
def purchase(plan):
    # Logic for handling purchases would go here
    # For now, just redirect back to pricing page
    return f"Processing purchase for {plan} plan..."


# Needs to be fixed
@app.route('/create_server', methods=['GET', 'POST'])
@auth_required
def create_server():
    locations = ["Slovenija, Ljubljana"]
    if not request.method == 'POST':
        return render_template('cpanel/create_server.html', nests=SERVER_TEMPLATES, locations=locations)


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

        return redirect(url_for('loading'))
        #return render_template('cpanel/server/server_details.html', server=DockerManager.container, template=SERVER_TEMPLATES.get(server_nest, {}))
    except Exception as e:
        return jsonify({'success': False, 'error': f"{e} - {type(e)}"})


@app.route('/get_eggs/<nest>')
def get_eggs(nest):
    return jsonify(SERVER_TEMPLATES.get(nest, {}).get("eggs", {}))

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


@app.route('/dashboard')
@auth_required
def cpanel():
    # Get user's servers

    user_id = session['user_id']
    server_refs = db.collection('servers').where('user_id', '==', user_id).stream()
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