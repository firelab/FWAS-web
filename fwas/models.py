from datetime import datetime
from uuid import uuid4

from attrs_sqlalchemy import attrs_sqlalchemy
from flask import current_app
from geoalchemy2.types import Geometry, Raster
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.dialects.postgresql import UUID

from .database import db
from .encryption import bcrypt


def generate_uuid():
    return str(uuid4())


class TimeStampMixin(object):
    """Timestamping mixin for generating created_at and updated_at columns."""

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at._creation_order = 9998
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        db.event.listen(cls, "before_update", cls._updated_at)


class Base(db.Model, TimeStampMixin):
    __abstract__ = True


@attrs_sqlalchemy
class User(Base):
    """User of the application and their contact information."""

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUID(as_uuid=True), unique=True, nullable=False, default=generate_uuid
    )
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    phone = db.Column(db.String(12))

    alerts = db.relationship("Alert", back_populates="user")
    notifications = db.relationship("Notification", back_populates="user")

    def __init__(self, email, password, phone=None, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config["BCRYPT_LOG_ROUNDS"]
        ).decode()
        self.admin = admin
        self.phone = phone

    def generate_auth_token(self, expiration: int = 600) -> str:
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_auth_token(token: str):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data["id"])
        return user


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

    # Location information
    # SRID-4326 means degrees lat/lon
    latitude = db.Column(db.Float, nullable=False)
    longtitude = db.Column(db.Float, nullable=False)
    geom = db.Column(Geometry(geometry_type="POINT", srid=4326), index=True)
    # Units are in meters
    radius = db.Column(db.Float)

    # Time information
    timezone = db.Column(db.String(30), nullable=False)
    expires_in_hours = db.Column(db.Float, nullable=False)
    expires_at = db.Column(db.DateTime)

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
    uuid = db.Column(
        UUID(as_uuid=True), unique=True, nullable=False, default=generate_uuid
    )

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="notifications")

    alert_id = db.Column(db.Integer, db.ForeignKey("alert.id"))
    alert = db.relationship("Alert", back_populates="notifications")

    message = db.Column(db.String)
    sent_at = db.Column(db.DateTime)
    violates_at = db.Column(db.DateTime)
    violated_on = db.Column(db.String)  # forecast, station, etc.

    temperature_violated = db.Column(db.Boolean)
    temperature_violated_at = db.Column(db.DateTime)
    temperature_value = db.Column(db.Float)

    relative_humidity_violated = db.Column(db.Boolean)
    relative_humidity_violated_at = db.Column(db.DateTime)
    relative_humidity_value = db.Column(db.Float)

    wind_violated = db.Column(db.Boolean)
    wind_violated_at = db.Column(db.DateTime)
    wind_value = db.Column(db.Float)

    precipitation_violated = db.Column(db.Boolean)
    precipitation_violated_at = db.Column(db.DateTime)
    precipitation_value = db.Column(db.Float)


class WeatherRaster(Base):
    id = db.Column(db.Integer, primary_key=True)

    rast = db.Column(Raster)
    filename = db.Column(db.String(255))
    source = db.Column(db.String(255))

    forecasted_at = db.Column(db.DateTime)
    forecast_time = db.Column(db.DateTime)
