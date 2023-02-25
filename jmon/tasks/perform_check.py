
from celery.result import AsyncResult

from jmon import app
import jmon.models
from jmon.run import Run
from jmon.runner import Runner
from jmon.logger import logger
import jmon.database
from jmon.step_status import StepStatus


def perform_check(self, check_name, environment_name):

    # Check if task has already executed due to being
    # pushed to multiple queues and, if so,
    # return the original result
    res = AsyncResult(self.request.id, app=app)
    if res.status != "PENDING":
        return res.result

    logger.info(f"Starting check: Check Name: {check_name}, Environment: {environment_name}")

    # Get environment
    environment = jmon.models.environment.Environment.get_by_name(name=environment_name)
    if not environment:
        raise Exception("Could not find environment")

    # Get check
    check = jmon.models.check.Check.get_by_name_and_environment(
        name=check_name, environment=environment
    )
    if not check:
        raise Exception("Could not find check")

    # Create run and mark as started
    run = Run(check)
    run.start()

    runner = Runner()

    status = StepStatus.FAILED
    try:
        status = runner.perform_check(run=run)

    except Exception as exc:
        run.logger.error(f"An internal/uncaught error occured: {exc}")
        raise

    finally:
        run.end(run_status=status)
        jmon.database.Database.clear_session()

    return (status == StepStatus.SUCCESS)
