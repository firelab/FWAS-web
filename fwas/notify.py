from enum import Enum

from . import queries


class Bands(Enum):
    reflectivity = 1
    lightening = 2
    temperature = 4
    relative_humidity = 5
    wind = 6
    precipitation = 7


def check_alerts():
    """
    1. Retrieve alert
    2. Create a buffer around the alert location with radius
    3. Compute the band min/max values within that radius
    4. Check values against preconfigured alert thresholds
    5. Record violations and queue notifications to be sent
    """
    rows = queries.find_alert_violations()
    df = rows.export("df")

    # check temperature violations
    # Alert is generated of max temperature within the radius
    # exceeds the temperature threshold as defined by the user.
    filtered = df[df.temperature_limit.notnull()]
    temperature_df = filtered.where(
        filtered.temperature_max >= filtered.temperature_limit
    )
    return temperature_df

    # create notifications with the details of the violations
