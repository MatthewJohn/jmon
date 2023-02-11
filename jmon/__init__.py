
import os
from time import sleep

from celery import Celery
import redis

from jmon.runner import Runner
import jmon.models


broker_url = f"{os.environ.get('BROKER_TYPE')}://{os.environ.get('BROKER_USERNAME')}:{os.environ.get('BROKER_PASSWORD')}@{os.environ.get('BROKER_HOST')}:{os.environ.get('BROKER_PORT')}/{os.environ.get('BROKER_INSTANCE')}"

app = Celery(
    "server",
    backend=broker_url,
    broker=broker_url
)


@app.task()
def perform_check(check_name):
    # Get config for check
    check = jmon.models.Check.query.filter(jmon.models.Check.name==check_name).first()
    if not check:
        raise Exception("Could not find check")

    runner = Runner()
    runner.perform_check(check.steps)
    # print("PRetending", config)
    return True
