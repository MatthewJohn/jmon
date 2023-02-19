
from time import sleep

from pyvirtualdisplay import Display
import selenium
from jmon.step_status import StepStatus

from jmon.steps import RootStep
from jmon.steps.actions.screenshot_action import ScreenshotAction


class Runner:
    """Execute run"""

    DISPLAY = None
    SELENIUM_INSTANCE = None

    @staticmethod
    def get_display():
        if Runner.DISPLAY is None:
            Runner.DISPLAY = Display(visible=0, size=(1920, 1080))
            Runner.DISPLAY.start()
        return Runner.DISPLAY

    @staticmethod
    def get_selenium_instance():
        # Get display
        Runner.get_display()

        if Runner.SELENIUM_INSTANCE is None:
            Runner.SELENIUM_INSTANCE = selenium.webdriver.Firefox()
            Runner.SELENIUM_INSTANCE.implicitly_wait(1)
        Runner.SELENIUM_INSTANCE.delete_all_cookies()
        return Runner.SELENIUM_INSTANCE

    def perform_check(self, run):
        """Setup selenium and perform checks"""
        selenium_instance = self.get_selenium_instance()

        root_step = RootStep(run=run, config=run.check.steps, parent=None)

        _, status = root_step.execute(
            selenium_instance=selenium_instance,
            element=selenium_instance
        )

        if status is StepStatus.FAILED and run.check.should_screenshot_on_error:
            # Perform failure screenshot, if configured
            error_screenshot = ScreenshotAction(
                run=run,
                config="failure",
                parent=root_step,
                enable_log=False
            )
            error_screenshot.execute(
                selenium_instance=selenium_instance,
                element=selenium_instance
            )

        return status
