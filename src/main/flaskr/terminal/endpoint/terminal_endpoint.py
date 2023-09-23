from flask import Blueprint
from markupsafe import escape

terminal_endpoint = Blueprint('terminal_endpoint', __name__)

from src.main.flaskr.global_model.response import response_with_request



@terminal_endpoint.route("/terminal/<command>")
def parse_command(command):
    """parses the given command, validates and runs it
    
    Returns:
        text_response: [Int, String]
    """
    res = response_with_request
    res.update({
            "status": 200,
            "message": "your message has been seen by the server",
            "request": escape(command)
        })
    return res
