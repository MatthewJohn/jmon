
import os
from time import sleep

from celery import Celery
import redis

from jmon.runner import Runner

broker_url = f"{os.environ.get('BROKER_TYPE')}://{os.environ.get('BROKER_USERNAME')}:{os.environ.get('BROKER_PASSWORD')}@{os.environ.get('BROKER_HOST')}:{os.environ.get('BROKER_PORT')}/{os.environ.get('BROKER_INSTANCE')}"

app = Celery(
    "server",
    backend=broker_url,
    broker=broker_url
)

example_config = {'name': 'Terrareg', 'steps': [{'goto': 'https://local-dev.dock.studio'}, {'check': {'repsonse': 200, 'title': 'Home - Terrareg'}}, {'type': {'id': 'navBarSearchInput', 'text': 'aws'}}, {'click': {'id': 'navBarSearchButton'}}, {'check': {'url': 'https://local-dev.dock.studio/modules/search?q=aws'}}, {'click': {'id': 'modulesearch-trusted.mixedsearch-trusted-result.aws.1.0.0', 'find': {'class': 'module-card-title'}}}]}


@app.on_after_configure.connect
def schedule_periodic_tasks(sender, **kwargs):
    # Checking weather information every 1 minute
    sender.add_periodic_task(15.0, perform_check.s(example_config))


@app.task()
def perform_check(config):
    runner = Runner()
    runner.perform_check(config)
    # print("PRetending", config)
    return True
