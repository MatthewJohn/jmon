
from flask import request
import yaml

from jmon.result_database import ResultDatabase, ResultMetricAverageSuccessRate

from . import FlaskApp
from jmon.models import Check


@FlaskApp.app.route('/api/v1/checks/<check_name>/results', methods=["GET"])
def get_check_results(check_name):
    """Register check"""
    check = Check.get_by_name(check_name)
    if not check:
        return {
            "error": "Check does not exist"
        }, 400

    result_database = ResultDatabase()
    return {
        "average_success": ResultMetricAverageSuccessRate().read(
            result_database=result_database, check=check)
    }, 200
