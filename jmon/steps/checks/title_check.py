

from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger


class TitleCheck(BaseCheck):

    CHECK_NAME = "title"

    def _execute(self, selenium_instance, element):
        """Check page title"""
        logger.info("Checking page title")
        actual_title = selenium_instance.title
        if actual_title != self._config:
            raise Exception(f'Title does not match excepted title. Expected "{self._config}" and got: {actual_title}')
        return element
