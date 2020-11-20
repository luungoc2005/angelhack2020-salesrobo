import json
from flask import (
    Blueprint, jsonify, request, 
)
from werkzeug.exceptions import (
    NotFound,
)
from trading_calendars import get_calendar

bp = Blueprint('misc-data', __name__, url_prefix='/misc-data')


@bp.route('/holidays', methods=('GET',))
def get_holidays():
    xses_calendar = get_calendar('XSES')
    return jsonify({
        'name': 'Singapore Holidays',
        'dates': xses_calendar.precomputed_holidays.tolist(),
    })

