import datetime

from geoalchemy2.types import Geometry

from .database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(12))
    carrier = db.Column(db.String(15))


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(80))

    # Location information
    # SRID-4326 means degrees lat/lon
    geom = db.Column(Geometry(geometry_type="POINT", srid=4326), index=True)
    # Units are in meters
    radius = db.Column(db.Float)

    # Time information
    timezone = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
