
from jmon.steps.base_step import BaseStep
import jmon.steps.actions
from jmon.logger import logger

class ActionStep(BaseStep):

    CONFIG_KEY = "actions"

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        return jmon.steps.actions.BaseAction.__subclasses__()

    def get_child_steps(self):
        """
        Get child steps

        Handle actions similar to:
        actions:
         - type: Pabalonium
         - press: enter
         - click
        """
        steps = []

        supported_actions = self.get_supported_child_steps()

        for action_config in self._config:
            if type(action_config) is dict:
                for action_name in action_config:
                    if action_name in supported_actions:
                        steps.append(
                            supported_actions[action_name](action_config[action_name])
                        )
            elif type(action_config) is str:
                steps.append(
                    supported_actions[action_config](None)
                )
        return steps

    def _execute(self, selenium_instance, element):
        """Do nothihng"""
        # Do nothing, let sub-actions perform actions
        return element
