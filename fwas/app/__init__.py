import logging

from flask import Flask

from .api import blueprint as api_blueprint
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
