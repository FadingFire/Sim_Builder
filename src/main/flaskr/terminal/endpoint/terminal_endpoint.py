from flask import Blueprint, request
from markupsafe import escape
from src.main.bluesky.creator import airlineslist


terminal_endpoint = Blueprint('terminal_endpoint', __name__)

from src.main.flaskr.globals.model.response import response_with_request, text_response


@terminal_endpoint.route("/<command>")
def parse_command(command):
    airline = airlineslist()
    res = text_response
    res.update({
            "status": command,
            "message": airline
        })
    if command == "B":
        command = "CRE 12 12 12 12 12 12 12"
        try:
            from PyQt5.QtCore import Qt, QTimer
            from PyQt5.QtWidgets import QTextEdit
        except ImportError:
            from PyQt6.QtCore import Qt, QTimer
            from PyQt6.QtWidgets import QTextEdit

        from bluesky.network.client import Client


        echobox = None

        class TextClient(Client):
            def __init__(self):
                super().__init__()
                self.timer = QTimer()
                self.timer.timeout.connect(self.update)
                self.timer.start(20)

            def stack(self, text):
                ''' Stack function to send stack commands to BlueSky. '''
                self.send_event(b'STACK', text)


        # Create and start BlueSky client
        bsclient = TextClient()
        bsclient.connect(event_port=11000, stream_port=11001)
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
