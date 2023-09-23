from flask import Flask
from src.main.flaskr.terminal.endpoint.terminal_endpoint import terminal_endpoint

app = Flask(__name__)

app.register_blueprint(terminal_endpoint, url_prefix='/terminal')
