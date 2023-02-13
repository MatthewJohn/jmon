

from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger


class TitleCheck(BaseCheck):

    CHECK_NAME = "title"

    def _execute(self, selenium_instance, element):
        """Check page title"""
        logger.info("Checking page title")
        assert selenium_instance.title == self._config
