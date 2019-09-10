from geoalchemy2.elements import WKTElement

from . import models


def get_nearest_alert(lat, lon):
    # find the nearest point to the input coordinates
    # convert the input coordinates to a WKT point and query for nearest point
    pt = WKTElement("POINT({0} {1})".format(lon, lat), srid=4326)
    return models.Alert.query.order_by(models.Alert.geom.distance_box(pt)).first()
