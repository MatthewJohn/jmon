

from jmon.logger import logger


class BaseStep:

    CONFIG_KEY = None

    def __init__(self, config):
        """Store member variables"""
        logger.info(f"Creating step: {self.__class__.__name__}: {config}")
        self._config = config

    def get_child_steps(self):
        """Get child steps"""
        steps = []

        if not self._config or type(self._config) not in [list, dict]:
            return steps

        supported_child_steps = self.get_supported_child_steps()

        print(self.__class__.__name__)
        print(self._config)
        # Handle lists of steps
        if type(self._config) is list:
            for step_config in self._config:
                for supported_step_name, supported_step_class in supported_child_steps.items():
                    if supported_step_name in step_config:
                        print(supported_step_name)
                        logger.info(f"Adding child step: {supported_step_name}: {step_config[supported_step_name]}")
                        steps.append(
                            supported_step_class(step_config[supported_step_name])
                        )

        # Handle check dictionaries
        elif type(self._config) is dict:
            for step_name in self._config:
                if step_name in supported_child_steps:
                    logger.info(f"Adding child step: {step_name}: {self._config[step_name]}")
                    steps.append(supported_child_steps[step_name](self._config[step_name]))

        return steps

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        raise NotImplementedError

    def get_supported_child_steps(self):
        """Get dictionary of supported child steps"""
        return {
            child_step.CONFIG_KEY: child_step
            for child_step in self.supported_child_steps
            if child_step.CONFIG_KEY
        }

    def _execute(self, selenium_instance, element):
        """Execute step"""
        raise NotImplementedError

    def execute(self, selenium_instance, element):
        """Execute the current step and then execute each of the child steps"""
        element = self._execute(selenium_instance, element)
        for step in self.get_child_steps():
            element = step.execute(selenium_instance, element)
        return element
