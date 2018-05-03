# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(config_name=None):
    app = Flask(__name__)
    
    return app




def register_blueprints(app):
    from main_app.hello import bp_hello
    app.register_blueprint(bp_hello.bp, url_prefix='/hello')



