

from jmon.client_type import ClientType
from jmon.step_state import SeleniumStepState
from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


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

    def execute_selenium(self, state: SeleniumStepState):
        """Type text"""
        state.element.send_keys(self._config)
