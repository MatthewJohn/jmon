#!python

from flask_cors import CORS

from jmon.api import FlaskApp

flask_app = FlaskApp()
CORS(flask_app.app)
flask_app.app.run(host='0.0.0.0', threaded=True)