import os
import redis

from .worker import celery

redis_store = redis.Redis.from_url(os.getenv("REDIS_URL"))


@celery.task
def parse_data():
    pass
