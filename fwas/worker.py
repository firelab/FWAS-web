import os

import redis
from rq import Connection, Queue, Worker

listen = ["default"]
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
connection = redis.from_url(redis_url)


def run_worker():
    with Connection(connection):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
