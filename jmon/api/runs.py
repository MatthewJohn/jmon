
from flask import request
import yaml

from jmon.result_database import (
    ResultDatabase, ResultRegisterResult
)

from . import FlaskApp
from jmon.models import Check


@FlaskApp.app.route('/api/v1/checks/<check_name>/runs', methods=["GET"])
def get_check_runs(check_name):
    """Register check"""
    check = Check.get_by_name(check_name)
    if not check:
        return {
            "error": "Check does not exist"
        }, 400

    result_database = ResultDatabase()
    runs =  ResultRegisterResult().get_all_runs_by_check(
        result_database=result_database,
        check=check)
    return runs, 200
