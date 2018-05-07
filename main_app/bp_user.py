import hashlib

from flask_login import current_user, login_user, logout_user, login_required
from models.user import User
from flask import request, url_for

bp = Blueprint('bp_user', __name__)

@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    form = request.form
    username = form.get('username')
    password = form.get('password')

    user = User.query.filter_by(username=username).first()

    encrypted_password = hashlib.sha1(_str).hexdigest()

    if password == encrypted_password:
        login_user(user)
        return json.dumps({'blah blah'})