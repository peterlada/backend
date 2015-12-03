# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Manager module
"""

import os

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from backend import api, frontend
from backend.core import db
from backend.manage import CreateUserCommand, DeleteUserCommand, ListUsersCommand


frontend_app = frontend.create_app()
api_app = api.create_app()
full_app = DispatcherMiddleware(frontend_app, {
    '/api': api_app
})

manager = Manager(frontend_app)

print os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend', 'alembic'))

migrate = Migrate(frontend_app, db, os.path.abspath(os.path.join(os.path.dirname(__file__), 'alembic')))
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    '''Overrides the default runserver command'''
    run_simple(frontend_app.config['HOST'], frontend_app.config['PORT'],
               full_app,
               use_reloader=True, use_debugger=frontend_app.debug)


@manager.shell
def shell_context():
    '''Populates the shell with default imports. Add common imports here.'''
    return {
        'frontend_app': frontend_app,
        'api_app': api_app,
        'app': full_app,
        'db': db,
    }


manager.add_command('create_user', CreateUserCommand())
manager.add_command('delete_user', DeleteUserCommand())
manager.add_command('list_users', ListUsersCommand())


if __name__ == "__main__":
    manager.run()
