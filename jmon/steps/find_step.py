
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from jmon.client_type import ClientType
from jmon.errors import StepValidationError
from jmon.step_state import SeleniumStepState
from jmon.step_status import StepStatus

from jmon.steps.action_step import ActionStep
from jmon.steps.base_step import BaseStep
from jmon.logger import logger
from jmon.steps.check_step import CheckStep
from jmon.utils import retry


class FindStep(BaseStep):

    CONFIG_KEY = "find"

    @property
    def supported_clients(self):
        """Return list of supported clients"""
        return [
            ClientType.BROWSER_FIREFOX,
            ClientType.BROWSER_CHROME
        ]

    @property
    def supported_child_steps(self):
        """Return list of child support step classes"""
        return [
            FindStep,
            ActionStep,
            CheckStep
        ]

    @property
    def id(self):
        """ID string for step"""
        return f"Find"

    @property
    def description(self):
        """Friendly description of step"""
        _, description, _ = self._get_find_type()
        return f"Find element {description}"

    def _validate_step(self):
        """Check step is valid"""
        found_types = []
        for supported_check_type in ['id', 'class', 'text', 'placeholder', 'tag']:
            if self._config.get(supported_check_type):
                found_types.append(supported_check_type)
        
        # Allow 1 type or
        # text/placeholder with tag
        if not (len(found_types) == 1 or ('tag' in found_types and ('placeholder' in found_types or 'text' in found_types))):
            raise StepValidationError("Find only supports one of: id, class, tag. Or placeholder or text with optional tag")

    def _get_find_type(self):
        """Get find type based on config"""
        by_type = None
        description = None
        value = None

        if id := self._config.get('id'):
            by_type = By.ID
            value = id
            description = f"by ID: {value}"
        elif (text := self._config.get('text')) or (placeholder := self._config.get('placeholder')):
            if text:
                xpath_key = 'text'
                xpath_value = text

            elif placeholder:
                xpath_key = 'placeholder'
                xpath_value = placeholder
            tag = self._config.get('tag')
            description = f"by {xpath_key}: {xpath_value}"
            if not tag:
                tag = '*'
            else:
                description += f" and tag: {tag}"

            # Search by XPATH
            by_type = By.XPATH
            value = f".//{tag}[contains({xpath_key}(), '{xpath_value}')]"

        elif class_name := self._config.get('class'):
            by_type = By.CLASS_NAME
            value = class_name
            description = f"by class: {value}"

        elif tag := self._config.get('tag'):
            by_type = By.TAG_NAME
            value = tag
            description = f"by tag: {value}"

        return by_type, description, value

    @retry(count=5, interval=0.5)
    def _find_element(self, element, by_type, value):
        """Find element"""
        try:
            return element.find_element(by_type, value)
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.ElementNotInteractableException) as exc:
            self._logger.error("Could not find element")
            self._logger.debug(str(exc).split("\n")[0])
            return None

    def execute_selenium(self, state: SeleniumStepState):
        """Find element on page"""
        by_type, _, value, = self._get_find_type()
        element = self._find_element(state.element, by_type, value)
        if not element:
            self._set_status(StepStatus.FAILED)
        state.element = element
