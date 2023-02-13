

class BaseStep:

    SUPPORTED_CHILD_STEPS = None
    CONFIG_KEY = None

    def __init__(self, config):
        self._config = config

    def get_child_steps(self):
        """Get child steps"""
        steps = []
        for supported_step_name, supported_step_class in self.get_supported_child_steps().items():
            if supported_step_name in self._config:
                steps.append(
                    supported_step_class(self._config[supported_step_name])
                )
        return steps

    def get_supported_child_steps(self):
        """Get dictionary of supported child steps"""
        if self.SUPPORTED_CHILD_STEPS is None:
            raise NotImplementedError
        return {
            child_step.config_key: child_step
            for child_step in self.SUPPORTED_CHILD_STEPS
        }

    @property
    def config_key(self):
        """Return key of step type in config"""
        if self.CONFIG_KEY is None:
            raise NotImplementedError
        return self.CONFIG_KEY
