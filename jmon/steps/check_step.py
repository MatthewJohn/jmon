
from jmon.steps.base_step import BaseStep
import jmon.steps.checks
from jmon.logger import logger


class CheckStep(BaseStep):

    CONFIG_KEY = "check"

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        return jmon.steps.checks.BaseCheck.__subclasses__()

    def get_child_steps(self):
        """
        Get child steps

        Support checks such as:
        - check:
            title: An example website
            response_code: 200
            url: https://www.example.com
        """
        steps = []

        supported_actions = self.get_supported_child_steps()

        for action_name in self._config:
            if action_name in supported_actions:
                logger.info(f"Adding child step: {action_name}: {self._config[action_name]}")
                steps.append(
                    supported_actions[action_name](self._config[action_name])
                )
        return steps

    def _execute(self, selenium_instance, element):
        """Check variables attributes of the page/element"""
        # Do nothing, let sub-checks perform checks
        return element
