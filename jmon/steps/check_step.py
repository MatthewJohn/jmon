
from jmon.steps.base_step import BaseStep
import jmon.steps.checks

class CheckStep(BaseStep):

    CONFIG_KEY = "check"
    SUPPORTED_CHILD_STEPS = []

    @classmethod
    def get_available_steps(cls):
        return {
            check_class.CHECK_NAME: check_class
            for check_class in jmon.steps.checks.BaseCheck.__subclasses__()
        }

    def get_checks(self):
        """Get all checks"""
        available_checks = self.get_available_steps()
        checks = []
        for check_name, check_config in self._config.items():
            if check_name not in available_checks:
                raise Exception(f'Invalid check: {check_name}')
            checks.append(available_checks[check_name](check_config))
        return checks

    def get_child_steps(self):
        """Add checks to list of available child steps"""
        steps = super().get_child_steps()
        steps.extend(self.get_checks())
        return steps

    def _execute(self, selenium_instance, element):
        """Check variables attributes of the page/element"""
        # Do nothing, let sub-checks perform checks
        return element
