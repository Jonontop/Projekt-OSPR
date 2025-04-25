

from flask import Flask
from flaskr.models import load_server_templates
from flaskr.docker import DockerManager


# Defining the Flask app
app = Flask(__name__)
app.config.from_object('config')


# Defining the SQLAlchemy database object
# db = SQLAlchemy(app) # data stealing


from flaskr import routes
