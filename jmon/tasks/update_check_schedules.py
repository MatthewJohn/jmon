
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
        logger.debug(f"Processing check: {check.name}")
        if check.enabled:
            if check.upsert_schedule():
                logger.info(f"Added/updated schedule for {check.name}")

    # Clear down session
    jmon.database.Database.clear_session()
