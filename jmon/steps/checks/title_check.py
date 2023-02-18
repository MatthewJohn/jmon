

from jmon.step_status import StepStatus
from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger
from jmon.utils import retry


class TitleCheck(BaseCheck):

    CONFIG_KEY = "title"

    @property
    def id(self):
        """ID string for step"""
        return f"CheckTitle"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Check current title of browser matches: {self._config}"

    @retry(count=5, interval=0.5)
    def _execute(self, selenium_instance, element):
        """Check page title"""
        logger.info("Checking page title")
        actual_title = selenium_instance.title

        if actual_title != self._config:
            self._set_status(StepStatus.FAILED)
            self._logger.error(f'Title does not match excepted title. Expected "{self._config}" and got: "{actual_title}"')

        return element
