import logging
import time
from enum import Enum

import click_log

from fwas import crud
from fwas.config import SQLALCHEMY_DATABASE_URI
from fwas.database import Database
from fwas.serialize import NotificationIn

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


class Bands(Enum):
    reflectivity = 1
    lightening = 2
    temperature = 4
    relative_humidity = 5
    wind = 6
    precipitation = 7


async def check_alerts():
    """
    1. Retrieve alert
    2. Create a buffer around the alert location with radius
    3. Compute the band min/max values within that radius
    4. Check values against preconfigured alert thresholds
    5. Record violations and queue notifications to be sent
    """
    with Database(SQLALCHEMY_DATABASE_URI) as db:
        start = time.time()

        # find contains all current and future times where the
        # configured alert thresholds are violated by the
        # the weather data for active alert definitions.
        rows = crud.find_alert_violations()

        # create notifications with the details of the violations
        notifications = []
        for row in rows:
            params = dict(row)
            params[
                "violated_on"
            ] = "forecast"  # TODO (lmalott): Compute this from something
            notification = NotificationIn(**params).dict()
            notifications.append(notification)

        await crud.create_user_notifications(db, notifications)

        # TODO (lmalott): remove persistent violations keeping only the first violation
        # may need separate `violates_at` timestamps for each weather data type
        # e.g. `temperture_violates_at`.

        end = time.time()
        logger.info(f"Completed check_alerts in {end - start} seconds")

        return notifications
