import os
import pandas as pd
from flask import Blueprint, current_app, request, send_file
from src.main.bluesky.paginator import paginate_dataframe, editdata
from src.main.bluesky.creator import parsefiles, makescene
# from src.main.bluesky.creator import parsefiles
from werkzeug.utils import secure_filename

scene_endpoint = Blueprint('scene_endpoint', __name__)
from src.main.flaskr.globals.model.response import response_with_request, text_response, paginated_response
# Load the complete CSV file into a DataFrame

outputfile = "src/main/bluesky/Data/complete.csv"


@scene_endpoint.route('/upload', methods=['POST'])
def upload_file():
    res = text_response
    print(request.files)
    if 'Flights' not in request.files:
        res.update({
            "status": 500,
            "message": "No file given",
        })
    Flights = request.files['Flights']
    Landings = request.files['Landings']
    if Flights.filename == '':
        res.update({
            "status": 500,
            "message": "No file name was given",
        })
    if Flights and Landings:
        uploads_dir = "src/main/bluesky/Data/SAVE"
        Flights.save(os.path.join(uploads_dir, secure_filename(Flights.filename)))
        Landings.save(os.path.join(uploads_dir, secure_filename(Landings.filename)))
        parsefiles(os.path.join(uploads_dir, secure_filename(Flights.filename)), os.path.join(uploads_dir, secure_filename(Landings.filename)), outputfile)
        # Use file.data? or anything not including the filename
        res = text_response
        res.update({
            "status": 200,
            "message": "You have successfully uploaded your file to the server",
        })
    elif Flights:
        uploads_dir = "src/main/bluesky/Data/SAVE"
        Flights.save(os.path.join(uploads_dir, secure_filename(Flights.filename)))
        parsefiles(os.path.join(uploads_dir, secure_filename(Flights.filename)),
                   "scr/main/bluesky/Data/Landings.csv", outputfile)
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
    deleteafter = request.args.get('DeleteOlder', default="01-01-2000", type=str)
    deleterow = request.args.get('Deleterow', default=0, type=int)
    order = request.args.get('order', default="asc", type=str)

    # Call paginate_dataframe function to get paginated data
    paginated_data, rowcount = paginate_dataframe(page_size, page_number, sortBy, deleteafter, outputfile, deleterow, order)
    res["data"] = paginated_data
    res["pagenumber"] = rowcount
    return res


@scene_endpoint.route('/scene', methods=['GET'])
def scenefile():
    sortamount = request.args.get('sortamount', default=50, type=int)

    inputfile = "../bluesky/Data/scenefile.scn"
    makescene(outputfile, "src/main/bluesky/Data/scenefile.scn", sortamount)
    return send_file(inputfile, as_attachment=True, mimetype='application/octet-stream')


@scene_endpoint.route('/update', methods=['POST'])
def update_data():
    res = text_response
    editdata(outputfile, request.json)
    res.update({
        "status": 200,
        "message": "The server has seen your request"
    })
    return res


