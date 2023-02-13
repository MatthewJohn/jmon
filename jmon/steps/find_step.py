
from selenium.webdriver.common.by import By

from jmon.steps.base_step import BaseStep
from jmon.logger import logger


class FindStep(BaseStep):

    CONFIG_KEY = "find"
    SUPPORTED_CHILD_STEPS = []

    def _execute(self, selenium_instance, element):
        """Find element on page"""
        if id := self._config.get('id'):
            logger.info(f"Finding element by id: {id}")
            element.find_element(By.ID, id)
        if class_name := self._config.get('class'):
            logger.info(f"Finding element by class: {class_name}")
            element.find_element(By.ID, class_name)
        return element