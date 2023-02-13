
from jmon.steps.base_step import BaseStep

class GotoStep(BaseStep):

    CONFIG_KEY = "goto"
    SUPPORTED_CHILD_STEPS = []

    def _execute(self, selenium_instance, element):
        """Goto URL"""
        selenium_instance.get(self._config)
