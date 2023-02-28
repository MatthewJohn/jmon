

import datetime
from io import StringIO
import logging
import os

from jmon.logger import logger
from jmon.artifact_storage import ArtifactStorage
from jmon.plugins import NotificationLoader
from jmon.result_database import ResultMetricAverageSuccessRate, ResultDatabase, ResultMetricLatestStatus
import jmon.models.run
from jmon.step_status import StepStatus
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

    def end(self, run_status):
        """End logging and upload"""
        self._db_run.set_status(run_status)

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

        # Send notifications using plugins
        self.send_notifications(run_status)

    def send_notifications(self, run_status):
        """Send notifications to plugins"""
        methods_to_call = [
            # Always call the "on_complete" method
            "on_complete"
        ]

        last_2_runs = jmon.models.run.Run.get_by_check(check=self._check, limit=2)
        is_new_state = False
        # If this is the first run, count as a state change
        if len(last_2_runs) == 1:
            is_new_state = True
        # Otherwise, set is_new_state if last two runs had differing results
        elif last_2_runs[0].success != last_2_runs[1].success:
            is_new_state = True

        # Create list of methods to be called on the notification plugin
        if run_status is StepStatus.SUCCESS:
            methods_to_call.append("on_every_success")
            if is_new_state:
                methods_to_call.append("on_first_success")
        elif run_status is StepStatus.FAILED:
            methods_to_call.append("on_every_failure")
            if is_new_state:
                methods_to_call.append("on_first_failure")

        for notification_plugin in NotificationLoader.get_instance().get_plugins():
            logger.debug(f"Processing notification plugin: {notification_plugin}")
            for method_to_call in methods_to_call:
                try:
                    logger.debug(f"Calling notification plugin method: {notification_plugin}.{method_to_call}")
                    getattr(notification_plugin(), method_to_call)(
                        check_name=self._check.name,
                        run_status=run_status,
                        run_log=self.read_log_stream()
                    )
                except Exception as exc:
                    logger.debug(f"Failed to call notification method: {str(exc)}")

    def get_run_key(self):
        """Return datetime key for run"""
        return self._db_run.timestamp_id

    def get_artifact_key(self):
        """Return key for run"""
        return f"{self._check.name}/{self._check.environment.name}/{self.get_run_key()}"

    def read_log_stream(self):
        """Return data from logstream"""
        # Reset log stream
        self._log_stream.seek(0)
        return self._log_stream.read()
