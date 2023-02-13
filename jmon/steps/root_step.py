

from jmon.logger import logger
from jmon.steps.base_step import BaseStep
from jmon.steps.goto_step import GotoStep
from jmon.steps.find_step import FindStep
from jmon.steps.check_step import CheckStep
from jmon.steps.action_step import ActionStep


class RootStep(BaseStep):

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        return [
            GotoStep,
            FindStep,
            CheckStep,
            ActionStep
        ]

    def _execute(self, selenium_instance, element):
        """Root module does nothing"""
        logger.info(f"Starting root with config: {self._config}")
        return element
