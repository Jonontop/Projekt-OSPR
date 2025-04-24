import os

import docker
from flask import jsonify
import traceback
from flaskr.models import load_server_templates
from flask import session
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# Load Docker client
try:
    REMOTE_DOCKER_HOST = 'tcp://local.jonpecar.xyz:2375'
    client = docker.DockerClient(base_url=REMOTE_DOCKER_HOST)
    print("Connected to remote Docker host")
except Exception as e:
    client = docker.from_env()
    print("Connected to local Docker host")


class DockerManager:

    def __init__(self):
        self.__server_templates = load_server_templates()
        self.container = None

    def docker_create(self, server_name, server_cpu, server_storage, server_ram, server_nest, server_egg) -> any:

        docker_image = self.__server_templates[server_nest]['eggs'][server_egg]['docker_image']
        port = self.__server_templates[server_nest]['port_default']
        storage = server_storage if server_storage is not None else 100  # Default to 100MB
        server_cpu = int(server_cpu) if server_cpu is not None else 1  # Default to 1 CPU

        try:

            container = client.containers.run(
                docker_image,
                name=server_name,
                detach=True,
                ports={f'{port}/tcp': None},
                mem_limit=f"{server_ram}M",
                cpu_period=100000,
                cpu_quota=int(server_cpu * 1000),  # 50% → 50000
                #storage_opt={'size': f'{storage}M'}, # Ne dela v celoti
                environment={
                    'EULA': 'TRUE' if server_nest == 'minecraft' else None,
                    'SERVER_NAME': server_name,
                }

            )

            self.container = container

        except Exception as e:
            print("Error creating container:")
            print(traceback.format_exc())
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def docker_stop(container_id) -> any:
        try:
            # Stop the container
            container = client.containers.get(container_id)
            container.stop()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def docker_start(container_id) -> any:
        try:
            # Start the container
            container = client.containers.get(container_id)
            container.start()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def docker_delete(container_id) -> any:
        try:
            # Stop the container
            container = client.containers.get(container_id)
            container.stop()
            container.remove(force=True)  # Force remove the container
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def docker_restart(container_id) -> any:
        try:
            # Restart the container
            container = client.containers.get(container_id)
            container.restart()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def stream_logs(container_id) -> any:
        try:
            container = client.containers.get(container_id)
            for line in container.logs(stream=True):
                yield f"data: {line.decode('utf-8')}\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    @staticmethod
    def container_stats(container_id) -> any:
        try:
            # Fetch the container by ID
            container = client.containers.get(container_id)

            server_data = Database.get_server_stats(container_id)

            # Get container stats
            stats = container.stats(stream=False)

            # Get current CPU usage (as a percentage of the total system CPU usage)
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100 if \
            stats['cpu_stats']['system_cpu_usage'] > 0 else 0

            # Get current RAM usage
            mem_usage = stats['memory_stats']['usage'] / (1024 * 1024)  # in MB

            # Get current Disk usage (if available)
            disk_usage = stats['storage_stats']['total'] / (1024 * 1024) if 'storage_stats' in stats else 0  # in MB

            # Fetch max CPU, RAM, and Disk from your DB or the user input
            # For example:
            max_cpu = float(server_data['cpu'])  # Assume this is passed from the user input or database
            total_ram = float(server_data['ram'])  # Same for RAM
            total_disk = float(server_data['storage'])  # Same for Disk

            # Calculate percentages
            cpu_percentage = (cpu_usage / max_cpu) * 100 if max_cpu > 0 else 0
            mem_percentage = (mem_usage / total_ram) * 100 if total_ram > 0 else 0
            disk_percentage = (disk_usage / total_disk) * 100 if total_disk > 0 else 0

            return jsonify({
                'cpu_percentage': round(cpu_percentage, 2),
                'mem_percentage': round(mem_percentage, 2),
                'disk_percentage': round(disk_percentage, 2)
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500


class DockerFiles:
    def __init__(self):
        pass

    @staticmethod
    def build_tree(file_list):
        tree = {}
        current_path = []

        current = tree
        for line in file_list:
            if line.endswith(':'):
                # New directory section (e.g., /app/data:)
                path = line[:-1]
                current_path = path.strip('/').split('/')
                current = tree
                for part in current_path:
                    if part not in current or not isinstance(current[part], dict):
                        current[part] = {}
                    current = current[part]
            elif line.strip():
                # It's a file inside the current directory
                current[line] = None  # File node
        return tree

    @staticmethod
    def docker_download_file(container_id, file_path):
        container = client.containers.get(container_id)
        local_tmp = f"/tmp/{os.path.basename(file_path)}"

        # Copy file from container to host
        with open(local_tmp, "wb") as f:
            bits, stat = container.get_archive(file_path)
            for chunk in bits:
                f.write(chunk)

        return local_tmp

    @staticmethod
    def docker_delete_file(container_id, file_path):
        try:
            container = client.containers.get(container_id)
            exit_code, output = container.exec_run(f"rm -f {file_path}")
            
            if exit_code == 0:
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': output.decode()})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def docker_edit_file(container_id, file_path, content):
        try:
            container = client.containers.get(container_id)
            temp_path = f"/tmp/edit_{os.path.basename(file_path)}"
            
            # Write content to a temp file
            with open(temp_path, 'w') as f:
                f.write(content)
                
            # Copy the file into the container
            with open(temp_path, 'rb') as f:
                container.put_archive(os.path.dirname(file_path), f.read())
                
            os.remove(temp_path)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def docker_create_file(container_id, file_path, content=""):
        try:
            container = client.containers.get(container_id)
            # Create directory structure if it doesn't exist
            dir_path = os.path.dirname(file_path)
            exit_code, _ = container.exec_run(f"mkdir -p {dir_path}")
            
            # Create file with content
            temp_path = f"/tmp/new_{os.path.basename(file_path)}"
            with open(temp_path, 'w') as f:
                f.write(content)
                
            # Copy the file into the container
            with open(temp_path, 'rb') as f:
                container.put_archive(dir_path, f.read())
                
            os.remove(temp_path)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def docker_upload_file(container_id, local_file_path, container_file_path):
        try:
            container = client.containers.get(container_id)
            
            # Copy the file into the container
            with open(local_file_path, 'rb') as f:
                container.put_archive(os.path.dirname(container_file_path), f.read())
                
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @staticmethod
    def docker_display_files(container_id):
        container = client.containers.get(container_id)
        volumes = container.attrs['Mounts']
        full_output = []

        for volume in volumes:
            if volume['Type'] == 'volume':
                mount_path = volume['Destination']
                exit_code, output = container.exec_run(f"ls -R {mount_path}")
                file_list = output.decode().splitlines()
                full_output.extend(file_list)

        file_tree = DockerFiles.build_tree(full_output)
        return file_tree

    @staticmethod
    def docker_create_folder(container_id, folder_path):
        try:
            container = client.containers.get(container_id)
            exit_code, output = container.exec_run(f"mkdir -p {folder_path}")
            
            if exit_code == 0:
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': output.decode()})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

# Docker
DockerManager = DockerManager()

class Database:
    def __init__(self):
        # Initialize Firestore
        self.db = None
        self.client = self.get_firestore_client()

    def get_firestore_client(self):
        return self.db # IDK zakaj je to potrebno

    @staticmethod
    def server_create(server_name, server_description, server_cpu, server_ram, server_storage, server_ports, server_databases, server_backup, server_location, server_nest, server_egg):
        try:
            # Adding server to Firestore
            server_ref = db.collection('servers').add({
                'name': server_name,
                'description': server_description,
                'cpu': server_cpu,
                'ram': server_ram,
                'storage': server_storage,
                'ports_number': server_ports,
                'databases_number': server_databases,
                'backup_number': server_backup,
                'location': server_location,
                'ip': DockerManager.container.attrs['NetworkSettings']['IPAddress'],
                'ports': DockerManager.container.ports,
                'user_id': session['user_id'],
                'container_id': DockerManager.container.id,
                'nest': server_nest,
                'egg': server_egg,
            })

        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def server_delete(server_id):
        try:
            # Delete server from Firestore
            docs = db.collection('servers').where('container_id', '==', server_id).stream()
            for doc in docs: #Loop je nepotreben, ker je samo en server
                db.collection('servers').document(doc.id).delete()

            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def get_server_stats(container_id):
        try:
            # Get server stats from Firestore
            server_ref = db.collection('servers').where('container_id', '==', container_id).stream()
            for doc in server_ref:
                server_data = doc.to_dict()
                return {
                    'cpu': server_data['cpu'],
                    'ram': server_data['ram'],
                    'storage': server_data['storage'],
                    'name': server_data['name'],
                    'description': server_data['description'],
                    'ports_number': server_data['ports_number'],
                    'databases_number': server_data['databases_number'],
                    'backup_number': server_data['backup_number'],
                    'location': server_data['location'],
                    'ip': server_data['ip'],
                    'ports': server_data['ports'],
                    'user_id': server_data['user_id'],
                    'container_id': server_data['container_id'],
                    'nest': server_data['nest'],
                    'egg': server_data['egg']
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}

