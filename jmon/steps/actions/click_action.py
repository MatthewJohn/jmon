

from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


class ClickAction(BaseAction):

    CONFIG_KEY = "click"

    @property
    def id(self):
        """ID string for step"""
        return f"Click"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Clicking element"

    def _execute(self, selenium_instance, element):
        """Click mouse"""
        logger.info(f"Clicking")
        element.click()
        return element
