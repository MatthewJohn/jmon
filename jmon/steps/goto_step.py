
from jmon.steps.base_step import BaseStep
from jmon.logger import logger


class GotoStep(BaseStep):

    CONFIG_KEY = "goto"
    SUPPORTED_CHILD_STEPS = []

    def _execute(self, selenium_instance, element):
        """Goto URL"""
        logger.info(f"Goto URL: {self._config}")
        selenium_instance.get(self._config)
        return element