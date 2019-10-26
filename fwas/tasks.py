"""
Scheduled and background tasks for FWAS.
"""
from redis import Redis

from rq_scheduler import Scheduler

from .notify import check_alerts


def schedule_jobs():
    scheduler = Scheduler(connection=Redis())

    scheduler.cron(
        "0 * * * *",  # at every hour
        func=check_alerts,
        repeat=None,
        queue_name="default",
        meta={"foo": "bar"},
        use_local_timezone=False,
    )
