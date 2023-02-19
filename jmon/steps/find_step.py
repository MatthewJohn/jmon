
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from jmon.step_status import StepStatus

from jmon.steps.action_step import ActionStep
from jmon.steps.base_step import BaseStep
from jmon.logger import logger
from jmon.steps.check_step import CheckStep
from jmon.utils import retry


class FindStep(BaseStep):

    CONFIG_KEY = "find"

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
        return description

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
            value = f"//{tag}[@{xpath_key}='{xpath_value}']"

        elif class_name := self._config.get('class'):
            by_type = By.CLASS_NAME
            value = class_name
            description = "by class: {value}"

        elif tag := self._config.get('tag'):
            by_type = By.TAG_NAME
            value = tag
            description = "by tag: {value}"

        return by_type, description, value

    @retry(count=5, interval=0.5)
    def _find_element(self, element, by_type, value):
        """Find element"""
        try:
            return element.find_element(by_type, value)
        except selenium.common.exceptions.NoSuchElementException as exc:
            self._logger.error("Could not find element")
            self._logger.debug(str(exc))
            return None

    def _execute(self, selenium_instance, element):
        """Find element on page"""
        by_type, _, value, = self._get_find_type()
        element = self._find_element(element, by_type, value)
        if not element:
            self._set_status(StepStatus.FAILED)
        return element
