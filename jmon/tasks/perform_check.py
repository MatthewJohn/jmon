
import jmon.models
from jmon.run import Run
from jmon.runner import Runner
from jmon.logger import logger
import jmon.database
from jmon.step_status import StepStatus


def perform_check(check_name):
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
        success = bool(status is StepStatus.SUCCESS)

    except Exception as exc:
        run.logger.error(f"An internal/uncaught error occured: {exc}")
        raise

    finally:
        run.end(success=success)
        jmon.database.Database.clear_session()

    return True
