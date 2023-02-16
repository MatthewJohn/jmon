

import datetime
from io import StringIO
import logging
import os

from jmon.logger import logger
from jmon.artifact_storage import ArtifactStorage
from jmon.result_database import ResultMetricAverageSuccessRate, ResultDatabase, ResultMetricLatestStatus
import jmon.models.run


class Run:

    def __init__(self, check):
        """Store run information"""
        self._check = check
        self._db_run = jmon.models.run.Run.create(check=check)

        self._artifact_paths = []

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

    @property
    def success(self):
        """Return success status"""
        return self._db_run.success

    def register_artifact(self, path):
        """Register artifact to be uploaded to artifact storage"""
        self._artifact_paths.append(path)

    def end(self, success):
        """End logging and upload"""
        self._db_run.set_success(success)

        logger.removeHandler(self._log_handler)

        # Upload to storage
        artifact_storage = ArtifactStorage()
        artifact_storage.upload_file(f"{self.get_artifact_key()}/artifact.log", content=self.read_log_stream())
        artifact_storage.upload_file(f"{self.get_artifact_key()}/status", content=str(self.success))
        for artifact_path in self._artifact_paths:
            _, artifact_name = os.path.split(artifact_path)
            artifact_storage.upload_file(f"{self.get_artifact_key()}/{artifact_name}", source_path=artifact_path)

        # Create metrics
        result_database = ResultDatabase()
        average_success_metric = ResultMetricAverageSuccessRate()
        average_success_metric.write(result_database=result_database, run=self)
        latest_status_metric = ResultMetricLatestStatus()
        latest_status_metric.write(result_database=result_database, run=self)

    def get_run_key(self):
        """Return datetime key for run"""
        return self._db_run.timestamp_key

    def get_artifact_key(self):
        """Return key for run"""
        return f"{self._check.name}/{self.get_run_key()}"

    def read_log_stream(self):
        """Return data from logstream"""
        # Reset log stream
        self._log_stream.seek(0)
        return self._log_stream.read()
