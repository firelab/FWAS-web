import asyncio
import logging
import os
import tempfile
from datetime import datetime

import click_log
from invoke import run

from ..database import db
from ..models import WeatherRaster
from . import utils
from .base import Fetcher

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


class ConusFetcher(Fetcher):
    def __init__(self):
        self.tempdir = None

    def download(self):
        """
        Download the National Mosaic, corresponding worldfile, and timestamps.

        https://www.weather.gov/jetstream/gis
        """
        if self.tempdir is None:
            self.tempdir = tempfile.mkdtemp()

        logger.info(f"tempdir created: {self.tempdir}")

        logger.info("Fetching CONUS RADAR and TimeList...")
        loop = asyncio.get_event_loop()
        tasks = [
            utils.download(url, os.path.join(self.tempdir, output_file))
            for (url, output_file) in [
                (
                    "https://radar.weather.gov/ridge/Conus/RadarImg/latest_radaronly.gif",
                    "conus_radar.gif",
                ),
                (
                    "https://radar.weather.gov/ridge/Conus/RadarImg/latest_radaronly.gfw",
                    "conus_radar.gfw",
                ),
                (
                    "https://radar.weather.gov/ridge/Conus/RadarImg/mosaic_times.txt",
                    "mosaic_times.txt",
                ),
            ]
        ]
        group = asyncio.gather(*tasks)
        loop.run_until_complete(group)

    def transform(self):
        logger.info("Entering transform phase")

        # Convert .gif file to EPSG:4326 projection and store into database
        path = os.path.join(self.tempdir, "conus_radar.gif")
        output_sql = path.replace(".gif", ".sql")
        # output_path = os.path.join(self.tempdir, "conus_radar_epsg_4326.gif")

        # TODO (lmalott): Confirm the project for the GIF files to make sure
        # it's compatible with the other rasters (EPSG:4326)
        #        logger.info(f"Converting {path} to EPSG:4326 at {output_path}")
        #        run(f"gdalwarp -t_srs EPSG:4326 {path} {output_path}")
        run(
            f"raster2pgsql -I -M -F -s 4326 -t auto -a {path} weather_raster > {output_sql}"
        )

        logger.info("Leaving transform phase")

    def save(self):
        logger.info("Entering save phase.")

        db_url = os.getenv("DATABASE_URL")
        path = os.path.join(self.tempdir, "conus_radar.sql")

        run(f"psql {db_url} -f {path}")
        current_datetime = datetime.utcnow()
        current_hour = current_datetime.replace(microsecond=0, second=0, minute=0)

        for weather_raster in WeatherRaster.query.filter_by(
            filename="conus_radar.gif", created_at=None
        ):
            weather_raster.source = "conus"
            weather_raster.created_at = current_datetime
            weather_raster.updated_at = current_datetime
            weather_raster.forecasted_at = current_hour
            weather_raster.forecast_time = current_hour
            db.session.add(weather_raster)
            db.session.commit()

        logger.info("Leaving save phase.")

    def cleanup(self):
        pass
