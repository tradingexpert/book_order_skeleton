from flask import Flask
from flask_migrate import Migrate


def create_app(config_obj: object) -> Flask:
    """Flask application factory"""
    app = Flask('bookapp')
    app.config.from_object(config_obj)

    from bookapp.models import db
    from bookapp.views import api
    app.register_blueprint(api)

    db.init_app(app)
    migrate = Migrate(app, db)      # In order to accommodate future migrations
    return app
