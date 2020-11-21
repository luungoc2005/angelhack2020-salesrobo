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
import numpy as np
import pandas as pd
from .products import _get_product_by_id

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


@bp.route('/<id>', methods=('PATCH',))
def update_today_units(id):
    data = request.json
    
    product_object = _get_product_by_id(id)
    units_sold = data.get('units_sold', 0)

    if product_object is not None:
        product_sales = product_object.get('sales')
        if product_sales is None:
            raise BadRequest()
        sales_file = path.join(UPLOAD_PATH, product_sales)
        
        if not path.isfile(sales_file):
            raise BadRequest()

        from statsmodels.tsa.arima_model import ARIMA
        df = pd.read_csv(sales_file, index_col=None)
        DATE_FORMAT = "%Y-%m-%d"
        now_date = datetime.now().strftime(DATE_FORMAT)
        df_dates = pd.to_datetime(df['date']).dt.strftime(DATE_FORMAT)
        
        # if date does not exist
        if sum(df_dates == now_date) == 0:
            df = df.append(pd.Series({
                "date": now_date,
                "units_sold": units_sold,
                "price": df['price'].values.tolist()[-1]
            }), ignore_index=True)
        else:
            df['units_sold'] = np.where(
                df_dates == now_date,
                units_sold,
                df['units_sold'].values
            )
        
        df.to_csv(sales_file, index=False)

        return jsonify(data)
    else:
        raise NotFound()