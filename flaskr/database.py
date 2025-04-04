from flaskr import db, DockerManager
from flask import session

class Database:
    def __init__(self):
        pass

    def get_firestore_client(self):
        return db # IDK zakaj je to potrebno

    def server_create(self, server_name, server_description, server_cpu, server_ram, server_storage, server_ports, server_databases, server_backup, server_location, server_nest, server_egg):
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

    def server_delete(self, server_id):
        try:
            # Stop the container
            container = DockerManager.container.get(server_id)
            container.stop()
            container.remove(force=True)  # Force remove the container

            # Delete server from Firestore
            db.collection('servers').document(server_id).delete()

            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}