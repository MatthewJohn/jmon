
from selenium.webdriver.common.by import By

from jmon.steps.action_step import ActionStep
from jmon.steps.base_step import BaseStep
from jmon.logger import logger


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

    def _execute(self, selenium_instance, element):
        """Find element on page"""
        if id := self._config.get('id'):
            logger.info(f"Finding element by id: {id}")
            element = element.find_element(By.ID, id)
        if class_name := self._config.get('class'):
            logger.info(f"Finding element by class: {class_name}")
            element = element.find_element(By.ID, class_name)
        if tag := self._config.get('tag'):
            logger.info(f"Finding element by tag: {tag}")
            element = element.find_element(By.TAG_NAME, tag)
        return element

