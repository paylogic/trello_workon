"""Create the app for the management."""

from flask import Flask

from models.base import db_session

from management.blueprint import management


def create_app():
    """Create the flask app."""
    app = Flask(__name__)
    app.config['SERVER_NAME'] = '127.0.0.1:5000'
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'OWee7sohNgu2chuSh3aequaim6let9Ie'

    app.config.from_envvar('TRELLO_WORKON_SETTINGS')  # overrides server name, debug and secret key

    app.register_blueprint(management)

    return app

management_app = create_app()

@management_app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
