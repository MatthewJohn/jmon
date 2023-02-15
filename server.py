#!python

from jmon.api import FlaskApp

flask_app = FlaskApp()
flask_app.app.run(host='0.0.0.0', threaded=True)