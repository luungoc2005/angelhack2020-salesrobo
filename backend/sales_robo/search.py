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
import numpy as np
from werkzeug.utils import secure_filename
from urllib.request import pathname2url

bp = Blueprint('search', __name__, url_prefix='/search')
MAX_RESULTS = 100
VENDORS = ['amazon', 'shopee']
UPLOAD_PATH = path.join(path.dirname(__file__), "_upload")
IMAGE_SIMILARITY_THRESHOLD = 20

"""
One iphone vs multiple iphones
16.93065
One iphone vs Samsung phone
17.579874
One iphone vs Dog
24.606842
Dog vs Cat
24.56893
Cat vs Cat
16.510061
"""

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
        "iphone",
        "laptop",
    ])


def _search_products(
    query, 
    limit=None, 
    product_image=None,
    price_from=None,
    price_to=None,
):
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
            ]

        if price_from is not None and price_from > 0:
            vendor_data = [
                item for item in vendor_data
                if item.get('price') > price_from
            ]

        if price_to is not None and price_to > 0:
            vendor_data = [
                item for item in vendor_data
                if item.get('price') < price_to
            ]

        if product_image is not None:
            product_image_path = path.join(UPLOAD_PATH, product_image)
            if path.isfile(product_image_path):
                vendor_data = [
                    item for item in vendor_data if 
                    item.get('image')
                ]
                # print(f"Found {len(vendor_data)} items with images")
                from .utils.encode_image import encode_image
                my_product_enc = encode_image(product_image_path)
                filtered_vendor_data = []
                for item in vendor_data:
                    enc = encode_image(item.get('image'))
                    if enc is not None:
                        distance = np.linalg.norm(my_product_enc - enc, axis=0)
                        # print(distance)
                        if distance < IMAGE_SIMILARITY_THRESHOLD:
                            filtered_vendor_data.append(item)
                vendor_data = filtered_vendor_data

        if limit is not None:
            # to make results look nicer
            vendor_data = vendor_data[:limit // len(VENDORS)]
        data.extend(vendor_data)

    return data

@bp.route('/', methods=('GET',))
def get_search_results():
    query = request.args.get('q')
    limit = request.args.get('limit', MAX_RESULTS)
    product_image = request.args.get('product_image', None)
    price_from = float(request.args.get('price_from', 0))
    price_to = float(request.args.get('price_to', 0))
    
    data = _search_products(query, limit, product_image, price_from, price_to)
    
    # to make the results look nicer in the list
    random.shuffle(data)
    return jsonify(data)


@bp.route('/upload-image', methods=('POST',))
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