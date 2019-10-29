from datetime import datetime
from uuid import uuid4

from attrs_sqlalchemy import attrs_sqlalchemy
from geoalchemy2.types import Geometry, Raster
from sqlalchemy.dialects.postgresql import UUID

from .database import db


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
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(12))
    carrier = db.Column(db.String(15))

    alerts = db.relationship("Alert", back_populates="user")
    notifications = db.relationship("Notification", back_populates="user")


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


@attrs_sqlalchemy
class WeatherSource(Base):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUID(as_uuid=True), unique=True, nullable=False, default=generate_uuid
    )

    type = db.Column(db.String(80))
    rasters = db.relationship("WeatherRaster", back_populates="source")


class WeatherRaster(Base):
    id = db.Column(db.Integer, primary_key=True)

    source_id = db.Column(db.Integer, db.ForeignKey("weather_source.id"))
    source = db.relationship("WeatherSource", back_populates="rasters")

    rast = db.Column(Raster)
    filename = db.Column(db.String(255))

    forecasted_at = db.Column(db.DateTime)
    forecast_time = db.Column(db.DateTime)
