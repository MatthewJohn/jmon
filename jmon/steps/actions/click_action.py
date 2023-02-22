

from jmon.client_type import ClientType
from jmon.step_state import SeleniumStepState
from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


class ClickAction(BaseAction):

    CONFIG_KEY = "click"

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
        return f"Click"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Clicking element"

    def execute_selenium(self, state: SeleniumStepState):
        """Click mouse"""
        state.element.click()
