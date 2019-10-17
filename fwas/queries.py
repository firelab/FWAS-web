import os
from importlib.resources import path as resource_path

from geoalchemy2.elements import WKTElement

from . import models
from .database import conn, db

with resource_path("fwas", "queries") as path:
    QUERY_TEMPLATE_DIR = path


def query_file(filename: str, **params):
    abs_path = os.path.join(QUERY_TEMPLATE_DIR, filename)

    return conn.query_file(abs_path, **params)


def get_nearest_alert(lat, lon):
    # find the nearest point to the input coordinates
    # convert the input coordinates to a WKT point and query for nearest point
    pt = WKTElement("POINT({0} {1})".format(lon, lat), srid=4326)
    return models.Alert.query.order_by(models.Alert.geom.distance_box(pt)).first()


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
