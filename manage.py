# -*- coding: utf-8 -*-

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from wsgi import app
from main_app import db



migrate = Migrate(app, db)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()

