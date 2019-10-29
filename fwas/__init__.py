import logging

import click_log
import rq_dashboard
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from .api import blueprint as api_blueprint
from .config import Config
from .database import db

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def create_app(config=Config):

    logger.info("Creating app..")
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config.from_object(rq_dashboard.default_settings)

    db.init_app(app)
    Migrate(app, db)
    Marshmallow(app)
    docs = FlaskApiSpec(app)

    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

    import fwas.models  # noqa: F401

    with app.app_context():
        db.create_all()

    # Register API endpoints with apispec
    from . import api

    docs.register(api.user, blueprint="api_blueprint")
    docs.register(api.create_user, blueprint="api_blueprint")
    docs.register(api.user_alerts, blueprint="api_blueprint")
    docs.register(api.user_notifications, blueprint="api_blueprint")

    logger.info("App created")

    return app
