
from flask import request

from . import FlaskApp
from jmon.models import Check, Run


@FlaskApp.app.route('/api/v1/checks/<check_name>/runs', methods=["GET"])
def get_check_runs(check_name):
    """Register check"""
    check = Check.get_by_name(check_name)
    if not check:
        return {
            "error": "Check does not exist"
        }, 400

    return {
        run.timestamp_key: run.success
        for run in Run.get_by_check(check=check)
    }, 200
