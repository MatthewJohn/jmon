

from jmon.client_type import ClientType
from jmon.step_status import StepStatus
from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger
from jmon.utils import retry


class JsonCheck(BaseCheck):

    CONFIG_KEY = "json"

    @property
    def supported_clients(self):
        """Return list of supported clients"""
        return [
            ClientType.REQUESTS
        ]

    @property
    def id(self):
        """ID string for step"""
        return f"CheckJson"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Check JSON response matches: {self._config}"

    def execute_requests(self, element):
        """Check response code"""
        if self._check_valid_requests_response(element):
            return element

        if element.json() != self._config:
            self._logger.error(f"Expected JSON response: {self._config}, but got: {element.json()}")
            self._set_status(StepStatus.FAILED)

        return element
