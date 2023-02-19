

import datetime
from io import StringIO
import logging
import os

from jmon.logger import logger
from jmon.artifact_storage import ArtifactStorage
from jmon.result_database import ResultMetricAverageSuccessRate, ResultDatabase, ResultMetricLatestStatus
import jmon.models.run
from jmon.steps.root_step import RootStep


class Run:

    def __init__(self, check, db_run=None):
        """Store run information"""
        self._check = check
        self._db_run = db_run

        self._artifact_paths = []

        self._logger = None
        self._log_stream = StringIO()
        self._log_handler = logging.StreamHandler(self._log_stream)
        self._log_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        self._log_handler.setFormatter(formatter)

        self._root_step = RootStep(run=self, config=self.check.steps, parent=None)

    @property
    def logger(self):
        """Return logger"""
        if self._logger is None:
            raise Exception("Attempt to access run logger before start() called")
        return self._logger

    @property
    def root_step(self):
        """Return root step instance"""
        return self._root_step

    def start(self):
        """Start run, setting up db run object and logging"""
        if self._db_run is not None:
            raise Exception("Cannot start run with Run DB modal already configured")
        self._db_run = jmon.models.run.Run.create(check=self._check)

        # Setup logger
        self._logger = logging.getLogger(self._db_run.id)
        self._logger.addHandler(self._log_handler)

    @property
    def log_handler(self):
        """Return log handler"""
        return self._log_handler

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

    def get_stored_artifacts(self):
        """Get list of artifacts from storage"""
        artifact_storage = ArtifactStorage()
        artifact_prefix = f"{self.get_artifact_key()}/"
        return [
            key.replace(artifact_prefix, '')
            for key in artifact_storage.list_files(artifact_prefix)
        ]

    def get_artifact_content(self, artifact):
        """Get artifact content"""
        artifact_storage = ArtifactStorage()
        artifact_path = f"{self.get_artifact_key()}/{artifact}"
        return artifact_storage.get_file(artifact_path)

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
        return self._db_run.timestamp_id

    def get_artifact_key(self):
        """Return key for run"""
        return f"{self._check.name}/{self.get_run_key()}"

    def read_log_stream(self):
        """Return data from logstream"""
        # Reset log stream
        self._log_stream.seek(0)
        return self._log_stream.read()
