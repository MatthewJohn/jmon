
from jmon.step_status import StepStatus
from jmon.steps.checks.base_check import BaseCheck
from jmon.logger import logger
from jmon.utils import retry


class UrlCheck(BaseCheck):

    CONFIG_KEY = "url"

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

    def _execute(self, selenium_instance, element):
        """Check page URL"""
        if self._check_url(selenium_instance, self._config) is None:
            self._set_status(StepStatus.FAILED)

        return element
