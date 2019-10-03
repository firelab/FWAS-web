from geoalchemy2.elements import WKTElement

from . import models
from .database import db


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
    # TODO(lmalott) parameterize this to select specific rasters
    # TODO(lmalott) parameterize to select specific raster bands
    query = f"""
    with alert_buffers as (
        select id, st_buffer(geom::geography, radius) as geom from alert
    ),
    data as (
        select id, st_band(rast, {band}) as rast from weather_raster
    )

    select
        a.id as alert_id,
        d.id as raster_id,
        st_clip(d.rast, a.geom) as rast
    from alert_buffers as a, data as d
    where st_intersects(d.rast, a.geom::geometry)
    """
    results = db.engine.execute(query)
    return [result[0] for result in results]


def compute_clipped_bands_stats(band):
    query = f"""
    with alert_buffers as (
        select id, st_buffer(geom::geography, radius) as geom from alert
    ),
    data as (
        select id, st_band(rast, {band}) as rast from weather_raster
    ),
    raster_stats as (
        select
            a.id as alert_id,
            d.id as raster_id,
            st_summarystats(st_union(st_clip(d.rast, a.geom, true))) as stats
        from alert_buffers as a, data as d
        where st_intersects(d.rast, a.geom::geometery)
        group by alert_id, raster_id
    )

    select
        alert_id,
        raster_id,
        (stats).max,
        (stats).mean,
        (stats).min
    from raster_stats
    """
    results = db.engine.execute(query)
    return [result[0] for result in results]
