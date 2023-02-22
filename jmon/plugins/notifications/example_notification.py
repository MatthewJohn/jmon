

from jmon.plugins import NotificationPlugin


class ExampleNotification(NotificationPlugin):
    """Example notification plugin"""

    def on_first_success(self, check_name, run_status, run_log):
        """Handle first success"""
        print(f"{check_name} had has changed to success state")

    def on_first_failure(self, check_name, run_status, run_log):
        """Handle first failure"""
        print(f"{check_name} had has changed to failure state")

    def on_every_success(self, check_name, run_status, run_log):
        """Handle every success"""
        print(f"{check_name} is passing")

    def on_every_failure(self, check_name, run_status, run_log):
        """Handle every failure"""
        print(f"{check_name} is failing")

    def on_complete(self, check_name, run_status, run_log):
        """Handle every run completion"""
        print(f"{check_name} has run with status: {run_status}")
        print(f"Log: {run_log}")
