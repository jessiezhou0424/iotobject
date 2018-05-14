from  flask import render_template,Blueprint,redirect,url_for,flash
from flask_login import login_user, logout_user,login_required

from main_app.forms.userform import Login_Form,Register_Form
from main_app.models.user import User
from main_app import db
import json

bp = Blueprint('bp_route', __name__)

@bp.route('/display')
def display():
    return render_template('maps/map_startup.html')

@bp.route('/map')
def map():
    return render_template('maps/map.html')

@bp.route('/request_route')
def request_route():
    return render_template('login.html',form=form)
