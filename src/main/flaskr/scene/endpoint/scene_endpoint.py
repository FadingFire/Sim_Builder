from flask import Blueprint
from markupsafe import escape

scene_endpoint = Blueprint('scene_endpoint', __name__)

from src.main.flaskr.globals.model.response import response_with_request, text_response

@scene_endpoint.route("/load/<filename>")
def load_scene(filename):
    """loads a scene file to the active blueksy window
    
    Returns:
        response_with_request: [Int, String, String]
    """
    res = response_with_request
    res.update({
            "status": 200,
            "message": "the start command has been seen by the server",
            "request": escape(filename)
        })
    return res
