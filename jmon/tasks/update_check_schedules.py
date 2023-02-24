
import celery.schedules
from redbeat import RedBeatSchedulerEntry

import jmon.models
import jmon.config
import jmon.database
from jmon import app
from jmon.logger import logger


def update_check_schedules():
    """Add task schedules for each check in database."""
    checks = jmon.models.Check.get_all()
    for check in checks:
        if check.enabled:
            check.upsert_schedule()

    # Clear down session
    jmon.database.Database.clear_session()
