
import os
from flask import Flask, send_file

class FlaskApp:

    app = Flask(__name__, static_folder=os.path.join('..', 'static'))

    @app.route('/')
    def serve_index():
        """Return static index page"""
        return send_file(os.path.join('..', 'static', 'index.html'))
