
import jmon.models
from jmon.run import Run
from jmon.runner import Runner
from jmon.logger import logger
import jmon.database


def perform_check(check_name):
    # Get config for check
    with jmon.database.Session() as session:
        check = session.query(jmon.models.Check).filter(jmon.models.Check.name==check_name).first()

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
        run.end(success=success)

    return True
