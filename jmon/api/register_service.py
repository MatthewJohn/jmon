
from flask import request
import yaml

from . import FlaskApp
from jmon.models import Check

@FlaskApp.app.route('/api/v1/check', methods=["POST"])
def register_check():
    """Register check"""
    task = Check.from_yaml(request.data)
    return "Check created", 200
