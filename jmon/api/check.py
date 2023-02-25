
from flask import request
import yaml

from jmon.database import Database
from jmon.errors import CheckCreateError

from . import FlaskApp
from jmon.models import Check


@FlaskApp.app.route('/api/v1/checks', methods=["GET"])
def get_checks():
    """Register check"""
    checks = Check.get_all()
    return sorted([
        check.name
        for check in checks
    ]), 200


@FlaskApp.app.route('/api/v1/checks', methods=["POST"])
def register_check():
    """Register check"""
    try:
        task = Check.from_yaml(request.data)
    except CheckCreateError as exc:
        return {"status": "error", "msg": str(exc)}, 400

    return {"status": "ok", "msg": "Check created/updated"}, 200

@FlaskApp.app.route('/api/v1/checks/<check_name>', methods=["GET"])
@FlaskApp.app.route('/api/v1/checks/<check_name>/<environment_name>', methods=["GET"])
def get_check(check_name, environment_name=None):
    """Get check details"""
    check, _, error = get_check_and_environment_by_name(
        check_name=check_name, environment_name=environment_name)
    if error:
        return error, 404

    return {
        "name": check.name,
        "client": check.client.value if check.client else None,
        "interval": check.interval,
        "steps": check.steps,
        "enable": check.enabled
    }, 200

@FlaskApp.app.route('/api/v1/checks/<check_name>', methods=["DELETE"])
@FlaskApp.app.route('/api/v1/checks/<check_name>/environments/<environment_name>', methods=["DELETE"])
def delete_check(check_name, environment_name=None):
    """Register check"""
    check, _, error = get_check_and_environment_by_name(
        check_name=check_name, environment_name=environment_name)
    if error:
        return error, 404

    check.delete()
    return {"status": "ok", "msg": "Check deleted"}, 200

@FlaskApp.app.route('/api/v1/checks/<check_name>/enable', methods=["POST"])
def enable_check(check_name):
    """Get check details"""
    check = Check.get_by_name(check_name)
    if not check:
        return {"status": "error", "msg": "Check does not exist"}, 404

    check.enable()

    return {
        "status": "ok", "msg": "Enabled check"
    }, 200

@FlaskApp.app.route('/api/v1/checks/<check_name>/disable', methods=["POST"])
def disable_check(check_name):
    """Get check details"""
    check = Check.get_by_name(check_name)
    if not check:
        return {"status": "error", "msg": "Check does not exist"}, 404

    check.disable()

    return {
        "status": "ok", "msg": "Disabled check"
    }, 200
