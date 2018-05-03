from flask import Blueprint
import json

bp = Blueprint('bp_hello', __name__)

@bp.route('/hello')
def hello():
    return json.dumps({'Response': 'Hello'})
