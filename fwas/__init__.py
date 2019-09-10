import logging

import click_log
from flask import Flask
from flask_migrate import Migrate

from .api import blueprint as api_blueprint
from .config import Config
from .database import db

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def create_app(config=Config):

    logger.info("Creating app..")
    app = Flask(__name__)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(api_blueprint, url_prefix="/api")

    #    from .models import *

    logger.info("App created")

    return app
