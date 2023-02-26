
from flask import Response

from . import FlaskApp
from .utils import get_check_and_environment_by_name
import jmon.models
import jmon.run


@FlaskApp.app.route('/api/v1/checks/<check_name>/environments/<environment_name>/runs/<timestamp>/artifacts/<artifact>', methods=["GET"])
def get_run_artifact(check_name, environment_name, timestamp, artifact):
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

    # Get mimetype of known file types
    mimetype = None
    if artifact.endswith(".png"):
        mimetype = "image/png"
    elif artifact.endswith(".log"):
        mimetype = "text/plain"

    if mimetype is None:
        return {
            "error": "Unknown file type"
        }, 400

    artifact_content = run.get_artifact_content(artifact)
    if artifact_content is None:
        return {
            "error": "artifact not found"
        }, 404

    return Response(artifact_content, mimetype=mimetype)
