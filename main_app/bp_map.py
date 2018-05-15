from  flask import render_template,Blueprint,redirect,url_for,flash,request
from flask_login import login_user, logout_user,login_required

from main_app.forms.userform import Login_Form,Register_Form
from main_app.models.user import User
from main_app import db
import json,requests

bp = Blueprint('bp_route', __name__)

@bp.route('/display')
def display():
    return render_template('maps/map_startup.html')

@bp.route('/map')
def map():
    return render_template('maps/map.html')

@bp.route('/map/addbikepin')
def addbikepin():
    positions=[(150.0523, -32.8306),(150.053, -32.8307),(150.0528, -32.83069)]
    currentp= request.query_string.decode()[1:]
    jsonlist=[]
    for i in range(len(positions)):
        distq="https://atlas.microsoft.com/route/directions/json?subscription-key=KvO9Xix-Fn8WuxK8VKnqSm7tukA-aPgycdk-tEpxoNk&api-version=1.0&query="+\
        currentp.split(",")[0]+","+currentp.split(",")[1]+":"+str(positions[i][1])+","+str(positions[i][0])
        response=requests.get(distq).json()
        dist=response["routes"][0]["summary"]["lengthInMeters"];
        position={"lon":positions[i][0],"lat":positions[i][1]};
        jsonlist.append({"dist":dist,"position":position})
    return json.dumps(jsonlist)

@bp.route('/request_route')
def request_route():
    return render_template('login.html',form=form)
