

from jmon.client_type import ClientType
from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


class ClickAction(BaseAction):

    CONFIG_KEY = "click"

    @property
    def supported_clients(self):
        """Return list of supported clients"""
        return [
            ClientType.BROWSER_FIREFOX
        ]

    @property
    def id(self):
        """ID string for step"""
        return f"Click"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Clicking element"

    def execute_selenium(self, selenium_instance, element):
        """Click mouse"""
        element.click()
        return element
