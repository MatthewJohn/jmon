
from flask import request

from . import FlaskApp
from .utils import get_check_and_environment_by_name
import jmon.models
import jmon.run


@FlaskApp.app.route('/api/v1/checks/<check_name>/environments/<environment_name>/runs/<timestamp>', methods=["GET"])
def get_run_details(check_name, environment_name, timestamp):
    """Register check"""
    check, _, error = get_check_and_environment_by_name(
        check_name=check_name, environment_name=environment_name)
    if error:
        return error, 404


    db_run = jmon.models.Run.get(
        check=check,
        timestamp_id=timestamp
    )
    if not db_run:
        return {
            "error": "Run does not exist"
        }, 400

    run = jmon.run.Run(check=check, db_run=db_run)

    return {
        "status": db_run.status,
        "artifacts": run.get_stored_artifacts()
    }
