from flask import jsonify, request, render_template, send_file
from flaskr.models import load_server_templates
import docker
import os

# Load Docker client
#REMOTE_DOCKER_HOST = 'tcp://local.jonpecar.xyz:2375'
#REMOTE_DOCKER_HOST = 'tcp://192.168.1.187:2375'
#client = docker.DockerClient(base_url=REMOTE_DOCKER_HOST)
client = docker.from_env()

class DockerManager:
    def __init__(self):
        self.__server_templates = load_server_templates()
        self.container = None

    def docker_create(self, server_name, server_cpu, server_storage, server_ram, server_nest, server_egg):

        docker_image = self.__server_templates[server_nest]['eggs'][server_egg]['docker_image']
        port = self.__server_templates[server_nest]['port_default']
        try:

            # Run the container with the appropriate Docker image
            container = client.containers.run(
                docker_image,
                name=server_name,
                detach=True,  # Run in detached mode
                ports={f'{port}/tcp': None},  # Expose necessary ports for the game
                environment={
                    'EULA': 'TRUE',  # Example environment variable
                    'SERVER_NAME': server_name,
                    "CPU": server_cpu,
                    "STORAGE": server_storage,
                    "RAM": server_ram,
                }

            )

            self.container = container

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    def docker_stop(self, container_id):
        try:
            # Stop the container
            container = client.containers.get(container_id)
            container.stop()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    def docker_start(self, container_id):
        try:
            # Start the container
            container = client.containers.get(container_id)
            container.start()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    def docker_delete(self, container_id):
        try:
            # Stop the container
            container = client.containers.get(container_id)
            container.stop()
            container.remove(force=True)  # Force remove the container
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})


    def docker_restart(self, container_id) -> any:
        try:
            # Restart the container
            container = client.containers.get(container_id)
            container.restart()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

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

    def docker_delete_file(self):
        pass

    def docker_edit_file(self):
        pass

    def docker_create_file(self):
        pass

    @staticmethod
    def docker_display_files( container_id):
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

    def docker_create_folder(self):
        pass