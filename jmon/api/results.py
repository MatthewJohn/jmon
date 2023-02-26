
from flask import request
import yaml

from jmon.result_database import (
    ResultDatabase, ResultMetricAverageSuccessRate,
    ResultMetricLatestStatus
)

from . import FlaskApp
from .utils import get_check_and_environment_by_name


@FlaskApp.app.route('/api/v1/checks/<check_name>/environments/<environment_name>/results', methods=["GET"])
def get_check_results(check_name, environment_name):
    """Register check"""
    check, _, error = get_check_and_environment_by_name(
        check_name=check_name, environment_name=environment_name)
    if error:
        return error, 404

    result_database = ResultDatabase()
    return {
        "average_success": ResultMetricAverageSuccessRate().read(
            result_database=result_database, check=check),
        "latest_status": ResultMetricLatestStatus().read(
            result_database=result_database, check=check)
    }, 200
