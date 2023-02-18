

from io import StringIO
import logging
from jmon.logger import logger


class BaseStep:

    CONFIG_KEY = None

    def __init__(self, run, config, parent):
        """Store member variables"""
        self._config = config
        self._run = run
        self._parent = parent

        self._setup_logging()

        logger.debug(f"Creating step: {self.__class__.__name__}: {config}")

    @property
    def full_id(self):
        """Return full Id for step"""
        id = ""
        if self._parent is not None:
            id = self._parent.full_id + " -> "
        id += self.id
        return id

    @property
    def id(self):
        """ID string for step"""
        raise NotImplementedError

    @property
    def description(self):
        """Friendly description of step"""
        raise NotImplementedError

    def _setup_logging(self):
        """Setup logger"""
        self._logger = logging.getLogger(self.full_id)
        self._log_stream = StringIO()

        # Create local log handler
        self._log_handler = logging.StreamHandler(self._log_stream)
        self._log_handler.setLevel(logging.INFO)

        # Add format for user-friendly logs
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        self._log_handler.setFormatter(formatter)
        self._logger.addHandler(self._log_handler)

        # Add log handlder from root of run
        self._logger.addHandler(self._run.log_handler)

    def get_child_steps(self):
        """Get child steps"""
        steps = []

        if not self._config or type(self._config) not in [list, dict]:
            return steps

        supported_child_steps = self.get_supported_child_steps()

        # Handle lists of steps
        if type(self._config) is list:
            for step_config in self._config:
                for supported_step_name, supported_step_class in supported_child_steps.items():
                    if supported_step_name in step_config:
                        steps.append(
                            supported_step_class(
                                run=self._run,
                                config=step_config[supported_step_name],
                                parent=self
                            )
                        )

        # Handle check dictionaries
        elif type(self._config) is dict:
            for step_name in self._config:
                if step_name in supported_child_steps:
                    steps.append(
                        supported_child_steps[step_name](
                            run=self._run,
                            config=self._config[step_name],
                            parent=self
                        )
                    )

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
        self._logger.info(f"Starting {self.id}: {self.description}")
        element = self._execute(selenium_instance, element)
        self._logger.info(f"Completed {self.id}")

        for step in self.get_child_steps():
            step.execute(selenium_instance, element)
        return element
