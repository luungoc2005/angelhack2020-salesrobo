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
from sklearn.linear_model import LinearRegression

from .search import _search_products, VENDORS
from .products import _get_product_by_id

bp = Blueprint('pricing', __name__, url_prefix='/pricing')


@bp.route('/optimal_pricing/<id>', methods=('GET',))
def get_optimal_pricing(id):
    product_object = _get_product_by_id(id)
    if product_object is not None:
        data = _search_products(
            query=product_object['keyword'],
            limit=None,
            product_image=product_object.get('product_image'),
            price_from=product_object.get('price_from'),
            price_to=product_object.get('price_to'),
        )

        marginal_cost = product_object.get('marginal_cost')
        
        if marginal_cost is None or float(marginal_cost) == 0:
            return jsonify({
                'optimal_price': 0,
                'elasticity': 0,
                'r2': 0,
            })

        else:
            marginal_cost = float(marginal_cost)
            vendors_weights = []
            vendors_e = []
            vendors_r2 = []

            for vendor in VENDORS:
                X_train = [item['price'] for item in data if item['from'] == vendor]
                y_train = [item['sold'] for item in data if item['from'] == vendor]

                X_train = np.log(np.array(X_train).reshape(-1, 1))
                y_train = np.log(np.array(y_train).reshape(-1, 1))

                from sklearn.linear_model import LinearRegression

                reg = LinearRegression().fit(X_train, y_train)

                r2 = reg.score(X_train, y_train)
                elasticity = reg.coef_[0][0]

                vendors_weights.append(len(X_train))
                vendors_e.append(elasticity)
                vendors_r2.append(r2)

            elasticity = sum([
                vendors_e[ix] * vendors_weights[ix] 
                for ix in range(len(VENDORS))
            ]) / sum(vendors_weights)
            r2 = sum([
                vendors_r2[ix] * vendors_weights[ix] 
                for ix in range(len(VENDORS))
            ]) / sum(vendors_weights)

            price = marginal_cost * (elasticity / (elasticity + 1))

            return jsonify({
                'optimal_price': price,
                'elasticity': elasticity,
                'r2': r2,
            })
    else:
        raise NotFound()