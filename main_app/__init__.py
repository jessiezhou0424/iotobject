# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(config_name=None):
    app = Flask(__name__)
    db.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from main_app.hello import bp_hello
    from main_app import bp_user

    app.register_blueprint(bp_hello.bp, url_prefix='/hello')
    app.register_blueprint(bp_user.bp, url_prefix='/user')



