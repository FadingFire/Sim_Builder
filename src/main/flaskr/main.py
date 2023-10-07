from flask import Flask
from src.main.flaskr.terminal.endpoint.terminal_endpoint import terminal_endpoint
from src.main.flaskr.scene.endpoint.scene_endpoint import scene_endpoint

app = Flask(__name__)

app.register_blueprint(terminal_endpoint, url_prefix='/terminal')
app.register_blueprint(scene_endpoint, url_prefix='/scene')
app.config['UPLOAD_FOLDER'] = '../bluesky/files/'
