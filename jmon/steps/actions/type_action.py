
import selenium.common.exceptions

from jmon.client_type import ClientType
from jmon.step_state import SeleniumStepState
from jmon.step_status import StepStatus
from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger
from jmon.utils import retry


class TypeAction(BaseAction):

    CONFIG_KEY = "type"

    @property
    def supported_clients(self):
        """Return list of supported clients"""
        return [
            ClientType.BROWSER_FIREFOX,
            ClientType.BROWSER_CHROME
        ]

    @property
    def id(self):
        """ID string for step"""
        return f"Type"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Typing text into browser element: {self._config}"

    @retry(count=5, interval=0.5)
    def _type(self, element, text):
        try:
            element.send_keys(text)
            return True
        except selenium.common.exceptions.ElementNotInteractableException:
            return None

    def execute_selenium(self, state: SeleniumStepState):
        """Type text"""
        if not self._type(state.element, self._config):
            self._set_status(StepStatus.FAILED)
            self._logger.error("Unable to type into element")
