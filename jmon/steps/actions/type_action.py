

from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


class TypeAction(BaseAction):

    ACTION_NAME = "type"

    def _execute(self, selenium_instance, element):
        """Type text"""
        logger.info(f"Typing text: {self._config}")
        element.send_keys(self._config)
        return element
