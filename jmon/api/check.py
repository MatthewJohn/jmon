
from flask import request
import yaml

from jmon.database import Database

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
    task = Check.from_yaml(request.data)
    return {"status": "ok", "msg": "Check created/updated"}, 200

@FlaskApp.app.route('/api/v1/checks/<check_name>', methods=["DELETE"])
def delete_check(check_name):
    """Register check"""
    check = Check.get_by_name(check_name)
    if check is None:
        return {"status": "error", "msg": "Check does not exist"}, 404

    check.delete()
    return {"status": "ok", "msg": "Check deleted"}, 200
