import logging
import os
import shutil
import tempfile
import time
from datetime import datetime, timedelta
from urllib.request import urlopen

import click_log
from invoke import run

from .base import Fetcher

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


class HrrrFetcher(Fetcher):
    def __init__(self):
        self.tempdir = None

    def download(self):
        self.tempdir = tempfile.mkdtemp()
        logger.info(f"tempdir created: {self.tempdir}")
        start_hour = datetime.utcnow().hour - 1

        for forecast_hour in range(1, 8):
            logger.info(f"Downloading forecast hour {forecast_hour}")
            start = time.time()
            url = build_url(start_hour, forecast_hour)

            output_file = os.path.join(
                self.tempdir, url[url.find("file=") + 5 : url.find(".grib2")] + ".grib2"
            )
            logger.info(f"Saving forecast data to {output_file}")

            with urlopen(url) as response:
                with open(output_file, "wb") as tmp_file:
                    shutil.copyfileobj(response, tmp_file)

            end = time.time()
            logger.info(f"Download complete in {end - start} seconds")

    def transform(self):
        """Convert each grib2 file into SRID 4326. The latter is suitable
        for storage into PostGIS."""
        logger.info("Entering transform phase")
        for grib in os.listdir(self.tempdir):
            path = os.path.join(self.tempdir, grib)
            output_path = os.path.join(self.tempdir, path.replace(".grib2", ".vrt"))
            logger.info(f"Converting {path} to EPSG:4326 at {output_path}")
            run(f"gdalwarp -t_srs EPSG:4326 {path} {output_path}")
            logger.info(f"Removing {path}")
            shutil.remove(path)

        logger.info("Leaving transform phase")

    def save(self):
        """Load each .vrt file from tempdir into PostGIS"""
        pass

    def cleanup(self):
        shutil.rmtree(self.tempdir)


def build_url(start_hour: int, forecast_hour: int) -> str:
    """
    Builds the most recent URL for HRRR Data

    Args:
        start_hour: Which hour to retrieve HRRR data from. The day is pulled
                    from calling `utcnow()`.
        forecase_hour: Which hour of forecast data to retrieve.

    Returns:
        str: URL of the HRRR grib file to download.
    """
    # If the start_hour is negative, assume that the most recent HRRR data
    # is from the last hour of yesterday.
    if start_hour == -1:
        start_hour = 23
        day = (datetime.utcnow() - timedelta(days=1)).strftime("%Y%m%d")
    else:
        day = datetime.utcnow().strftime("%Y%m%d")

    base_url = "http://nomads.ncep.noaa.gov/cgi-bin/filter_hrrr_2d.pl"
    source_file = f"?file=hrrr.t{start_hour:02}z.wrfsfcf{forecast_hour:02}.grib2"
    params = """&lev_surface=on&lev_10_m_above_ground=on&lev_2_m_above_ground=on\
&lev_entire_atmosphere=on&var_REFC=on&var_RH=on\
&var_TMP=on&var_PRATE=on&var_LTNG=on&var_WIND=on\
&leftlon=0&rightlon=360&toplat=90\
&bottomlat=-90&dir=%2Fhrrr."""

    url = base_url + source_file + params + day + "%2Fconus"
    return url
