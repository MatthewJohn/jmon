

from jmon.client_type import ClientType
from jmon.step_state import SeleniumStepState
from jmon.step_status import StepStatus
from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger
from jmon.utils import retry


class TitleCheck(BaseCheck):

    CONFIG_KEY = "title"

    @property
    def supported_clients(self):
        """Return list of supported clients"""
        return [
            ClientType.BROWSER_FIREFOX
        ]

    @property
    def id(self):
        """ID string for step"""
        return f"CheckTitle"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Check current title of browser matches: {self._config}"

    @retry(count=5, interval=0.5)
    def _check_title(self, selenium_instance, expected_title):
        """Check title"""
        actual_title = selenium_instance.title
        if actual_title != expected_title:
            self._logger.error(f'Title does not match excepted title. Expected "{self._config}" and got: "{actual_title}"')
            return None
        return True

    def execute_selenium(self, state: SeleniumStepState):
        """Check page title"""
        if not self._check_title(state.selenium_instance, self._config):
            self._set_status(StepStatus.FAILED)
