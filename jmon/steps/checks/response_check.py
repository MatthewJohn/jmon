

from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger
from jmon.utils import retry


class ResponseCheck(BaseCheck):

    CONFIG_KEY = "response"

    @property
    def id(self):
        """ID string for step"""
        return f"CheckResponseCode"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Check response code matches: {self._config}"

    @retry(count=5, interval=0.5)
    def _check_response_code(self):
        return True

    def _execute(self, selenium_instance, element):
        """Check response code"""
        logger.info("Checking response")
        self._check_response_code()
        raise NotImplementedError
