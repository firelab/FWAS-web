from datetime import datetime

from attrs_sqlalchemy import attrs_sqlalchemy
from geoalchemy2.types import Geometry

from .database import db


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
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(12))
    carrier = db.Column(db.String(15))

    alerts = db.relationship("Alert", back_populates="user")


@attrs_sqlalchemy
class Alert(Base):
    """Defines the configuration of an Alert for a User."""

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="alerts")

    # Location information
    # SRID-4326 means degrees lat/lon
    geom = db.Column(Geometry(geometry_type="POINT", srid=4326), index=True)
    # Units are in meters
    radius = db.Column(db.Float)

    # Time information
    timezone = db.Column(db.String(30), nullable=False)
    expires_in_hours = db.Column(db.Float, nullable=False)
    expires_at = db.Column(db.DateTime)


@attrs_sqlalchemy
class Notification(Base):
    """Corresponds to Notifications sent to users.

    Useful for preventing a user being notified multiple times per
    configured alert and for tracking the notification history.
    """

    id = db.Column(db.Integer, primary_key=True)
