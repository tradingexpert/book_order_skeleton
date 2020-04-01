"""
An application that performs basic web-service API functionality, using json-based communication.

Exports method:
    create_app - factory method for creating a flask application
"""

import os

from flask import Flask
from flask_migrate import Migrate


def create_app(config_obj: object = None) -> Flask:
    """Flask application factory"""
    app = Flask('bookapp')

    if not config_obj:
        # Read object file from the environment variable
        app.config.from_object(os.environ['APP_CONFIG'])
    else:
        app.config.from_object(config_obj)

    from bookapp.models import db
    from bookapp.views import api
    app.register_blueprint(api)

    db.init_app(app)
    migrate = Migrate(app, db)      # In order to accommodate future migrations
    return app
