import json
from flask import (
    Blueprint, jsonify, request, 
)
from werkzeug.exceptions import (
    NotFound,
)
from datetime import datetime

bp = Blueprint('sales-data', __name__, url_prefix='/sales-data')
DATA_FILE_NAME = 'data/sales_data.csv'


