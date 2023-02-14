
import jmon.models
from jmon.run import Run
from jmon.runner import Runner
from jmon.logger import logger


def perform_check(check_name):
    # Get config for check
    check = jmon.models.Check.query.filter(jmon.models.Check.name==check_name).first()
    if not check:
        raise Exception("Could not find check")

    run = Run(check)

    runner = Runner()

    success = False
    try:
        runner.perform_check(run=run)
        success = True
    except Exception as exc:
        logger.error(f"An error occured: {exc}")
        raise
    finally:
        run.end(status=success)

    return True
