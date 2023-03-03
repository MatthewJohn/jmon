

from jmon.client_type import ClientType
from jmon.step_state import RequestsStepState
from jmon.step_status import StepStatus
from jmon.steps.checks.base_check import BaseCheck


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

    def _validate_step(self):
        """Check step is valid"""
        # Nothing to check, value can be of any type
        pass

    def execute_requests(self, state: RequestsStepState):
        """Check response code"""
        if self._check_valid_requests_response(state.response):
            return

        if state.response.json() != self._config:
            self._set_status(StepStatus.FAILED)
            self._logger.error(f"Expected JSON response: {self._config}, but got: {state.response.json()}")
