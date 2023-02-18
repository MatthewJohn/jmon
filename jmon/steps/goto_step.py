
from jmon.steps.base_step import BaseStep
from jmon.logger import logger


class GotoStep(BaseStep):

    CONFIG_KEY = "goto"

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        return []

    @property
    def id(self):
        """ID string for step"""
        return f"GoTo"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Going to URL: {self._config}"

    def _execute(self, selenium_instance, element):
        """Goto URL"""
        logger.info(f"Goto URL: {self._config}")
        selenium_instance.get(self._config)
        return element
