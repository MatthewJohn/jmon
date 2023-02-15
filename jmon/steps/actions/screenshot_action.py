
import os
import re
from selenium.webdriver.common.keys import Keys

from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


class ScreenshotAction(BaseAction):

    CONFIG_KEY = "screenshot"
    NAME_REGEX = re.compile(r'[^\w^_^-]')
    TEMP_DIRECTORY = '/tmp'


    def _execute(self, selenium_instance, element):
        """Press keyboard key"""
        # Handle None screenshot name
        screenshot_name = self._config or ''

        # Remove any special characters from screenshot
        screenshot_name = self.NAME_REGEX.sub('', screenshot_name)

        if not screenshot_name:
            raise Exception('Screenshot name is invalid')

        screenshot_path = os.path.join(self.TEMP_DIRECTORY, '{}.png'.format(screenshot_name))

        selenium_instance.save_screenshot(screenshot_path)

        self._run.register_artifact(screenshot_path)

        return element
