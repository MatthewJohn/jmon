
from jmon.steps.base_step import BaseStep

class BaseAction(BaseStep):

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        return []
