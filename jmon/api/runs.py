
from flask import request

from . import FlaskApp
from .utils import get_check_and_environment_by_name
from jmon.models import Run


@FlaskApp.app.route('/api/v1/checks/<check_name>/environments/<environment_name>/runs', methods=["GET"])
def get_check_runs(check_name, environment_name):
    """Register check"""
    check, _, error = get_check_and_environment_by_name(
        check_name=check_name, environment_name=environment_name)
    if error:
        return error, 404

    return {
        run.timestamp_id: run.status.value
        for run in Run.get_by_check(check=check)
    }, 200
