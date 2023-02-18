
import os
import re
from selenium.webdriver.common.keys import Keys

from jmon.steps.actions.base_action import BaseAction
from jmon.logger import logger


class ScreenshotAction(BaseAction):

    CONFIG_KEY = "screenshot"
    NAME_REGEX = re.compile(r'[^\w^_^-]')
    TEMP_DIRECTORY = '/tmp'

    @property
    def id(self):
        """ID string for step"""
        return f"Screenshot"

    @property
    def description(self):
        """Friendly description of step"""
        return f"Taking screenshot of browser: {self.screenshot_file_name}"

    @property
    def screenshot_file_name(self):
        """Return name of screenshot file"""
        # Handle None screenshot name
        screenshot_name = self._config or ''

        # Remove any special characters from screenshot
        screenshot_name = self.NAME_REGEX.sub('', screenshot_name)

        if not screenshot_name:
            raise Exception('Screenshot name is invalid')

        return f"{screenshot_name}.png"

    def _execute(self, selenium_instance, element):
        """Press keyboard key"""
        screenshot_path = os.path.join(self.TEMP_DIRECTORY, self.screenshot_file_name)

        selenium_instance.save_screenshot(screenshot_path)

        self._run.register_artifact(screenshot_path)

        return element
