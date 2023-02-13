

from jmon.logger import logger
from jmon.steps.base_step import BaseStep
from jmon.steps.goto_step import GotoStep
from jmon.steps.find_step import FindStep
from jmon.steps.check_step import CheckStep


class RootStep(BaseStep):

    SUPPORTED_CHILD_STEPS = [
        GotoStep,
        FindStep,
        CheckStep
    ]


    def _execute(self, selenium_instance, element):
        """Root module does nothing"""
        logger.info(f"Starting root with config: {self._config}")
        return element
