
import os
from time import sleep

from celery import Celery
from kombu import Queue, Exchange, binding
import redis
from redbeat.schedulers import RedBeatConfig

from jmon.logger import logger
from jmon.runner import Runner
import jmon.models

redis_url = f"{os.environ.get('REDIS_TYPE')}://{os.environ.get('REDIS_USERNAME')}:{os.environ.get('REDIS_PASSWORD')}@{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/{os.environ.get('REDIS_INSTANCE')}"
broker_url = f"{os.environ.get('BROKER_TYPE')}://{os.environ.get('BROKER_USERNAME')}:{os.environ.get('BROKER_PASSWORD')}@{os.environ.get('BROKER_HOST')}:{os.environ.get('BROKER_PORT')}/{os.environ.get('BROKER_INSTANCE')}"

app = Celery(
    "server",
    backend=redis_url,
    broker=broker_url
)

app.conf.task_default_queue = 'default'

task_exchange = Exchange('task', type='direct')
check_exchange = Exchange('check', type='headers')

app.conf.task_queues = (
    Queue('default', exchange=task_exchange, routing_key='task.default'),
    Queue(
        'requests',
        bindings=[
            binding(exchange=check_exchange, arguments={'x-match': 'any', 'requests': 'true'})
        ]
    ),
    Queue(
        'firefox',
        bindings=[
            binding(exchange=check_exchange, arguments={'x-match': 'any', 'firefox': 'true'})
        ]
    ),
    Queue(
        'chrome',
        exchange=check_exchange,
        bindings=[
            binding(exchange=check_exchange, arguments={'x-match': 'any', 'chrome': 'true'})
        ]
    )
)
app.conf.task_default_exchange = task_exchange.name
app.conf.task_default_exchange_type = task_exchange.type
app.conf.task_default_routing_key = 'task.default'

# Setup default redbeat config
app.conf.redbeat_redis_url = redis_url
app.redbeat_conf = RedBeatConfig(app=app)

logger.info("Imported jmon")
