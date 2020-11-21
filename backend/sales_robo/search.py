from datetime import datetime
import json
import random
from os import path
from flask import (
    Blueprint, jsonify, request, 
)
from werkzeug.exceptions import (
    NotFound,
    BadRequest,
)
from werkzeug.utils import secure_filename
from urllib.request import pathname2url

bp = Blueprint('search', __name__, url_prefix='/search')
MAX_RESULTS = 100
VENDORS = ['amazon', 'shopee']
UPLOAD_PATH = path.join(path.dirname(__file__), "_upload")


@bp.route('/suggestions', methods=('GET',))
def get_search_keywords():
    return jsonify([
        "smartphone",
        "children's book",
        "rice cooker",
        "origami",
        "selfie stick",
        "wireless charger",
        "birthday cake",
        "nintendo switch",
        "lipstick",
    ])


@bp.route('/', methods=('GET',))
def get_search_results():
    query = request.args.get('q')
    limit = request.args.get('limit', MAX_RESULTS)
    data = []
    for vendor in VENDORS:
        vendor_file_path = path.join(
            path.dirname(__file__), 
            f"products_data/data_amazon_{pathname2url(query)}.json"
        )
        if not path.isfile(vendor_file_path):
            continue
        with open(vendor_file_path, 'r') as fp:
            vendor_data = [
                {**item, 'from': vendor}
                for item in json.load(fp)
                if item.get('price') is not None
                and item.get('price') > 0
                and item.get('sold') is not None
                and item.get('sold') > 0
            ][:limit // 2]
            data.extend(vendor_data)

    random.shuffle(data)
    return jsonify(data)


@bp.route('/upload_image', methods=('POST',))
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