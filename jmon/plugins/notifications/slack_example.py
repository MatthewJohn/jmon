
import os
import requests

from jmon.plugins import NotificationPlugin
from jmon.logger import logger


class SlackExample(NotificationPlugin):

    _WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

    def _post_message(self, text):
        """Send message to slack"""
        if not self._WEBHOOK_URL:
            # It slack webhook has not been configured - return early
            return

        res = requests.post(
            self._WEBHOOK_URL,
            json={
                "text": text
            }
        )
        if res.json().get("ok") is not True:
            logger.error("Slack did not return an OK status when posting notification")

    def on_first_failure(self, check_name, run_status, run_log):
        """Post slack message on failure"""
        self._post_message(f"{check_name} has failed :alarm:")

    def on_first_success(self, check_name, run_status, run_log):
        """Post slack message on success"""
        self._post_message(f"{check_name} is back to normal :checkmark:")

    def on_check_queue_timeout(self, check_count):
        """Handle queue timeout"""
        self._post_message(
            f"WARNING: {check_count} check(s) missed due to queue timeout. "
            "Check queue size and consider increase workers."
        )
