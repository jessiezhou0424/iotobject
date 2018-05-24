import datetime
import random

from  flask import render_template,Blueprint,redirect,url_for,flash,request
from flask_login import login_user, logout_user,login_required
from main_app.forms.userform import Login_Form,Register_Form
from main_app.models.user import User
from main_app.models.bike import Bike
from main_app import db
import json
import requests

NSW_PLANNER_KEY =  "Psajnbl0TfP428H2baHaz2JWmXlWetqsEOCI"
NSW_PLANNER_URL = "https://api.transport.nsw.gov.au/v1/tp/"
bp = Blueprint('bp_map', __name__)

@bp.route('/display')
def display():
    return render_template('maps/map_startup.html')

@bp.route('/map')
def map():
    return render_template('maps/map.html')

@bp.route('/map/addbikepin')
def addbikepin():
    positions=[]
    positinquery=Bike.query.filter_by(status=0)
    for i in positinquery:
        positions.append((i.lon,i.lat))
    #positions=[(150.0523, -32.8306),(150.053, -32.8307),(150.0528, -32.83069)
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

@bp.route('/stop_finder')
def stop_finder():
    dest = request.args.get('dest')

    request_dict = {
        'outputFormat': 'rapidJSON',
        'odvSugMacro': 1,
        'name_sf': dest,
        'type_sf': 'any',
        'coordOutputFormat': 'EPSG:4326',
        'TfNSWSF': 'true',
        'version': '10.2.1.42'
    }

    request_header = {
        'Authorization': 'apikey %s' % NSW_PLANNER_KEY,
    }

    resp = requests.request("GET", NSW_PLANNER_URL + 'stop_finder/', params=request_dict, headers=request_header).json()
    locations = resp['locations']
    locations = sorted(locations, key=lambda x: -x['matchQuality'])[:5]
    return json.dumps(locations)

@bp.route('/route_planner')
def route_planner():
    origin_lon = request.args.get('origin_lon')
    origin_lat = request.args.get('origin_lat')
    dest = request.args.get('dest')
    print(request.args)

    request_dict = {
        'outputFormat': 'rapidJSON',
        'coordOutputFormat': 'EPSG:4326',
        'depArrMacro': 'dep',
        'odvSugMacro': 1,
        'name_origin': "%s:%s:EPSG:4326"%(origin_lon, origin_lat),
        'type_origin': 'coord',
        'name_destination': dest,
        'type_destination': 'any',
        'TfNSWSF': 'true',
        'version': '10.2.1.42',
        'itdDate': datetime.datetime.now().strftime("%Y%m%d"),
        'itdTime': datetime.datetime.now().strftime("%H%M"),
        'TfNSWTR': 'true'
    }

    request_header = {
        'Authorization': 'apikey %s' % NSW_PLANNER_KEY,
    }

    resp = requests.request("GET", NSW_PLANNER_URL + 'trip/', params=request_dict, headers=request_header).json()
    for journey in resp['journeys']:
        legs = journey['legs']
        for leg in legs:
            if int(leg['transportation']['product']['class']) == 5:
                leg['transportation']['capacity'] = 80
                leg['transportation']['currentOnboard'] = random.randint(5,80)
                for stop in leg['stopSequence']:
                    stop['expectedOnboard'] = random.randint(0,20)

    return json.dumps(resp['journeys'])
