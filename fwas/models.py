from collections import OrderedDict
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
import pytz
from attrs_sqlalchemy import attrs_sqlalchemy
from flask import current_app
from flask_login import UserMixin
from geoalchemy2.types import Geometry, Raster
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import DateTime, TypeDecorator

from . import utils
from .database import db
from .extensions import bcrypt


def generate_uuid():
    return str(uuid4())


class AwareDateTime(TypeDecorator):
    impl = DateTime(timezone=True)

    def process_bind_params(self, value, dialect):
        if isinstance(value, datetime) and value.tzinfo is None:
            raise ValueError(f"{value} must be timezone-aware.")
        return value

    def __repr__(self):
        return "AwareDateTime()"


class TimeStampMixin(object):
    """Timestamping mixin for generating created_at and updated_at columns."""

    created_at = db.Column(AwareDateTime(), default=utils.get_current_utc_datetime)
    created_at._creation_order = 9998
    updated_at = db.Column(AwareDateTime(), default=utils.get_current_utc_datetime)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = utils.get_current_utc_datetime()

    @classmethod
    def __declare_last__(cls):
        db.event.listen(cls, "before_update", cls._updated_at)


class Base(db.Model, TimeStampMixin):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


@attrs_sqlalchemy
class User(UserMixin, Base):
    """User of the application and their contact information."""

    ROLES = OrderedDict([("member", "Member"), ("admin", "Admin")])

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(
        db.Enum(*ROLES, name="role_types", native_enum=False),
        index=True,
        nullable=False,
        server_default="member",
    )
    active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
    phone = db.Column(db.String(12))

    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_at = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_at = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    alerts = db.relationship("Alert", back_populates="user")
    notifications = db.relationship("Notification", back_populates="user")
    subscriptions = db.relationship(
        "Alert",
        secondary=lambda: alert_subscribers,
        lazy="subquery",
        backref=db.backref("subscribers", lazy=True),
    )

    def __init__(self, email, password, phone=None, role="member", active=True):
        self.email = email
        self.password = User.encrypt_password(password)
        self.phone = phone
        self.role = role
        self.active = active

    @classmethod
    def find_by_identity(cls, identity):
        """Find a user by their e-mail or username."""
        return User.query.filter(
            (User.email == identity) | (User.username == identity)
        ).first()

    @classmethod
    def encrypt_password(cls, plaintext_password: str) -> str:
        if plaintext_password:
            password = bcrypt.generate_password_hash(
                plaintext_password, current_app.config["BCRYPT_LOG_ROUNDS"]
            ).decode()
            return password

        return None

    @staticmethod
    def generate_auth_token(user_id, expiration: int = 3600) -> str:
        payload = {
            "exp": utils.get_current_utc_datetime()
            + timedelta(days=0, seconds=expiration),
            "iat": utils.get_current_utc_datetime(),
            "sub": user_id,
        }
        return jwt.encode(
            payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
        )

    def get_auth_token(self):
        expiration = current_app.config.get("REMEMBER_COOKIE_DURATION").total_seconds()
        return User.generate_auth_token(self.id, expiration=expiration)

    @staticmethod
    def verify_auth_token(auth_token):
        """
        Verify the auth token by returning the user assocaiated
        """
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get("SECRET_KEY"), algorithms="HS256"
            )
            user_id = payload["sub"]
        except jwt.ExpiredSignatureError:
            return None  # 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return None  # 'Invalid token. Please log in again.'

        user = User.query.get(user_id)
        return user

    def authenticated(self, with_password=True, password=""):
        """
        Ensure a user is authenticated, and optionally check their password.
        """
        if with_password:
            return bcrypt.check_password_hash(self.password, password)

        return True

    def update_activity_tracking(self, ip_address):
        """
        Update various fields on the user that's related to meta data on their
        account, such as the sign in count and ip address, etc..
        """
        self.sign_in_count += 1

        self.last_sign_in_at = self.current_sign_in_at
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_at = datetime.now(pytz.utc)
        self.current_sign_in_ip = ip_address

        return self.save()


@attrs_sqlalchemy
class BlacklistToken(Base):
    """Stores auth tokens that should be explicitly disallowed (e.g. user logged out)"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)

    @staticmethod
    def check_blacklist(auth_token: str) -> bool:
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        return bool(res)


@attrs_sqlalchemy
class Alert(Base):
    """Defines the configuration of an Alert for a User."""

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUID(as_uuid=True), unique=True, nullable=False, default=generate_uuid
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="alerts")
    notifications = db.relationship("Notification", back_populates="alert")
    name = db.Column(db.String(255), nullable=False)

    # Location information
    # SRID-4326 means degrees lat/lon
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    geom = db.Column(Geometry(geometry_type="POINT", srid=4326), index=True)
    # Units are in meters
    radius = db.Column(db.Float)

    # Time information
    timezone = db.Column(db.String(30), nullable=False)
    expires_at = db.Column(AwareDateTime)

    # Thresholds
    temperature_limit = db.Column(db.Float)  # in degrees Celcius
    relative_humidity_limit = db.Column(db.Float)  # in percentage
    wind_limit = db.Column(db.Float)  # in meters per second
    precipitation_limit = db.Column(db.Float)  # in millimeters

    # Configured Checks
    check_thunderstorms = db.Column(db.Boolean, default=False)


@attrs_sqlalchemy
class Notification(Base):
    """Corresponds to Notifications sent to users.

    Useful for preventing a user being notified multiple times per
    configured alert and for tracking the notification history.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="notifications")

    alert_id = db.Column(db.Integer, db.ForeignKey("alert.id"))
    alert = db.relationship("Alert", back_populates="notifications")

    message = db.Column(db.String)
    sent_at = db.Column(AwareDateTime)
    violates_at = db.Column(AwareDateTime)
    violated_on = db.Column(db.String)  # forecast, station, etc.

    temperature_violated = db.Column(db.Boolean)
    temperature_violated_at = db.Column(AwareDateTime)
    temperature_value = db.Column(db.Float)

    relative_humidity_violated = db.Column(db.Boolean)
    relative_humidity_violated_at = db.Column(AwareDateTime)
    relative_humidity_value = db.Column(db.Float)

    wind_violated = db.Column(db.Boolean)
    wind_violated_at = db.Column(AwareDateTime)
    wind_value = db.Column(db.Float)

    precipitation_violated = db.Column(db.Boolean)
    precipitation_violated_at = db.Column(AwareDateTime)
    precipitation_value = db.Column(db.Float)


class WeatherRaster(Base):
    id = db.Column(db.Integer, primary_key=True)

    rast = db.Column(Raster)
    filename = db.Column(db.String(255))
    source = db.Column(db.String(255))

    forecasted_at = db.Column(AwareDateTime)
    forecast_time = db.Column(AwareDateTime)


alert_subscribers = db.Table(
    "alert_subscribers",
    Base.metadata,
    db.Column("alert_id", db.Integer, db.ForeignKey("alert.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)
