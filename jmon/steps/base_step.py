

from io import StringIO
import logging
from jmon.logger import logger
from jmon.step_status import StepStatus


class BaseStep:

    CONFIG_KEY = None
    CHILD_STEPS_FORM_STEP = False

    def __init__(self, run, config, parent, enable_log=True):
        """Store member variables"""
        self._config = config
        self._run = run
        self._parent = parent
        self._child_steps = None
        self._status = StepStatus.NOT_RUN
        self._should_log = enable_log

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

    @property
    def status(self):
        """Return current status"""
        return self._status

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

        # Add log handlder from root of run, if configured to log
        if self._should_log:
            self._logger.addHandler(self._run.log_handler)

    def get_child_steps(self):
        """Get child steps"""
        # Return cached child steps
        if self._child_steps is None:

            self._child_steps = []

            if not self._config or type(self._config) not in [list, dict]:
                return self._child_steps

            supported_child_steps = self.get_supported_child_steps()

            # Handle lists of steps
            if type(self._config) is list:
                for step_config in self._config:
                    for supported_step_name, supported_step_class in supported_child_steps.items():
                        if supported_step_name in step_config:
                            self._child_steps.append(
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
                        self._child_steps.append(
                            supported_child_steps[step_name](
                                run=self._run,
                                config=self._config[step_name],
                                parent=self
                            )
                        )

        return self._child_steps

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

    def _set_status(self, status):
        """Set status"""
        if status is StepStatus.FAILED:
            self._logger.error("Step failed")
        elif status is StepStatus.SUCCESS:
            self._logger.info(f"Step completed")
        self._status = status

    def execute(self, selenium_instance, element):
        """Execute the current step and then execute each of the child steps"""
        self._status = StepStatus.RUNNING

        self._logger.info(f"Starting {self.id}")
        self._logger.info(self.description)

        element = self._execute(selenium_instance, element)

        if self.status is StepStatus.FAILED:
            return element, self.status

        # If child steps do not form part of this step,
        # mark status as success, if not already failed.
        if not self.CHILD_STEPS_FORM_STEP:
            self._set_status(StepStatus.SUCCESS)

        child_status = None

        for step in self.get_child_steps():
            _, child_status = step.execute(selenium_instance, element)

            # If child step has failed, return early
            if child_status is StepStatus.FAILED:
                break

        if self.CHILD_STEPS_FORM_STEP:
            # Set current step to failed if child step has failed.
            if child_status is StepStatus.FAILED:
                self._set_status(StepStatus.FAILED)
            else:
                self._set_status(StepStatus.SUCCESS)

        return element, (self.status if child_status is not StepStatus.FAILED else StepStatus.FAILED)
