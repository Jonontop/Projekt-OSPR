from flaskr import db, DockerManager
from flask import session

class Database:
    def __init__(self):
        pass

    def get_firestore_client(self):
        return db # IDK zakaj je to potrebno

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