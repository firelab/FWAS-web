from geoalchemy2.elements import WKTElement

from fwas import db
from fwas.models import Alert, User


def create_seeds():
    _ = User(email="levi.malott@gmail.com", password="secret", phone="123-456-7890")
    user = User(email="levi.malott+2@gmail.com", password="test", phone="123-456-7890")

    lat = 38.6247
    lon = -90.1854
    pt = WKTElement(f"POINT({lon} {lat})", srid=4326)
    alert = Alert(
        user=user,
        latitude=lat,
        longtitude=lon,
        geom=pt,
        radius=20000.0,
        timezone="America/Chicago",
        expires_in_hours=6.0,
        temperature_limit=0.0,  # celcius
        precipitation_limit=5,  # inches
        relative_humidity_limit=80.0,  # percent
        wind_limit=1.0,  # meters / second
    )

    alert2 = Alert(
        user=user,
        latitude=lat,
        longtitude=lon,
        geom=pt,
        radius=50000.0,
        timezone="America/Chicago",
        expires_in_hours=6.0,
        temperature_limit=20.0,  # celcius
        precipitation_limit=1.0,  # inches
        relative_humidity_limit=90.0,  # percent
        wind_limit=1.0,  # meters / second
    )

    db.session.add_all([user, alert, alert2])
    db.session.commit()
