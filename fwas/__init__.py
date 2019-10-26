import logging

import click_log
import rq_dashboard
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
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

    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

    import fwas.models  # noqa: F401

    _ = APISpec(
        title="Fire Weather Alert Service",
        version="0.1.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    with app.app_context():
        db.create_all()

    logger.info("App created")

    return app
