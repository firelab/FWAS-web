import os
from importlib.resources import path as resource_path
from typing import List, Optional

import aiofiles
from geoalchemy2.elements import WKTElement
from loguru import logger

from fwas import models
from fwas.database import Database, database
from fwas.serialize import (
    AlertIn,
    AlertInDb,
    NotificationIn,
    NotificationInDb,
    UserIn,
    UserInDb,
    WeatherRasterInDb,
)

with resource_path("fwas", "queries") as path:
    QUERY_TEMPLATE_DIR = path


async def query_file(filename: str, **params):
    abs_path = os.path.join(QUERY_TEMPLATE_DIR, filename)
    if not os.path.exists(abs_path):
        raise IOError(f"{abs_path} does not exist.")

    sql_content = None
    async with aiofiles.open(abs_path, "r") as fh:
        sql_content = await fh.read()
        sql_content = sql_content.strip()

    return await database.execute(sql_content, values=params)


def get_nearest_alert(lat, lon):
    # find the nearest point to the input coordinates
    # convert the input coordinates to a WKT point and query for nearest point
    pt = WKTElement("POINT({0} {1})".format(lon, lat), srid=4326)
    return models.Alert.query.order_by(models.Alert.geom.distance_box(pt)).first()


async def get_user(db: Database, user_id: int) -> Optional[UserInDb]:
    query = "select * from users where id=:user_id"
    row = await db.fetch_one(query, values={"user_id": user_id})
    return UserInDb(**row) if row else row


async def create_user(db: Database, info: UserIn) -> int:
    query = models.t_users.insert()
    user_id = await db.execute(query, values=info.dict())

    return user_id


async def get_user_by_email(db: Database, email: str) -> Optional[UserInDb]:
    query = "select * from users where email = :email"
    row = await db.fetch_one(query, values={"email": email})
    return UserInDb(**row) if row else row


async def get_user_by_username(db: Database, username: str) -> Optional[UserInDb]:
    query = "select * from users where username = :username"
    row = await db.fetch_one(query, values={"username": username})
    return UserInDb(**row) if row else row


async def get_user_by_identity(db: Database, identity: str) -> Optional[UserInDb]:
    """Find a user by their e-mail or username."""
    query = "select * from users where email = :identity or username = :identity"
    row = await db.fetch_one(query, values={"identity": identity})
    return UserInDb(**row) if row else row


async def get_user_alerts(
    db: Database, user_id: int, since: str = None
) -> List[AlertInDb]:
    query = "select * from alerts where user_id=:user_id"
    values = {"user_id": user_id}

    if since is not None:
        query += "  and created_at >= :since"
        values["since"] = since

    rows = await db.fetch_all(query, values=values)
    return [AlertInDb(**row) for row in rows if row]


async def create_alert_for_user(db: Database, user_id: int, alert: AlertIn) -> int:
    query = models.t_alerts.insert()
    values = alert.dict()
    values['user_id'] = user_id
    values['geom'] = WKTElement(f"POINT({alert.longitude} {alert.latitude})", srid=4326)

    return await db.execute(query, values=values)


async def get_alert_by_id(db: Database, alert_id: int) -> AlertInDb:
    query = "select * from alerts where id=:alert_id"
    row = await db.fetch_one(query, values={'alert_id': alert_id})
    logger.info(dict(**row))
    return AlertInDb(**row)


async def get_user_notifications(
    db: Database, user_id: int, skip: int = 0, limit: int = 10
) -> List[NotificationInDb]:
    query = (
        "select * from notifications where user_id=:user_id offset :skip limit :limit"
    )
    rows = await db.fetch_all(
        query, values={"user_id": user_id, "skip": skip, "limit": limit}
    )
    return [NotificationInDb(**row) for row in rows if row]


async def create_user_notification(db: Database, notification: NotificationIn) -> int:
    query = models.t_notifications.insert()
    return await db.execute(query, values=notification.dict())


async def create_user_notifications(db: Database, notifications: List[NotificationIn]):
    query = models.t_notifications.insert()
    return await db.execute_many(query, values=notifications)


async def get_weather_rasters_by_filename(db: Database, filename: str):
    query = "select * from weather_rasters where filename=:filename"
    rows = await db.fetch_all(query, values={"filename": filename})
    return [WeatherRasterInDb(**row) for row in rows if row]


async def update_weather_raster(db: Database, weather_raster: WeatherRasterInDb):
    query = """
    update weather_rasters set
        filename=:filename,
        rast=:rast,
        source=:source,
        forecasted_at=:forecasted_at,
        forecast_time=:forecast_time
    where id = :id
    """
    return await db.execute(query, values=weather_raster.dict())


def get_alert_buffers(db: Database):
    query = """
    select id, st_buffer(geom, radius)
    from alert
    """
    return db.fetch_all(query)


def get_clipped_alert_band(band):
    return query_file("clipped_alert_band.sql", band=band)


def compute_clipped_bands_stats(band):
    return query_file("clipped_band_stats.sql", band=band)


def find_alert_violations():
    return query_file("find_alert_violations.sql")
