
from selenium.webdriver.common.by import By

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

    @retry(count=5, interval=0.5)
    def _execute(self, selenium_instance, element):
        """Find element on page"""
        if id := self._config.get('id'):
            logger.info(f"Finding element by id: {id}")
            element = element.find_element(By.ID, id)
        elif (text := self._config.get('text')) or (placeholder := self._config.get('placeholder')):
            if text:
                xpath_key = 'text'
                xpath_value = text
            elif placeholder:
                xpath_key = 'placeholder'
                xpath_value = placeholder
            tag = self._config.get('tag')
            if not tag:
                tag = '*'
            # Search by XPATH
            element = element.find_element(By.XPATH, f"//{tag}[@{xpath_key}='{xpath_value}']")

        elif class_name := self._config.get('class'):
            logger.info(f"Finding element by class: {class_name}")
            element = element.find_element(By.CLASS_NAME, class_name)
        elif tag := self._config.get('tag'):
            logger.info(f"Finding element by tag: {tag}")
            element = element.find_element(By.TAG_NAME, tag)
        return element

