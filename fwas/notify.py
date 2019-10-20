import logging
import time
from enum import Enum

import click_log

from . import queries
from .models import Notification

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


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
    start = time.time()

    # find contains all current and future times where the
    # configured alert thresholds are violated by the
    # the weather data for active alert definitions.
    rows = queries.find_alert_violations()

    # create notifications with the details of the violations
    notifications = []
    for row in rows:
        # rows contains entries for the same user and alert across multiple
        # hours.
        # two conditions: violated at current time or forecasted to violate

        # TODO (lmalott): find out if we need to worry about setting a
        # time horizon limit (e.g. "only notify me about alert violations
        # within an hour of the current time") or something.
        notification = Notification(
            user_id=row.user_id,
            alert_id=row.alert_id,
            violates_at=row.forecast_time,
            violated_on="forecast",  # TODO (lmalott): Compute this from something
            reflectivity_violated=row.reflectivity_violated,
            reflectivity_value=row.reflectivity_max,
            temperature_violated=row.temperature_violated,
            temperature_value=row.temperature_max,
            relative_humidity_violated=row.relative_humidity_violated,
            relative_humidity_value=row.relative_humidity_value,
            wind_violated=row.wind_violated,
            wind_value=row.wind_value,
            precipitation_violated=row.precipitation_violated,
            precipitation_value=row.precipitation_value,
        )
        notifications.append(notification)

    # TODO (lmalott): remove persistent violations keeping only the first violation
    # may need separate `violates_at` timestamps for each weather data type
    # e.g. `temperture_violates_at`.

    end = time.time()
    logger.info(f"Completed check_alerts in {end - start} seconds")
