import json
import os
import time
from functools import wraps

from firebase_admin import auth
from flask import redirect, session, url_for, flash, jsonify


## Needs Testing
# Load server templates from JSON file
def load_server_templates():
    try:
        with open('flaskr/templates.json', 'r') as file:
            print("Templates loaded")
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading server templates: {e}")
        return {}


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
            flash(f'Login failed!: {str(e)}', 'error')
            return redirect(url_for('login'))
    return decorated_function

# Verify Token
def TokenVerify(id_token):
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        # Store user ID in session
        session['user_id'] = user_id
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def create_server_instance(server_id, server_type, config):
    pass

## Needs Testing
# Helper function to simulate server creation
"""def create_server_instance(server_id, server_type, config):
    # In a real application, this would actually create the server
    # This is just a simulation for the example

    template = SERVER_TEMPLATES.get(server_type)
    if not template:
        db.collection('servers').document(server_id).update({
            'status': 'error',
            'error_message': 'Invalid server type'
        })
        return

    # Create server directory
    server_dir = os.path.join(template['base_folder'], server_id)
    os.makedirs(server_dir, exist_ok=True)

    # Generate configuration files
    for config_file in template['config_files']:
        with open(os.path.join(server_dir, config_file), 'w') as f:
            f.write(f"# Configuration for {config['name']}\n")
            f.write(f"# Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

            # Add specific configuration based on server type
            if server_type == 'minecraft':
                if config_file == 'server.properties':
                    f.write(f"server-port={config['port']}\n")
                    f.write(f"max-memory={config['ram']}M\n")
                    f.write("gamemode=survival\n")
                elif config_file == 'eula.txt':
                    f.write("eula=true\n")
            elif server_type == 'vps_ubuntu':
                if config_file == 'network.conf':
                    f.write(f"SSH_PORT={config['port']}\n")
                    f.write("NETWORK_MODE=bridge\n")
                elif config_file == 'user_data.yml':
                    f.write("hostname: ubuntu-vps\n")
                    f.write(f"memory: {config['ram']}M\n")
            elif server_type == 'game_server_cs2':
                if config_file == 'server.cfg':
                    f.write(f"hostport {config['port']}\n")
                    f.write("hostname \"CS2 Server\"\n")
                    f.write("sv_password \"\"\n")
                elif config_file == 'gamemode.cfg':
                    f.write("game_type 0\n")
                    f.write("game_mode 1\n")
                elif config_file == 'admins.cfg':
                    f.write("// Add admin Steam IDs here\n")
            elif server_type == 'web_server':
                if config_file == 'nginx.conf':
                    f.write(
                        f"server {{\n  listen {config['port']};\n  root /var/www/html;\n  index index.html index.php;\n}}\n")
                elif config_file == 'php.ini':
                    f.write("memory_limit = 128M\n")
                    f.write("upload_max_filesize = 2M\n")

    # Update server status in Firestore
    time.sleep(5)  # Simulate creation time
    db.collection('servers').document(server_id).update({
        'status': 'stopped',
        'ready': True
    })"""