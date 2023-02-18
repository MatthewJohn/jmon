
from jmon.steps.base_step import BaseStep
import jmon.steps.checks
from jmon.logger import logger


class CheckStep(BaseStep):

    CONFIG_KEY = "check"
    CHILD_STEPS_FORM_STEP = True

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        return jmon.steps.checks.BaseCheck.__subclasses__()

    @property
    def id(self):
        """ID string for step"""
        return f"Checks"

    @property
    def description(self):
        """Friendly description of step"""
        return "Running check steps"

    def get_child_steps(self):
        """
        Get child steps

        Support checks such as:
        - check:
            title: An example website
            response_code: 200
            url: https://www.example.com
        """
        if self._child_steps is None:
            self._child_steps = []

            supported_actions = self.get_supported_child_steps()

            for action_name in self._config:
                if action_name in supported_actions:
                    self._child_steps.append(
                        supported_actions[action_name](
                            run=self._run,
                            config=self._config[action_name],
                            parent=self
                        )
                    )
        return self._child_steps

    def _execute(self, selenium_instance, element):
        """Check variables attributes of the page/element"""
        # Do nothing, let sub-checks perform checks
        return element
