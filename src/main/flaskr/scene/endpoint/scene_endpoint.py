import os
import pandas as pd
from flask import Blueprint, current_app, request, send_file
from src.main.bluesky.paginator import paginate_dataframe, editdata, delete, addData
from src.main.bluesky.creator import parsefiles
# from src.main.bluesky.creator import parsefiles
from werkzeug.utils import secure_filename
from src.main.bluesky.parser import getdata

scene_endpoint = Blueprint('scene_endpoint', __name__)
from src.main.flaskr.globals.model.response import response_with_request, text_response, paginated_response

outputfile = "src/main/bluesky/Data/complete.csv"


@scene_endpoint.route('/change_outputfile', methods=['OPTIONS'])
def change_outputfile():
    global outputfile
    if request.args.get('selfmade') == "true":
        outputfile = "src/main/bluesky/Data/SAVE/selfmade.csv"
    else:
        outputfile = "src/main/bluesky/Data/complete.csv"
    return outputfile


@scene_endpoint.route('/upload', methods=['POST'])
def upload_file():
    res = text_response

    if 'Flights' not in request.files:
        res.update({
            "status": 500,
            "message": "No file given",
        })
        return res

    Flights = request.files['Flights']
    Landings = request.files['Landings']

    if Flights.filename == '':
        res.update({
            "status": 500,
            "message": "No file name was given",
        })
        return res

    uploads_dir = "src/main/bluesky/Data/SAVE"

    if Flights and Landings:
        Flights_filename = secure_filename(Flights.filename)
        Landings_filename = secure_filename(Landings.filename)

        Flights.save(os.path.join(uploads_dir, Flights_filename))
        Landings.save(os.path.join(uploads_dir, Landings_filename))

        parsefiles(os.path.join(uploads_dir, Flights_filename),
                   os.path.join(uploads_dir, Landings_filename),
                   outputfile)

        # Delete the files after use
        os.remove(os.path.join(uploads_dir, Flights_filename))
        os.remove(os.path.join(uploads_dir, Landings_filename))

        res.update({
            "status": 200,
            "message": "You have successfully uploaded and processed your files",
        })

    elif Flights:
        Flights_filename = secure_filename(Flights.filename)

        Flights.save(
            os.path.join(uploads_dir, Flights_filename)
        )

        parsefiles(
            os.path.join(uploads_dir, Flights_filename),
            "scr/main/bluesky/Data/Landings.csv",
            outputfile
        )

        # Delete the file after use
        os.remove(os.path.join(uploads_dir, Flights_filename))

        res.update({
            "status": 200,
            "message": "You have successfully uploaded and processed your file",
        })

    return res

@scene_endpoint.route('/download')
def download_file():
    # Send the file back to the frontend
    return send_file(
        os.path.join(current_app.config['UPLOAD_FOLDER'], "complete.csv"), as_attachment=True
    )

@scene_endpoint.route('/complete/table', methods=['GET'])
def paginated_file():
    res = paginated_response
    res.update({
        "status": 200,
        "message": "The server has seen your request",
        "request": "The server has seen your request"
    })

    # Get parameters from the request
    page_size = request.args.get('pageSize', default=10, type=int)
    page_number = request.args.get('pageNumber', default=1, type=int)
    search_filter = request.args.get('searchfilter', default="KLM", type=str)
    sort_by = request.args.get('sortBy', default="FLIGHT_ID", type=str)
    order = request.args.get('order', default="asc", type=str)

    # Call paginate_dataframe function to get paginated data
    paginated_data, row_count, new_search_filter = paginate_dataframe(
        page_size,
        page_number,
        outputfile,
        search_filter,
        sort_by,
        order
    )

    res["data"] = paginated_data
    res["pagenumber"] = row_count

    # Include new_search_filter and stored_search_filter in the response
    res["new_search_filter"] = new_search_filter
    res["stored_search_filter"] = search_filter

    return res


@scene_endpoint.route('/delete', methods=['GET'])
def deleterow():
    res = text_response
    delete(
        request.args.get('DeleteOlder', default="01-01-2000", type=str),
        request.args.get('Deleterow', default=0, type=float),
        outputfile
    )
    res.update({
        "status": 200,
        "message": "The server has seen your request"
    })
    return res


@scene_endpoint.route('/scene', methods=['GET'])
def scenefile():
    inputfile = "../bluesky/Data/scenefile.scn"
    getdata(
        outputfile,
        "src/main/bluesky/Data/scenefile.scn",
        request.args.get('sortamount', default=50, type=int),
        request.args.get('slidervalue'),
        request.args.get('slidervalueWTC'),
        request.args.get('APPvalue'),
        request.args.get('scenetime')
    )
    return send_file(inputfile, as_attachment=True, mimetype='application/octet-stream')


@scene_endpoint.route('/update', methods=['PATCH'])
def update_data():
    res = text_response
    editdata(
        outputfile,
        request.json
    )
    res.update({
        "status": 200,
        "message": "The server has seen your request"
    })
    return res


@scene_endpoint.route('/add', methods=['PATCH'])
def new_data():
    res = text_response
    addData(
        outputfile,
        request.json
    )
    res.update({
        "status": 200,
        "message": "The server has seen your request"
    })
    return res
