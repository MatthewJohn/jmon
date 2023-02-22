

from jmon.plugins import NotificationPlugin
from jmon.logger import logger


class ExampleNotification(NotificationPlugin):
    """Example notification plugin"""

    def on_first_success(self, check_name, run_status, run_log):
        """Handle first success"""
        logger.debug(f"{check_name} had has changed to success state")

    def on_first_failure(self, check_name, run_status, run_log):
        """Handle first failure"""
        logger.debug(f"{check_name} had has changed to failure state")

    def on_every_success(self, check_name, run_status, run_log):
        """Handle every success"""
        logger.debug(f"{check_name} is passing")

    def on_every_failure(self, check_name, run_status, run_log):
        """Handle every failure"""
        logger.debug(f"{check_name} is failing")

    def on_complete(self, check_name, run_status, run_log):
        """Handle every run completion"""
        logger.debug(f"{check_name} has run with status: {run_status}")
        logger.debug(f"Log: {run_log}")
