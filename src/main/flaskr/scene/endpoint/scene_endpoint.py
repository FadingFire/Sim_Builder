import os
from flask import Blueprint
from flask import current_app
from flask import request
from markupsafe import escape
from werkzeug.utils import secure_filename
from src.main.flaskr.globals.model.response import response_with_request, text_response

scene_endpoint = Blueprint('scene_endpoint', __name__)


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


@scene_endpoint.route("/merge", methods=['POST'])
def merge():
    """appends a file to the blueksy filghts file that contains all the files.

    Returns:
        text_response: [Int, String]
    """
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    res = text_response
    res.update({
        "status": 200,
        "message": "the start command has been seen by the server",
    })
    return res


@scene_endpoint.route("/get/<sortamount>")
def get_info(sortamount):
    """gets sortamount info from FE

        Returns:
            response_with_request: [Int, String, String]
        """
    res = response_with_request
    res.update({
        "status": 200,
        "message": "the start command has been seen by the server",
        "request": escape(sortamount)
    })
    return res
