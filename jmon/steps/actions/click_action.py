

from jmon.client_type import ClientType
from jmon.errors import StepValidationError
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

    def _validate_step(self):
        """Check step is valid"""
        if self._config is not None:
            raise StepValidationError(f"Click step should not have any attributes. Got: {self._config}")

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
