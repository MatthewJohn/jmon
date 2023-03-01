
import datetime

from jmon.config import Config
import jmon.database
import jmon.models.run
from jmon.logger import logger

def remove_expired_runs():
    """Remove expired runs from databases"""
    try:
        deletion_cutoff = (
            datetime.datetime.now() -
            datetime.timedelta(minutes=Config.get().RESULT_RETENTION_MINS)
        )


        # Get all runs
        logger.info(f"Deleting runs older than: {deletion_cutoff}")
        session = jmon.database.Database.get_session()
        count = session.query(
            jmon.models.run.Run
        ).filter(
            jmon.models.run.Run.timestamp<=deletion_cutoff
        ).delete()
        session.commit()
        logger.info(f"Delete {count} runs")

    finally:
        jmon.database.Database.clear_session()

