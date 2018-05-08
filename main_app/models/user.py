from flask_login import UserMixin
from sqlalchemy import text
from sqlalchemy.dialects.mysql import ENUM, BIGINT
from main_app import db
import sys


class User(db.Model, UserMixin):
    """用户"""
    __tablename__ = 'py_user'#对应mysql数据库表
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(64))

    def __init__(self,name,pwd):
        self.name=name
        self.pwd=pwd

    def get_id(self):
        return sys.unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    