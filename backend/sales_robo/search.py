from datetime import datetime
import json
import random
from os import path
from flask import (
    Blueprint, jsonify, request, 
)
from werkzeug.exceptions import (
    NotFound,
)

bp = Blueprint('search', __name__, url_prefix='/search')
MAX_RESULTS = 100

@bp.route('/suggestions', methods=('GET',))
def get_search_keywords():
    return jsonify([
        "smartphone"
    ])


@bp.route('/', methods=('GET',))
def get_search_results():
    query = request.args.get('q')
    limit = request.args.get('limit', MAX_RESULTS)

    amazon_file_path = path.join(
        path.dirname(__file__), f"products_data/data_amazon_{query}.json"
    )
    shopee_file_path = path.join(
        path.dirname(__file__), f"products_data/data_shopee_{query}.json"
    )
    if not path.isfile(amazon_file_path):
        return jsonify([])

    data = []
    if path.isfile(amazon_file_path):
        with open(amazon_file_path, 'r') as fp:
            data.extend([
                {**item, 'from': 'amazon'}
                for item in json.load(fp)
            ][:limit // 2])
    if path.isfile(shopee_file_path):
        with open(shopee_file_path, 'r') as fp:
            data.extend([
                {**item, 'from': 'shopee'}
                for item in json.load(fp)
            ][:limit // 2])

    random.shuffle(data)
    return jsonify(data)

    