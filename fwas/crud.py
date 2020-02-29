import os
from typing import Optional
from importlib.resources import path as resource_path

from geoalchemy2.elements import WKTElement

from fwas import models
from fwas.database import database, Database
from fwas.serialize import UserInDb


with resource_path("fwas", "queries") as path:
    QUERY_TEMPLATE_DIR = path


def run_sql(filename: str, **params):
    abs_path = os.path.join(QUERY_TEMPLATE_DIR, filename)
    if not os.path.exists(abs_path):
        raise IOError(f"{abs_path} does not exist.")

    sql_content = None
    with open(abs_path, "r") as fh:
        sql_content = fh.read().strip()

    return database.execute(sql_content, **params)


def get_nearest_alert(lat, lon):
    # find the nearest point to the input coordinates
    # convert the input coordinates to a WKT point and query for nearest point
    pt = WKTElement("POINT({0} {1})".format(lon, lat), srid=4326)
    return models.Alert.query.order_by(models.Alert.geom.distance_box(pt)).first()


def get_user(user_id):
    user = conn.query("select * from public.user where id=:user_id", user_id=user_id)
    return user.first()


def get_user_by_email(email):
    user = conn.query("select * from public.user where email=:email", email=email)
    return user.first()


async def get_user_by_identity(db: Database, identity: str) -> Optional[UserInDb]:
    """Find a user by their e-mail or username."""
    query = "select * from users where email = :identiy or username = :identiiy"
    row = await db.fetch_one(query, values={"identity": identity})
    return UserInDb(**row) if row else row


def get_user_alerts(user_id, since=None):
    query = """
      select
        *
      from alert
      where user_id=:user_id
    """
    if since is not None:
        query += "  and created_at >= :since"

    alerts = conn.query(query, user_id=user_id, since=since)
    return alerts


def check_blacklist(auth_token: str) -> bool:
    res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
    return bool(res)


def get_user_notifications(user_id):
    notifications = conn.query_file("get_user_notifications.sql", user_id=user_id)
    return notifications.all()


def get_alert_buffers():
    query = """
    select id, st_buffer(geom, radius)
    from alert
    """
    results = db.engine.execute(query)
    return [result[0] for result in results]


def get_clipped_alert_band(band):
    return query_file("clipped_alert_band.sql", band=band)


def compute_clipped_bands_stats(band):
    return query_file("clipped_band_stats.sql", band=band)


def find_alert_violations():
    return query_file("find_alert_violations.sql")
