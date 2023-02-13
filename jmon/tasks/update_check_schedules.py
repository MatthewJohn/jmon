
import celery.schedules
from redbeat import RedBeatSchedulerEntry

import jmon.models
import jmon.config
from jmon import app


def update_check_schedules():
    """Add task schedules for each check in database."""
    checks = jmon.models.Check.query.all()
    for check in checks:
        interval = celery.schedules.schedule(run_every=jmon.config.Config.get().DEFAULT_CHECK_INTERVAL)
        entry = RedBeatSchedulerEntry(
            f'check_{check.name}',
            'jmon.tasks.perform_check.perform_check',
            interval,
            args=[check.name],
            app=app
        )
        entry.save()
