
import requests
from jmon.client_type import ClientType
from jmon.step_state import RequestsStepState, SeleniumStepState
from jmon.step_status import StepStatus
from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger
from jmon.utils import retry


class UrlCheck(BaseCheck):

    CONFIG_KEY = "url"

    @property
    def supported_clients(self):
        """Return list of supported clients"""
        return [
            ClientType.REQUESTS,
            ClientType.BROWSER_FIREFOX,
            ClientType.BROWSER_CHROME
        ]

    @property
    def id(self):
        """ID string for step"""
        return f"CheckUrl"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Check current URL of browser matches: {self._config}"

    @retry(count=5, interval=0.5)
    def _check_url(self, selenium_instance, url):
        """Check URL"""
        actual_url = selenium_instance.current_url
        if actual_url != url:
            self._logger.error(f'URL does not match excepted url. Expected "{self._config}" and got: {actual_url}')
            return None
        return True

    def execute_requests(self, state: RequestsStepState):
        """Check URL"""
        if self._check_valid_requests_response(state.response):
            return
        if state.response.url != self._config:
            self._logger.error(f'URL does not match excepted url. Expected "{self._config}" and got: {state.response.url}')
            self._set_status(StepStatus.FAILED)

    def execute_selenium(self, state: SeleniumStepState):
        """Check page URL"""
        if self._check_url(state.selenium_instance, self._config) is None:
            self._set_status(StepStatus.FAILED)
