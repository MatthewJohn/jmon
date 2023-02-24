
from celery.result import AsyncResult

from jmon import app
import jmon.models
from jmon.run import Run
from jmon.runner import Runner
from jmon.logger import logger
import jmon.database
from jmon.step_status import StepStatus


def perform_check(self, check_name):

    # Check if task has already executed due to being
    # pushed to multiple queues and, if so,
    # return the original result
    res = AsyncResult(self.request.id, app=app)
    if res.status != "PENDING":
        return res.result

    logger.info(f"Starting check: {check_name}")

    # Get config for check
    session = jmon.database.Database.get_session()
    check = session.query(jmon.models.Check).filter(jmon.models.Check.name==check_name).first()

    if not check:
        raise Exception("Could not find check")

    run = Run(check)
    run.start()

    runner = Runner()

    success = False
    try:
        status = runner.perform_check(run=run)

    except Exception as exc:
        run.logger.error(f"An internal/uncaught error occured: {exc}")
        raise

    finally:
        run.end(run_status=status)
        jmon.database.Database.clear_session()

    return success
