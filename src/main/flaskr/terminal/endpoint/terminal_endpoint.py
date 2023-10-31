import sys

from flask import Blueprint
from markupsafe import escape
from src.main.bluesky.creator import airlineslist

terminal_endpoint = Blueprint('terminal_endpoint', __name__)

from src.main.flaskr.globals.model.response import response_with_request, text_response
from bluesky.network.client import Client


class TextClient(Client):
    def __init__(self):
        super().__init__()

    def stack(self, text):
        self.send_event(b'STACK', text, b"*")


bsclient = TextClient()
bsclient.connect(event_port=11000, stream_port=11001)


@terminal_endpoint.route("/<command>")
def parse_command(command):
    airline = airlineslist()
    res = text_response
    res.update({
        "status": command,
        "message": airline
    })
    stack = "CRE 12 12 12 12 12 12 12"
    if bsclient is not None:
        bsclient.stack(stack)
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
