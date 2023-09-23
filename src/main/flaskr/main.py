from flask import Flask
from src.main.flaskr.terminal.endpoint.terminal_endpoint import terminal_endpoint

app = Flask(__name__)

app.register_blueprint(terminal_endpoint)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
    