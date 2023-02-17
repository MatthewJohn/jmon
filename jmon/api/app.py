
import os
from flask import Flask, send_file

from jmon.database import Database


class FlaskApp:

    app = Flask(__name__, static_folder=os.path.join('..', 'static'))

    @app.teardown_request
    def teardown(request):
        """Tear down request"""
        # Clear down DB session
        Database.clear_session()


    @app.route('/')
    def serve_index():
        """Return static index page"""
        return send_file(os.path.join('..', 'static', 'index.html'))

    @app.route('/check')
    def serve_check():
        """Return check page"""
        return send_file(os.path.join('..', 'static', 'check.html'))

    @app.route('/run')
    def serve_run():
        """Return run page"""
        return send_file(os.path.join('..', 'static', 'run.html'))
