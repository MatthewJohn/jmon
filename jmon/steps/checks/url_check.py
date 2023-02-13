
from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger


class UrlCheck(BaseCheck):

    CHECK_NAME = "url"

    def _execute(self, selenium_instance, element):
        """Check page URL"""
        logger.info("Checking page URL")
        actual_url = selenium_instance.current_url
        if actual_url != self._config:
            raise Exception(f'URL does not match excepted url. Expected "{self._config}" and got: {actual_url}')
        return element
