from datetime import datetime, timedelta
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
import pandas as pd
from werkzeug.utils import secure_filename
from urllib.request import pathname2url
from sklearn.linear_model import LinearRegression

from .search import _search_products, VENDORS, UPLOAD_PATH
from .products import _get_product_by_id

bp = Blueprint('forecast', __name__, url_prefix='/forecast')


FORECAST_STEPS = 5
MAX_PAST_STEPS = 30


@bp.route('/<id>', methods=('GET',))
def get_forecast_sales(id):
    product_object = _get_product_by_id(id)
    if product_object is not None:
        product_sales = product_object.get('sales')
        if product_sales is None:
            raise BadRequest()
        sales_file = path.join(UPLOAD_PATH, product_sales)
        
        if not path.isfile(sales_file):
            raise BadRequest()

        from statsmodels.tsa.arima_model import ARIMA
        df = pd.read_csv(sales_file, index_col=None)
        df_diff = df['units_sold'].diff().dropna()

        values = list(df_diff.values)
        dates = list(pd.to_datetime(df['date'].values))
        preds = []
        last_value = df['units_sold'].values.tolist()[-1]
        groundtruth_steps = min(len(values), MAX_PAST_STEPS)
        
        for _ in range(FORECAST_STEPS):
            model=ARIMA(values, order=(5,1,0))
            results = model.fit(disp=0)
            output = float(results.forecast()[0])
            last_value += output
            preds.append(round(last_value))
            values.append(last_value)
            dates.append(dates[-1] + timedelta(days=1))

        str_dates = [item.strftime("%Y-%m-%d") for item in dates]
        
        str_dates = str_dates[-groundtruth_steps - FORECAST_STEPS:]

        trace1 = {
            "type": "scatter",
            "mode": "lines",
            "name": "Sales",
            "x": str_dates,
            "y": df['units_sold'].values.tolist()[-groundtruth_steps:] + ([None] * FORECAST_STEPS),
            "line": {
                "color": "#17BECF"
            }
        }
        trace2 = {
            "type": "scatter",
            "mode": "lines",
            "name": "Forecasted",
            "x": str_dates,
            "y": ([None] * groundtruth_steps) + preds,
            "line": {
                "color": "#7F7F7F"
            }
        }

        return jsonify([trace1, trace2])
    else:
        raise NotFound()