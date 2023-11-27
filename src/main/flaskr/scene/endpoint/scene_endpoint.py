import os
import pandas as pd
from flask import Blueprint, current_app, request, send_file
from src.main.bluesky.paginator import paginate_dataframe
from werkzeug.utils import secure_filename

scene_endpoint = Blueprint('scene_endpoint', __name__)
from src.main.flaskr.globals.model.response import response_with_request, text_response, paginated_response
# Load the complete CSV file into a DataFrame


@scene_endpoint.route('/upload', methods=['POST'])
def upload_file():
    res = text_response
    if 'file' not in request.files:
        res.update({
            "status": 500,
            "message": "No file given",
        })
    file = request.files['file']
    if file.filename == '':
        res.update({
            "status": 500,
            "message": "No file name was given",
        })
    if file:
        # YOUR BLUESKY MERGER CODE
        # Use file.data? or anything not including the filename
        res = text_response
        res.update({
            "status": 200,
            "message": "You have successfully uploaded your file to the server",
        })
    return res

@scene_endpoint.route('/download')
def download_file():
    # Send the file back to the frontend
    return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], "complete.csv"), as_attachment=True)

@scene_endpoint.route('/complete/table', methods=['GET'])
def paginated_file():
    res = paginated_response
    res.update({
        "status": 200,
        "message": "The server has seen your request",
        "request": "The server has seen your request"
    })
    page_size = request.args.get('pageSize', default=10, type=int)
    page_number = request.args.get('pageNumber', default=1, type=int)
    sortBy = request.args.get('sortBy', default="FLIGHT_ID", type=str)

    # Call paginate_dataframe function to get paginated data
    if pd.isna(sortBy):
        sortBy = "FLIGHT_ID"
        paginated_data = paginate_dataframe(page_size, page_number, sortBy)
        res["data"] = paginated_data
    else:
        paginated_data = paginate_dataframe(page_size, page_number, sortBy)
        res["data"] = paginated_data

    return res
