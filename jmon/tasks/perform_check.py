
import jmon.models
from jmon.run import Run
from jmon.runner import Runner
from jmon.storage import Storage


def perform_check(check_name):
    # Get config for check
    check = jmon.models.Check.query.filter(jmon.models.Check.name==check_name).first()
    if not check:
        raise Exception("Could not find check")

    run = Run(check)

    runner = Runner()

    try:
        runner.perform_check(run)
    finally:
        run.end()
        storage = Storage()
        storage.upload_log(run)


    return True
