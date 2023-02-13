
from selenium.webdriver.common.keys import Keys

from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


class PressAction(BaseAction):

    CONFIG_KEY = "press"

    def _execute(self, selenium_instance, element):
        """Press keyboard key"""
        if self._config.lower() == "enter":

            logger.info(f"Pressing enter")
            element.send_keys(Keys.ENTER)
        else:
            raise Exception(f'Unknown press action: {self._config}')

        return element
