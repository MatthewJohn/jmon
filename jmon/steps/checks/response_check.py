

from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger
from jmon.utils import retry


class ResponseCheck(BaseCheck):

    CONFIG_KEY = "response"

    @retry(count=5, interval=0.5)
    def _execute(self, selenium_instance, element):
        """Check response code"""
        logger.info("Checking response")
        raise NotImplementedError
