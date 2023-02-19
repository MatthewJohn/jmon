
import requests
import selenium.common.exceptions
from jmon.client_type import ClientType

from jmon.step_status import StepStatus
from jmon.steps.base_step import BaseStep
from jmon.logger import logger


class GotoStep(BaseStep):

    CONFIG_KEY = "goto"

    @property
    def supported_clients(self):
        """Return list of supported clients"""
        return [
            ClientType.BROWSER_FIREFOX,
            ClientType.REQUESTS
        ]

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        return []

    @property
    def id(self):
        """ID string for step"""
        return f"GoTo"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Going to URL: {self._config}"

    def execute_requests(self, element):
        """Execute step for requests"""
        return requests.get(self._config)

    def execute_selenium(self, selenium_instance, element):
        """Goto URL"""
        try:
            selenium_instance.get(self._config)
        except selenium.common.exceptions.WebDriverException as exc:
            self._set_status(StepStatus.FAILED)
            self._logger.error(str(exc))

        return element
