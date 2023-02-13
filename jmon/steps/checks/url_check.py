
from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger


class UrlCheck(BaseCheck):

    CHECK_NAME = "url"

    def _execute(self, selenium_instance, element):
        """Check page URL"""
        logger.info("Checking page URL")
        assert selenium_instance.current_url == self._config
