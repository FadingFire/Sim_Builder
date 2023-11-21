from flask import Blueprint
from src.main.bluesky.run import runbluesky
from src.main.flaskr.globals.model.response import response_with_request, text_response


terminal_endpoint = Blueprint('terminal_endpoint', __name__)


@terminal_endpoint.route("/<command>")
def parse_command(command):
    from src.main.bluesky.Client import bsclient
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
    from src.main.bluesky.Client import connectbs
    res = text_response
    runbluesky()
    connectbs()
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
    from src.main.bluesky.Client import bsclient
    res = text_response
    res.update({
        "status": 200,
        "message": "the stop command has been seen by the server",
    })
    if bsclient is not None:
        bsclient.stack("QUIT")
    return res
