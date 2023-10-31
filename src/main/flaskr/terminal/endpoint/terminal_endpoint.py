from flask import Blueprint
from src.main.bluesky.Client import TextClient

terminal_endpoint = Blueprint('terminal_endpoint', __name__)

from src.main.flaskr.globals.model.response import response_with_request, text_response


bsclient = TextClient()
bsclient.connect(event_port=11000, stream_port=11001)


@terminal_endpoint.route("/<command>")
def parse_command(command):
    # get all the airlines

    # send all airlines to FE
    res = text_response
    res.update({
        "status": 200,
        "message": "the command has been seen by the server"
    })
    # stack commands
    if bsclient is not None:
        bsclient.stack(command)
    return res


@terminal_endpoint.route("/start")
def start_command():
    """sends start command to the server
    Returns:
        text_response: [Int, String]
    """
    res = text_response
    res.update({
        "status": 200,
        "message": "the start command has been seen by the server",
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
