import json
from flask import (
    Blueprint, jsonify, request, 
)
from werkzeug.exceptions import (
    NotFound,
)
from trading_calendars import get_calendar
from datetime import datetime

bp = Blueprint('misc-data', __name__, url_prefix='/misc-data')


@bp.route('/holidays', methods=('GET',))
def get_holidays():
    current_year = datetime.today().year
    return jsonify([
        {
            'id': 0,
            'name': 'Singapore Holidays',
            'dates': get_calendar('XSES') \
                .precomputed_holidays[
                    get_calendar('XSES').precomputed_holidays.year == current_year
                ] \
                .tolist(),
        },
    ])

