from os import path
from flask import (
    Blueprint, jsonify, request, send_from_directory,
)
from werkzeug.exceptions import (
    NotFound,
    BadRequest,
)
from werkzeug.utils import secure_filename

bp = Blueprint('uploads', __name__, url_prefix='/uploads')
UPLOAD_PATH = path.join(path.dirname(__file__), "_upload")


@bp.route('/<filename>')
def uploaded_file(filename):
    if path.isfile(path.join(UPLOAD_PATH, filename)):
        return send_from_directory(UPLOAD_PATH, filename)
    else:
        raise NotFound()