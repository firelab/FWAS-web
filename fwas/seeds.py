from geoalchemy2.elements import WKTElement

from fwas import db
from fwas.models import Alert, User


def create_seeds():
    user = User(
        username="levi",
        email="levi.malott@gmail.com",
        phone="123-456-7890",
        carrier="T-Mobile",
    )

    lat = 38.6247
    lon = 90.1854
    pt = WKTElement(f"POINT({lon} {lat})", srid=4326)
    alert = Alert(user=user, geom=pt, timezone="tbd", expires_in_hours=6.0)

    db.session.add_all([user, alert])
    db.session.commit()
