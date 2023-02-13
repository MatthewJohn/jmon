
from jmon.steps.base_step import BaseStep
import jmon.steps.actions

class ActionStep(BaseStep):

    CONFIG_KEY = "actions"
    SUPPORTED_CHILD_STEPS = []

    @classmethod
    def get_available_steps(cls):
        return {
            action_class.ACTION_NAME: action_class
            for action_class in jmon.steps.actions.BaseAction.__subclasses__()
        }

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        return []

    def get_actions(self):
        """Get all actions"""
        available_actions = self.get_available_steps()
        actions = []
        for action_name, action_config in self._config.items():
            if action_name not in available_actions:
                raise Exception(f'Invalid action: {action_name}. Available actions: {[c for c in available_actions]}')
            actions.append(available_actions[action_name](self._config[action_config]))
        return actions

    def get_child_steps(self):
        """Add actions to list of available child steps"""
        steps = super().get_child_steps()
        steps.extend(self.get_actions())
        return steps

    def _execute(self, selenium_instance, element):
        """Do nothihng"""
        # Do nothing, let sub-actions perform actions
        return element
