
import redis
from redbeat import RedBeatSchedulerEntry

from jmon import app
import jmon.config
from jmon.logger import logger
import jmon.database
import jmon.models


def clean_orphaned_checks():
    """
    Remove all schedules and re-add each check in database.

    This handles deleted checks that didn't get correctly removed
    and any checks left over from jmon upgrades
    """
    # Get all existing scheduled checks
    config = jmon.config.Config.get()

    connection = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT, 
        password=config.REDIS_PASSWORD
    )
    existing_checks = [
        key.decode('utf-8')
        for key in connection.keys("redbeat:check_*")
    ]

    checks = jmon.models.Check.get_all()
    for check in checks:
        logger.debug(f"Processing check: {check.name}")
        if check.enabled:
            if check.redis_schedule_key in existing_checks:
                existing_checks.remove(check.redis_schedule_key)
            else:
                logger.info("Expected check not present in schedule")

    # Remove old checks from redis
    for existing_check in existing_checks:
        logger.info(f"Removing orphaned check from redis: {existing_check}")
        try:
            entry = RedBeatSchedulerEntry.from_key(key=existing_check, app=app)
            entry.delete()
        except KeyError:
            logger.info("Could not get beat scheduler entry from key")

    # Clear down session
    jmon.database.Database.clear_session()
