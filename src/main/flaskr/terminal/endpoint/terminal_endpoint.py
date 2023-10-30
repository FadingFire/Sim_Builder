from flask import Blueprint, request
from markupsafe import escape
from src.main.bluesky.creator import airlineslist

terminal_endpoint = Blueprint('terminal_endpoint', __name__)

from src.main.flaskr.globals.model.response import response_with_request, text_response


@terminal_endpoint.route("/<command>")
def parse_command(command):
    """parses the given command, validates and runs it

    Returns:
        response_with_request: [Int, String, String]
    """
    res = response_with_request
    res.update({
            "status": 200,
            "message": "your command has been seen by the server",
            "request": escape(command)
        })
    return res


@terminal_endpoint.route("/start")
def start_command():
    """sends start command to the server
    Returns:
        text_response: [Int, String]
    """
    data = request.args.get('choose')
    airline = airlineslist()
    res = text_response
    print(request.args.get('choose'))
    res.update({
            "status": data,
            "message": airline
        })
    return res

@terminal_endpoint.route("/stop")
def stop_command():
    """sends stop command to the server
    
    Returns:
        text_response: [Int, String]
    """
    res = text_response
    res.update({
            "status": 200,
            "message": "the start command has been seen by the server",
        })
    return res
