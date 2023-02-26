
import jmon.models


def get_check_and_environment_by_name(check_name, environment_name):
    """Return check and environment based on name"""
    environment = None
    if environment_name is not None:
        environment = jmon.models.environment.Environment.get_by_name(environment_name)
        if environment is None:
            return None, None, {"status": "error", "msg": "Environment does not exist"}

    check = jmon.models.check.Check.get_by_name_and_environment(check_name, environment)
    if not check:
        return None, None, {"status": "error", "msg": "Check does not exist"}

    return check, environment, None
