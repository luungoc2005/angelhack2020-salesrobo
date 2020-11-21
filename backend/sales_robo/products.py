import json
from uuid import uuid4
from flask import (
    Blueprint, jsonify, request, 
)
from werkzeug.exceptions import (
    NotFound,
)

bp = Blueprint('products', __name__, url_prefix='/products')
DATA_FILE_NAME = 'data/products_data.json'


@bp.route('/', methods=('GET',))
def get_products():
    with open(DATA_FILE_NAME, 'r') as json_file:
        return jsonify(json.load(json_file))


@bp.route('/<id>', methods=('GET',))
def get_products_by_id(id):
    with open(DATA_FILE_NAME, 'r') as json_file:
        all_data = json.load(json_file)
    for it in all_data:
        if it['id'] == id:
            return jsonify(it)
    raise NotFound()


@bp.route('/', methods=('PUT',))
def put_product():
    data = request.json
    data['id'] = uuid4().hex
    all_data = json.loads(DATA_FILE_NAME)
    all_data.append(data)

    with open(DATA_FILE_NAME, 'w') as json_file:
        json.dump(all_data, json_file)
    
    return jsonify(data)


@bp.route('/<id>', methods=('POST',))
def post_product(id):
    data = request.json
    data['id'] = id

    all_data = json.loads(DATA_FILE_NAME)
    all_data = [item for item in all_data if item['id'] != id]
    all_data.append(data)

    with open(DATA_FILE_NAME, 'w') as json_file:
        json.dump(all_data, json_file)
    
    return jsonify(data)


@bp.route('/<id>', methods=('PATCH',))
def patch_product(id):
    data = request.json
    data['id'] = id

    all_data = json.loads(DATA_FILE_NAME)
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

