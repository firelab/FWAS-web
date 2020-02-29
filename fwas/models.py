from enum import Enum
from collections import OrderedDict
from datetime import datetime, timedelta
from uuid import uuid4

import jwt
import pytz
from geoalchemy2.types import Geometry, Raster
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import DateTime, TypeDecorator
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    Table,
    Text,
    text,
    CheckConstraint,
    MetaData,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql.base import ENUM, UUID

from fwas import config, utils


metadata = MetaData()


UUID_DEFAULT = text("uuid_generate_v4()")
CURRENT_TIME = text("(now() at time zone 'utc')")


class Roles(str, Enum):
    MEMBER = "member"
    ADMIN = "admin"


class AwareDateTime(TypeDecorator):
    impl = DateTime(timezone=True)

    def process_bind_params(self, value, dialect):
        if isinstance(value, datetime) and value.tzinfo is None:
            raise ValueError(f"{value} must be timezone-aware.")
        return value

    def __repr__(self):
        return "AwareDateTime()"


t_blacklist_tokens = Table(
    "blacklist_tokens",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        server_default=text("nextval('blacklist_tokens_id_seq'::regclass)"),
    ),
    Column("token", String(500), nullable=False, unique=True),
)


t_users = Table(
    "users",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        server_default=text("nextval('users_id_seq'::regclass)"),
    ),
    Column("username", String(50), unique=True),
    Column("email", String(255), nullable=False, unique=True),
    Column("password", String(128), nullable=False),
    Column("is_active", Boolean, nullable=False, server_default=text("true")),
    Column("phone", String(12)),
    Column("sign_in_count", Integer, nullable=False, default=0),
    Column("current_sign_in_at", AwareDateTime),
    Column("current_sign_in_ip", String(45)),
    Column("last_sign_in_at", AwareDateTime),
    Column("last_sign_in_ip", String(45)),
    Column(
        "role",
        ENUM(*[code.value for code in Roles], name="role_code"),
        nullable=False,
        index=True,
        server_default=text("'member'::character varying"),
    ),
    Column("created_at", AwareDateTime, server_default=CURRENT_TIME),
    Column(
        "updated_at",
        AwareDateTime,
        server_default=CURRENT_TIME,
        server_onupdate=CURRENT_TIME,
    ),
)


t_weather_rasters = Table(
    "weather_rasters",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        server_default=text("nextval('weather_rasters_id_seq'::regclass)"),
    ),
    Column("rast", Raster),
    Column("filename", String(255)),
    Column("source", String(255)),
    Column("forecasted_at", AwareDateTime),
    Column("forecast_time", AwareDateTime),
    Column("created_at", AwareDateTime, server_default=CURRENT_TIME),
    Column(
        "updated_at",
        AwareDateTime,
        server_default=CURRENT_TIME,
        server_onupdate=CURRENT_TIME,
    ),
)


t_alerts = Table(
    "alerts",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        server_default=text("nextval('alerts_id_seq'::regclass)"),
    ),
    Column("uuid", UUID, nullable=False, unique=True, server_default=UUID_DEFAULT),
    Column("user_id", ForeignKey("users.id")),
    Column("name", String(255), nullable=False),
    Column("latitude", Float(53), nullable=False),
    Column("longitude", Float(53), nullable=False),
    Column("geom", Geometry("POINT", 4326), index=True),
    Column("radius", Float(53)),
    Column("timezone", String(30), nullable=False),
    Column("expires_at", AwareDateTime),
    Column("temperature_limit", Float(53)),
    Column("relative_humidity_limit", Float(53)),
    Column("wind_limit", Float(53)),
    Column("precipitation_limit", Float(53)),
    Column("check_thunderstorms", Boolean),
    Column("created_at", AwareDateTime, server_default=CURRENT_TIME),
    Column(
        "updated_at",
        AwareDateTime,
        server_default=CURRENT_TIME,
        server_onupdate=CURRENT_TIME,
    ),
)


t_alert_subscribers = Table(
    "alert_subscribers",
    metadata,
    Column("alert_id", ForeignKey("alerts.id"), primary_key=True, nullable=False),
    Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
)


t_notifications = Table(
    "notifications",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        server_default=text("nextval('notifications_id_seq'::regclass)"),
    ),
    Column("user_id", ForeignKey("users.id")),
    Column("alert_id", ForeignKey("alerts.id")),
    Column("message", String),
    Column("sent_at", AwareDateTime),
    Column("violates_at", AwareDateTime),
    Column("violated_on", String),
    Column("temperature_violated", Boolean),
    Column("temperature_violated_at", AwareDateTime),
    Column("temperature_value", Float(53)),
    Column("relative_humidity_violated", Boolean),
    Column("relative_humidity_violated_at", AwareDateTime),
    Column("relative_humidity_value", Float(53)),
    Column("wind_violated", Boolean),
    Column("wind_violated_at", AwareDateTime),
    Column("wind_value", Float(53)),
    Column("precipitation_violated", Boolean),
    Column("precipitation_violated_at", AwareDateTime),
    Column("precipitation_value", Float(53)),
    Column("created_at", AwareDateTime, server_default=CURRENT_TIME),
    Column(
        "updated_at",
        AwareDateTime,
        server_default=CURRENT_TIME,
        server_onupdate=CURRENT_TIME,
    ),
)
