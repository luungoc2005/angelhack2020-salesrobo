import json
from flask import (
    Blueprint, jsonify, request, 
)
from werkzeug.exceptions import (
    NotFound,
    BadRequest,
)
from werkzeug.utils import secure_filename
from datetime import datetime
from os import path

bp = Blueprint('sales-data', __name__, url_prefix='/sales-data')
DATA_FILE_NAME = 'data/sales_data.csv'
UPLOAD_PATH = path.join(path.dirname(__file__), "_upload")


@bp.route('/upload', methods=('POST',))
def upload_product_image():
    if not path.isdir(UPLOAD_PATH):
        import os
        os.makedirs(UPLOAD_PATH, exist_ok=True)

    # check if the post request has the file part
    if 'file' not in request.files:
        raise BadRequest()
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        raise BadRequest()

    filename = secure_filename(file.filename)
    file.save(path.join(UPLOAD_PATH, filename))
    return jsonify({
        "name": filename
    })