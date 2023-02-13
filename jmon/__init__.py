
import os
from time import sleep

from celery import Celery
import redis
from redbeat.schedulers import RedBeatConfig

from jmon.runner import Runner
import jmon.models


broker_url = f"{os.environ.get('BROKER_TYPE')}://{os.environ.get('BROKER_USERNAME')}:{os.environ.get('BROKER_PASSWORD')}@{os.environ.get('BROKER_HOST')}:{os.environ.get('BROKER_PORT')}/{os.environ.get('BROKER_INSTANCE')}"

app = Celery(
    "server",
    backend=broker_url,
    broker=broker_url
)

# Setup default redbeat config
app.redbeat_conf = RedBeatConfig(app=app)
