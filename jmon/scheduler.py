

from time import sleep
from jmon import app, perform_check
import jmon.config
import jmon.models

existing_checks = []

@app.on_after_configure.connect
def schedule_periodic_tasks(sender, **kwargs):
    checks = jmon.models.Check.query.all()
    for check in checks:
        existing_checks.append(check.name)
        sender.add_periodic_task(jmon.config.Config.get().DEFAULT_CHECK_INTERVAL, perform_check.s(check.name))
