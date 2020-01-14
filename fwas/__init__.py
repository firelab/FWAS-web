import logging
from logging.handlers import RotatingFileHandler

import click_log
import rq_dashboard
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from .api import blueprint as api_blueprint
from .auth.views import auth_blueprint
from .config import Config
from .database import db
from .extensions import bcrypt, login
from .user.views import user

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def create_app(config=Config):

    logger.info("Creating app..")
    app = Flask(__name__)
    app.config.from_object(config())
    app.config.from_object(rq_dashboard.default_settings)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    Marshmallow(app)
    login.init_app(app)

    # Configure authentication
    from fwas.models import User, BlacklistToken

    login.login_view = "user.login"

    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login.request_loader
    def load_user_from_request(request):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""

        if not auth_token:
            return None

        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            return None

        user = User.verify_auth_token(auth_token)
        return user

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")
    app.register_blueprint(user)

    # Create database models
    import fwas.models  # noqa: F401

    with app.app_context():
        db.create_all()

    # Register API endpoints with apispec
    from . import api, auth

    docs = FlaskApiSpec(app)
    docs.register(api.user, blueprint="api_blueprint")
    docs.register(api.user_alerts, blueprint="api_blueprint")
    docs.register(api.user_notifications, blueprint="api_blueprint")
    docs.register(api.register_alert_subscriber, blueprint="api_blueprint")

    docs.register(auth.views.create_user, blueprint="auth_blueprint")
    docs.register(auth.views.user_login, blueprint="auth_blueprint")
    docs.register(auth.views.user_status, blueprint="auth_blueprint")
    docs.register(auth.views.user_logout, blueprint="auth_blueprint")

    # Configure logger
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    handler = RotatingFileHandler("app.log", maxBytes=10000000, backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    logger.info("App created")

    return app
