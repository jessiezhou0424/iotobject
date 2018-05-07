from flask_login import UserMixin
from sqlalchemy import text
from sqlalchemy.dialects.mysql import ENUM, BIGINT
from main_app import db


class User(db.Model, UserMixin):
    """用户"""
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(64))

    db.Index('ix_oauth_openid', oauth_from, oauth_openid, unique=True)

    def to_dict(self):
        d = {
            
        }
        return d

    