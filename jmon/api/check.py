
from flask import request
import yaml

from . import FlaskApp
from jmon.models import Check


@FlaskApp.app.route('/api/v1/checks', methods=["GET"])
def get_checks():
    """Register check"""
    checks = Check.get_all()
    return [
        check.name
        for check in checks
    ], 200


@FlaskApp.app.route('/api/v1/checks', methods=["POST"])
def register_check():
    """Register check"""
    task = Check.from_yaml(request.data)
    return "Check created", 200
