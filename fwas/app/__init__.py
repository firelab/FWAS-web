import logging

from flask import Flask

from .api import blueprint as api_blueprint
from .config import Config


logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def create_app(config=Config):

    logger.info('Creating app..')
    app = Flask(__name__)

    app.register_blueprint(api_blueprint, url_prefix="/api")

    logger.info('App created')

    return app
