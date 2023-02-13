

from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


class ClickAction(BaseAction):

    ACTION_NAME = "click"

    def _execute(self, selenium_instance, element):
        """Click mouse"""
        logger.info(f"Clicking")
        element.click()
        return element
