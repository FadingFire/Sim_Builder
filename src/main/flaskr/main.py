from flask import Flask
from flask_cors import CORS
from src.main.flaskr.terminal.endpoint.terminal_endpoint import terminal_endpoint
from src.main.flaskr.scene.endpoint.scene_endpoint import scene_endpoint

app = Flask(__name__)

# Enable CORS for the entire application
CORS(app)

app.register_blueprint(terminal_endpoint, url_prefix='/terminal')
app.register_blueprint(scene_endpoint, url_prefix='/scene')
app.config['UPLOAD_FOLDER'] = '../bluesky/Data/'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
