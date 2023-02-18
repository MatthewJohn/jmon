

from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


class TypeAction(BaseAction):

    CONFIG_KEY = "type"

    @property
    def id(self):
        """ID string for step"""
        return f"Type"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Typing text into browser element: {self._config}"

    def _execute(self, selenium_instance, element):
        """Type text"""
        logger.info(f"Typing text: {self._config}")
        element.send_keys(self._config)
        return element
