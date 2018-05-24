from sqlalchemy import text
from sqlalchemy.dialects.mysql import ENUM, BIGINT
from main_app import db
import sys


class Bike(db.Model):
    """bikes"""
    __tablename__ = 'bike'#对应mysql数据库表
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    STATUS_DICT = { # status for order
        0: 'space',
        1: 'used'
    }

    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    status = db.Column(db.Integer, default=0)
    device_id = db.Column(db.Integer, primary_key=True)

    def __init__(self,device_id,lon,lat,status):
        self.lon=lon
        self.lat=lat
        self.status=status
        self.device_id=device_id

    def to_dict(self):
        return {
            'device': self.device_id,
            'log': self.lon,
            'lat': self.lat
        }

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<lon %r>' % self.lon

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

