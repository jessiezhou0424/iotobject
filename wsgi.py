# -*- coding: utf-8 -*-

from main_app import create_app
from configparser import ConfigParser

cf = ConfigParser()
app = create_app('dev')
cf.read("uwsgi.ini")

if __name__ == '__main__':
    app.run(port="6666")

