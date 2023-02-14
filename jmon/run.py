

import datetime
from io import StringIO
import logging

from jmon.logger import logger
from jmon.storage import Storage


class Run:

    def __init__(self, check):
        """Store run information"""
        self._check = check
        self._start_date = datetime.datetime.now()

        self._log_stream = StringIO()
        self._log_handler = logging.StreamHandler(self._log_stream)
        self._log_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._log_handler.setFormatter(formatter)
        logger.addHandler(self._log_handler)

    @property
    def check(self):
        """Return check"""
        return self._check

    def end(self):
        """End logging and upload"""
        logger.removeHandler(self._log_handler)

        # Upload to storage
        storage = Storage()
        storage.upload_file(f"{self.get_artifact_key()}/artifact.log", self.read_log_stream())

    def get_artifact_key(self):
        """Return key for run"""
        return f"{self._check.name}/{self._start_date.strftime('%Y-%m-%d_%H-%M-%S')}"

    def read_log_stream(self):
        """Return data from logstream"""
        # Reset log stream
        self._log_stream.seek(0)
        return self._log_stream.read()
