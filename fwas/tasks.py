"""
Scheduled and background tasks for FWAS.
"""
from redis import Redis
from rq_scheduler import Scheduler

from .fetchers import hrrr
from .notify import check_alerts


def schedule_jobs():
    scheduler = Scheduler(connection=Redis())

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
    )
