from flask import jsonify
from flaskr.models import load_server_templates
import docker

# Load Docker client
#REMOTE_DOCKER_HOST = 'tcp://local.jonpecar.xyz:2375'  # Replace with your Docker host URL
#REMOTE_DOCKER_HOST = 'tcp://192.168.1.187:2375'  # Replace with your Docker host URL
#client = docker.DockerClient(base_url=REMOTE_DOCKER_HOST)
client = docker.from_env()

class DockerManager:
    def __init__(self):
        self.server_templates = load_server_templates()
        self.container = None

    def docker_create(self, server_name, server_cpu, server_storage, server_ram, server_nest, server_egg):

        docker_image = self.server_templates[server_nest]['eggs'][server_egg]['docker_image']
        try:

            # Run the container with the appropriate Docker image
            container = client.containers.run(
                docker_image,
                name=server_name,
                detach=True,  # Run in detached mode
                ports={'25565/tcp': None},  # Expose necessary ports for the game
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


    def docker_restart(self, container_id):
        try:
            # Restart the container
            container = client.containers.get(container_id)
            container.restart()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})