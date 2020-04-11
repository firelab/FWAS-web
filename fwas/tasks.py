"""
Scheduled and background tasks for FWAS.
"""
from loguru import logger
from redis import Redis
from rq_scheduler import Scheduler

from fwas.config import REDIS_URL
from fwas.fetchers import hrrr
from fwas.notify import check_alerts


def schedule_jobs():
    scheduler = Scheduler(connection=Redis.from_url(REDIS_URL))

    scheduler.cron(
        "*/5 * * * *",
        func=check_alerts,
        description="Create notifications for violated alerts.",
        repeat=None,
        queue_name="default",
    )

    scheduler.cron(
        "10 * * * *",  # 10 minutes past the hour every hour
        func=hrrr.run_now,
        description="Update database with latest HRRR data",
        repeat=None,
        queue_name="default",
        timeout=600,
    )


def clear_scheduled_jobs():
    # Delete any existing jobs in the scheduler when the app starts up
    scheduler = Scheduler(connection=Redis())
    for job in scheduler.get_jobs():
        logger.debug("Deleting scheduled job %s", job)
        job.delete()
