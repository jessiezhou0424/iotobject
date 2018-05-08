from sqlalchemy import text
from sqlalchemy.dialects.mysql import ENUM, BIGINT
from main_app import db
import sys


class Orders(db.Model):
    """用户"""
    __tablename__ = 'orders'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    STATUS_DICT = { # status for order
        0: '',
        1: '',
        2: 'expired' 
    }


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    status = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, server_default=text('NOW()'))

    def __init__(self,name,pwd):
        self.name=name
        self.pwd=pwd

    