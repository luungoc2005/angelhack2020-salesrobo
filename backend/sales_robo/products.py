import json
from uuid import uuid4
from flask import (
    Blueprint, jsonify, request, 
)
from werkzeug.exceptions import (
    NotFound,
)
from os import path

bp = Blueprint('products', __name__, url_prefix='/products')
DATA_FILE_NAME = path.join(path.dirname(__file__), 'data/user_products_data.json')


@bp.route('/', methods=('GET',))
def get_products():
    if path.isfile(DATA_FILE_NAME):
        with open(DATA_FILE_NAME, 'r') as json_file:
            return jsonify(json.load(json_file))
    else:
        return jsonify([])


def _get_product_by_id(id):
    if path.isfile(DATA_FILE_NAME):
        with open(DATA_FILE_NAME, 'r') as json_file:
            all_data = json.load(json_file)
    else:
        all_data = []

    for it in all_data:
        if it['id'] == id:
            return it
    return None


@bp.route('/<id>', methods=('GET',))
def get_products_by_id(id):
    item = _get_product_by_id(id)
    if item is not None:
        return jsonify(item)
    else:
        raise NotFound()


@bp.route('/', methods=('PUT',))
def put_product():
    data = request.json
    data['id'] = uuid4().hex

    if path.isfile(DATA_FILE_NAME):
        with open(DATA_FILE_NAME, 'r') as json_file:
            all_data = json.load(json_file)
    else:
        all_data = []

    all_data.append(data)

    with open(DATA_FILE_NAME, 'w') as json_file:
        json.dump(all_data, json_file)
    
    return jsonify(data)


@bp.route('/<id>', methods=('POST',))
def post_product(id):
    data = request.json
    data['id'] = id

    if path.isfile(DATA_FILE_NAME):
        with open(DATA_FILE_NAME, 'r') as json_file:
            all_data = json.load(json_file)
    else:
        all_data = []

    all_data = [item for item in all_data if item['id'] != id]
    all_data.append(data)

    with open(DATA_FILE_NAME, 'w') as json_file:
        json.dump(all_data, json_file)
    
    return jsonify(data)


@bp.route('/<id>', methods=('PATCH',))
def patch_product(id):
    data = request.json
    data['id'] = id

    if path.isfile(DATA_FILE_NAME):
        with open(DATA_FILE_NAME, 'r') as json_file:
            all_data = json.load(json_file)
    else:
        all_data = []

    update_item = [item for item in all_data if item['id'] == id]

    if len(update_item) == 0:
        raise NotFound()
    else:
        update_item = update_item[0]

    update_item.update(data)

    all_data = [item for item in all_data if item['id'] != id]
    all_data.append(update_item)

    with open(DATA_FILE_NAME, 'w') as json_file:
        json.dump(all_data, json_file)
    
    return jsonify(data)

