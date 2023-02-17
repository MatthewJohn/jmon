
from flask import request

from . import FlaskApp
import jmon.models
import jmon.run


@FlaskApp.app.route('/api/v1/checks/<check_name>/runs/<timestamp>', methods=["GET"])
def get_run_details(check_name, timestamp):
    """Register check"""
    check = jmon.models.Check.get_by_name(check_name)
    if not check:
        return {
            "error": "Check does not exist"
        }, 400


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
        "status": run.success,
        "artfacts": run.get_stored_artifacts()
    }
