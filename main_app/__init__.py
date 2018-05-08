# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name=None):
    app = Flask(__name__)
    db.init_app(app)
    register_blueprints(app)
    bootstrap = Bootstrap(app)
    app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
    ))
    moment=Moment(app)
    login_manger=LoginManager()
    login_manger.session_protection='strong'
    login_manger.login_view='blog.login'
    login_manger.init_app(app)
    return app

    @login_manger.user_loader
    def load_user(user_id):
        from main_app.models.user import User
        return User.query.get(int(user_id))


def register_blueprints(app):
    from main_app.hello import bp_hello
    from main_app import bp_user

    app.register_blueprint(bp_hello.bp, url_prefix='/hello')
    app.register_blueprint(bp_user.bp, url_prefix='/user')



