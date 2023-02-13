
import jmon.models
from jmon.runner import Runner


def perform_check(check_name):
    # Get config for check
    check = jmon.models.Check.query.filter(jmon.models.Check.name==check_name).first()
    if not check:
        raise Exception("Could not find check")

    runner = Runner()
    runner.perform_check(check.steps)
    return True
