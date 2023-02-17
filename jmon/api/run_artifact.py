
from flask import Response

from . import FlaskApp
import jmon.models
import jmon.run


@FlaskApp.app.route('/api/v1/checks/<check_name>/runs/<timestamp>/artifacts/<artifact>', methods=["GET"])
def get_run_artifact(check_name, timestamp, artifact):
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
